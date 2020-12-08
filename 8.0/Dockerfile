FROM php:8.0-fpm-alpine

ENV ASUSER= \
    UID= \
    COMPOSER_ALLOW_SUPERUSER=1 \
    COMPOSER_MEMORY_LIMIT=-1 \
    ENABLE_XDEBUG=false \
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
    # build-deps
    && apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
        freetype-dev libpng-dev libjpeg-turbo-dev \
        icu-dev libedit-dev libxml2-dev \
        imagemagick-dev openldap-dev oniguruma-dev \
    # php-ext
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && export CFLAGS="$PHP_CFLAGS" CPPFLAGS="$PHP_CPPFLAGS" LDFLAGS="$PHP_LDFLAGS" \
    && docker-php-ext-install -j$(nproc) \
        bcmath \
        calendar \
        exif \
        gd \
        intl \
        ldap \
        mbstring \
        pcntl \
        pdo \
        pdo_mysql \
        readline \
        soap \
        xml \
        zip \
    # Temporarily building for PHP 8.0: https://github.com/Imagick/imagick/issues/358
    && git clone https://github.com/Imagick/imagick \
    && cd imagick \
    && phpize \
    && ./configure \
    && make \
    && make install \
    && cd ../ \
    && rm -rf imagick \
    && pecl install redis xdebug \
    && docker-php-ext-enable imagick \
    && docker-php-ext-enable redis \
    && cp "/usr/local/etc/php/php.ini-development" "/usr/local/etc/php/php.ini" \
    # composer
    && curl -sS https://getcomposer.org/installer | php -- --1 --install-dir=/usr/local/bin --filename=composer \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer2 \
    && su-exec kool composer global require hirak/prestissimo \
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
