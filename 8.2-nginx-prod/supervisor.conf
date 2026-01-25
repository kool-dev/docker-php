[supervisord]
logfile=/dev/stdout
logfile_maxbytes=0
pidfile=/run/supervisord.pid
nodaemon=true

[program:nginx]
depends_on = php-fpm
command = nginx -g "daemon off;"
autorestart = true
stopasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
stderr_logfile_maxbytes = 0
stdout_logfile_maxbytes = 0

[program:php-fpm]
command = php-fpm
autorestart = true
stopasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
stderr_logfile_maxbytes = 0
stdout_logfile_maxbytes = 0
