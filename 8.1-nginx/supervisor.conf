[supervisord]
logfile=/dev/stdout
logfile_maxbytes=0
pidfile=/run/supervisord.pid
nodaemon=true

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
