[program:nginx]
depends_on = php-fpm
command = nginx -g "daemon off;"
stopasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout

[program:php-fpm]
command = php-fpm
stopasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
