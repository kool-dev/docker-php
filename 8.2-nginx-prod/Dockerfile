FROM kooldev/php:8.2-prod

ENV PHP_FPM_LISTEN=/run/php-fpm.sock \
    NGINX_LISTEN=80 \
    NGINX_ROOT=/app/public \
    NGINX_INDEX=index.php \
    NGINX_CLIENT_MAX_BODY_SIZE=25M \
    NGINX_PHP_FPM=unix:/run/php-fpm.sock \
    NGINX_FASTCGI_READ_TIMEOUT=60s \
    NGINX_FASTCGI_BUFFERS='8 8k' \
    NGINX_FASTCGI_BUFFER_SIZE='16k' \
    NGINX_ENTRYPOINT_WORKER_PROCESSES_AUTOTUNE=true

RUN curl -L https://github.com/ochinchina/supervisord/releases/download/v0.6.3/supervisord_static_0.6.3_linux_amd64 -o /usr/local/bin/supervisord \
    && chmod +x /usr/local/bin/supervisord \
    && apk add --no-cache nginx \
    && chown -R kool:kool /var/lib/nginx \
    && chmod 770 /var/lib/nginx/tmp \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    # add h5bp/server-configs-nginx
    && mkdir -p /etc/nginx/conf.d \
    && mkdir /etc/nginx/h5bp \
    && cd /etc/nginx/h5bp \
    && wget https://github.com/h5bp/server-configs-nginx/archive/refs/tags/3.3.0.tar.gz -O h5bp.tgz \
    && tar xzvf h5bp.tgz \
    && rm -f h5bp.tgz \
    && mv server-configs-nginx-*/h5bp/* . \
    && mv server-configs-nginx-*/nginx.conf /etc/nginx/nginx.conf \
    && sed -i "s|^user .*|user\ kool kool;|g" /etc/nginx/nginx.conf \
    && mv server-configs-nginx-*/mime.types /etc/nginx/mime.types \
    && rm -rf server-configs-nginx-* \
    && curl -L https://raw.githubusercontent.com/nginxinc/docker-nginx/master/entrypoint/30-tune-worker-processes.sh -o /kool/30-tune-worker-processes.sh \
    && chmod +x /kool/30-tune-worker-processes.sh

COPY supervisor.conf /kool/supervisor.conf
COPY default.tmpl /kool/default.tmpl
COPY entrypoint /kool/entrypoint
RUN chmod +x /kool/entrypoint

EXPOSE 80

CMD [ "supervisord", "-c", "/kool/supervisor.conf" ]
