FROM {{ $from }}

ENV ASUSER= \
    UID= \
    COMPOSER_ALLOW_SUPERUSER=1 \
    COMPOSER_MEMORY_LIMIT=-1 \
@unless ($prod)
    ENABLE_XDEBUG=false \
@endunless
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
    && DOCKERIZE_ARCH="$( [ "$(uname -m)" = "aarch64" ] && echo arm64 || echo amd64 )" \
    && curl -L "https://github.com/jwilder/dockerize/releases/download/v0.9.3/dockerize-linux-${DOCKERIZE_ARCH}-v0.9.3.tar.gz" | tar xz \
    && mv dockerize /usr/local/bin/dockerize \
    # deps
    && apk --no-cache add su-exec bash sed git openssh-client icu shadow procps \
        freetype libpng libjpeg-turbo libzip-dev ghostscript imagemagick \
        jpegoptim optipng pngquant gifsicle libldap \
        libpq less \
    # build-deps
    && apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
        freetype-dev libpng-dev libjpeg-turbo-dev \
        icu-dev libedit-dev libxml2-dev \
        imagemagick-dev openldap-dev {{ version_compare($version, '7.4', '>=') ? 'oniguruma-dev' : '' }} libwebp-dev \
        postgresql-dev \
        linux-headers \
    # php-ext
@if (version_compare($version, '7.4', '>='))
    && docker-php-ext-configure gd --with-freetype --with-webp --with-jpeg \
@else
    && docker-php-ext-configure gd \
        --with-freetype-dir=/usr/include/ \
        --with-png-dir=/usr/include/ \
        --with-jpeg-dir=/usr/include/ \
@endif
    && export CFLAGS="$PHP_CFLAGS" CPPFLAGS="$PHP_CPPFLAGS" LDFLAGS="$PHP_LDFLAGS" \
    && docker-php-ext-install -j$(nproc) \
        bcmath \
        calendar \
        exif \
        gd \
        intl \
        ldap \
        mbstring \
@if ($prod)
        opcache \
@endif
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
@if (! $prod)
    && pecl install {{ version_compare($version, '8', '>=') ? 'xdebug' : 'xdebug-3.1.6' }} \
    && pecl install pcov && docker-php-ext-enable pcov \
@endif
@if (version_compare($version, '8.2', '<='))
    && pecl install imagick \
    && docker-php-ext-enable imagick \
@else
@if (version_compare($version, '8.4', '=='))
@else
    && mkdir /tmp/imagick && cd /tmp/imagick \
    && curl -L -o /tmp/imagick.tar.gz https://github.com/Imagick/imagick/archive/refs/tags/3.7.0.tar.gz \
    && tar --strip-components=1 -xf /tmp/imagick.tar.gz \
    && phpize \
    && ./configure --with-webp=yes \
    && make \
    && make install \
    && echo "extension=imagick.so" > /usr/local/etc/php/conf.d/ext-imagick.ini \
@endif
@endif
    && docker-php-ext-enable redis \
    && cp "/usr/local/etc/php/php.ini-{{ $prod ? 'production' : 'development' }}" "/usr/local/etc/php/php.ini" \
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
