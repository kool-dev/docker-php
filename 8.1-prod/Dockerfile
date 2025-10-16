FROM php:8.1-fpm-alpine

ENV ASUSER= \
    UID= \
    COMPOSER_ALLOW_SUPERUSER=1 \
    COMPOSER_MEMORY_LIMIT=-1 \
    PHP_DATE_TIMEZONE=UTC \
    PHP_MEMORY_LIMIT=256M \
    PHP_MAX_INPUT_VARS=1000 \
    PHP_UPLOAD_MAX_FILESIZE=25M \
    PHP_POST_MAX_SIZE=25M \
    PHP_MAX_EXECUTION_TIME=30 \
    PHP_FPM_LISTEN=9000 \
    PHP_FPM_MAX_CHILDREN=10 \
    PHP_FPM_REQUEST_TERMINATE_TIMEOUT=60 \
    ENTRYPOINT=entrypoint.php.sh

WORKDIR /app

RUN adduser -D -u 1337 kool \
    && addgroup kool www-data \
    # dockerize
    && curl -L https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-alpine-linux-amd64-v0.6.1.tar.gz | tar xz \
    && mv dockerize /usr/local/bin/dockerize \
    # deps
    && apk --no-cache add su-exec bash sed git openssh-client icu shadow procps \
        freetype libpng libjpeg-turbo libzip-dev ghostscript imagemagick \
        jpegoptim optipng pngquant gifsicle libldap \
        libpq less \
    # build-deps
    && cp "/usr/local/etc/php/php.ini-production" "/usr/local/etc/php/php.ini" \
    && apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
        freetype-dev libpng-dev libjpeg-turbo-dev \
        icu-dev libedit-dev libxml2-dev \
        imagemagick-dev openldap-dev oniguruma-dev libwebp-dev \
        postgresql-dev \
        linux-headers \
    # php-ext
    && docker-php-ext-configure gd --with-freetype --with-webp --with-jpeg \
    && export CFLAGS="$PHP_CFLAGS" CPPFLAGS="$PHP_CPPFLAGS" LDFLAGS="$PHP_LDFLAGS" \
    && docker-php-ext-install -j$(nproc) \
        bcmath \
        calendar \
        exif \
        gd \
        intl \
        ldap \
        mbstring \
        opcache \
        pcntl \
        pdo \
        pdo_mysql \
        pdo_pgsql \
        soap \
        xml \
        zip \
        sockets \
        mysqli \
        ftp \
    && pecl install redis \
    && pecl install imagick \
    && docker-php-ext-enable imagick \
    && docker-php-ext-enable redis \
    # composer
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && curl -sS https://getcomposer.org/installer | php -- --1 --install-dir=/usr/local/bin --filename=composer1 \
    # cleanup
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* /tmp/*

COPY kool.ini /kool/kool.tmpl
COPY zz-docker.conf /kool/zz-docker.tmpl
COPY entrypoint /kool/entrypoint
RUN chmod +x /kool/entrypoint

EXPOSE 9000

ENTRYPOINT [ "/kool/entrypoint" ]
CMD [ "php-fpm" ]
