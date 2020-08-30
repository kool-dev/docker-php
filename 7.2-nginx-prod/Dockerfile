FROM kooldev/php:7.2-prod

ENV PHP_FPM_LISTEN=/run/php-fpm.sock \
    NGINX_LISTEN=80 \
    NGINX_ROOT=/app/public \
    NGINX_CLIENT_MAX_BODY_SIZE=25M \
    NGINX_PHP_FPM=unix:/run/php-fpm.sock \
    NGINX_FASTCGI_READ_TIMEOUT=60s

RUN curl -L https://github.com/ochinchina/supervisord/releases/download/v0.6.3/supervisord_static_0.6.3_linux_amd64 -o /usr/local/bin/supervisord \
    && chmod +x /usr/local/bin/supervisord \
    && apk add --no-cache nginx \
    && sed -i "s|^user .*|user\ kool;|g" /etc/nginx/nginx.conf \
    && chown -R kool:kool /var/lib/nginx \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY supervisor.conf /kool/supervisor.conf
COPY default.tmpl /kool/default.tmpl

EXPOSE 80

ENTRYPOINT [ "dockerize", "-template", "/kool/kool.tmpl:/usr/local/etc/php/conf.d/kool.ini", "-template", "/kool/zz-docker.tmpl:/usr/local/etc/php-fpm.d/zz-docker.conf", "-template", "/kool/default.tmpl:/etc/nginx/conf.d/default.conf", "/kool/entrypoint" ]
CMD [ "supervisord", "-c", "/kool/supervisor.conf" ]
