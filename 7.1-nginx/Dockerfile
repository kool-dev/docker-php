FROM kooldev/php:7.1

ENV PHP_FPM_LISTEN=/run/php-fpm.sock \
    NGINX_LISTEN=80 \
    NGINX_ROOT=/app/public \
    NGINX_CLIENT_MAX_BODY_SIZE=25M \
    NGINX_PHP_FPM=unix:/run/php-fpm.sock

RUN curl -L https://github.com/ochinchina/supervisord/releases/download/v0.6.3/supervisord_static_0.6.3_linux_amd64 -o /usr/local/bin/supervisord \
    && chmod +x /usr/local/bin/supervisord \
    && apk add --no-cache nginx \
    && sed -i "s|^listen\ \=.*|listen\ \= $PHP_FPM_LISTEN|g" /usr/local/etc/php-fpm.d/zz-docker.conf \
    && echo "listen.owner = kool" >> /usr/local/etc/php-fpm.d/zz-docker.conf \
    && echo "listen.group = kool" >> /usr/local/etc/php-fpm.d/zz-docker.conf \
    && echo "listen.mode = 0666" >> /usr/local/etc/php-fpm.d/zz-docker.conf
    

COPY supervisor.conf /kool/supervisor.conf
COPY default.tmpl /kool/default.tmpl

EXPOSE 80

ENTRYPOINT [ "dockerize", "-template", "/kool/kool.tmpl:/usr/local/etc/php/conf.d/kool.ini", "-template", "/kool/default.tmpl:/etc/nginx/conf.d/default.conf", "/kool/entrypoint" ]
CMD [ "supervisord", "-c", "/kool/supervisor.conf" ]
