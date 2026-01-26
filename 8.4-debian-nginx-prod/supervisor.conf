[supervisord]
logfile=/dev/stdout
logfile_maxbytes=0
pidfile=/run/supervisord.pid
nodaemon=true

[program:php-fpm]
command = php-fpm
priority = 10
autorestart = true
stopasgroup = true
killasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
stderr_logfile_maxbytes = 0
stdout_logfile_maxbytes = 0

[program:nginx]
command = nginx -g "daemon off;"
priority = 20
autorestart = true
stopasgroup = true
killasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
stderr_logfile_maxbytes = 0
stdout_logfile_maxbytes = 0
