server {
    listen @{{ .Env.NGINX_LISTEN }} default_server;
    server_name _;
    root @{{ .Env.NGINX_ROOT }};
    index index.php;
    charset utf-8;

    location = /favicon.ico { log_not_found off; access_log off; }
    location = /robots.txt  { log_not_found off; access_log off; }

    client_max_body_size @{{ .Env.NGINX_CLIENT_MAX_BODY_SIZE }};

    error_page 404 /index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;

        add_header X-Served-By kool.dev;
    }

    location ~ \.php$ {
        fastcgi_pass @{{ .Env.NGINX_PHP_FPM }};
        fastcgi_read_timeout @{{ .Env.NGINX_FASTCGI_READ_TIMEOUT }};
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
