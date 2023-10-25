FROM {{ $from }}

RUN apk add --update --no-cache npm yarn \
    && rm -rf /var/cache/apk/* /tmp/*
