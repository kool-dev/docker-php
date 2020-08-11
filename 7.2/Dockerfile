FROM php:7.2-fpm-alpine

ENV ASUSER= \
    UID= \
    COMPOSER_ALLOW_SUPERUSER=1 \
    ENABLE_XDEBUG=false \
    PHP_MEMORY_LIMIT=256M \
    PHP_MAX_INPUT_VARS=1000 \
    PHP_UPLOAD_MAX_FILESIZE=25M \
    PHP_POST_MAX_SIZE=25M \
    ENTRYPOINT=entrypoint.php.sh

WORKDIR /app

RUN adduser -D -u 1337 kool \
    # dockerize
    && curl -L https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-alpine-linux-amd64-v0.6.1.tar.gz | tar xz \
    && mv dockerize /usr/local/bin/dockerize \
    # deps
    && apk --no-cache add su-exec bash git openssh-client icu shadow procps \
        freetype libpng libjpeg-turbo libzip-dev imagemagick \
        jpegoptim optipng pngquant gifsicle libldap \
    # build-deps
    && apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
        freetype-dev libpng-dev libjpeg-turbo-dev \
        icu-dev libedit-dev libxml2-dev \
        imagemagick-dev openldap-dev  \
    # php-ext
    && docker-php-ext-configure gd \
        --with-freetype-dir=/usr/include/ \
        --with-png-dir=/usr/include/ \
        --with-jpeg-dir=/usr/include/ \
    && export CFLAGS="$PHP_CFLAGS" CPPFLAGS="$PHP_CPPFLAGS" LDFLAGS="$PHP_LDFLAGS" \
    && pecl install imagick-3.4.4 redis xdebug \
    && docker-php-ext-enable imagick redis \
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
    && cp "/usr/local/etc/php/php.ini-development" "/usr/local/etc/php/php.ini" \
    && sed -i "s/user\ \=.*/user\ \= kool/g" /usr/local/etc/php-fpm.d/www.conf \
    # composer
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && su-exec kool composer global require hirak/prestissimo \
    # cleanup
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* /tmp/* /home/kool/.composer/cache

COPY kool.ini /kool/kool.tmpl
COPY entrypoint /kool/entrypoint
RUN chmod +x /kool/entrypoint

EXPOSE 9000

ENTRYPOINT [ "dockerize", "-template", "/kool/kool.tmpl:/usr/local/etc/php/conf.d/kool.ini", "/kool/entrypoint" ]
CMD [ "php-fpm" ]
