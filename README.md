![CI/CD](https://github.com/kool-dev/docker-php/workflows/CI/CD/badge.svg)

## Description

Minimal PHP Docker image focused on Laravel applications. It's use is intended for [kool.dev](https://github.com/kool-dev/kool), but can fit in any other PHP use-case.

The images with Nginx include [`h5bp/server-configs-nginx`](https://github.com/h5bp/server-configs-nginx) with a hand picked set of configuration active by default. So if you want to change or add a new server configuration you can `include h5bp/...` as you see fit.

### Usage

Simplest example:

[![asciicast](https://asciinema.org/a/388121.svg)](https://asciinema.org/a/388121)

##### About `composer`

> All images currently ship out with Composer 2.x as the default version. If for some reason you still need to use Composer 1.x and cannot make the upgrade, we still ship a `composer1` in the images PATH as well, which is latest Composer 1.x version. Feel free to use it while you prepare to move to 2.0.

## Available Tags

The image built is [`kooldev/php`](https://hub.docker.com/r/kooldev/php/tags?page=1&ordering=last_updated) which has a bunch of tags available:

### 8.0

- [8.0](https://github.com/kool-dev/docker-php/blob/master/8.0/Dockerfile)
- [8.0-prod](https://github.com/kool-dev/docker-php/blob/master/8.0-prod/Dockerfile)
- [8.0-nginx](https://github.com/kool-dev/docker-php/blob/master/8.0-nginx/Dockerfile)
- [8.0-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.0-nginx-prod/Dockerfile)

### 7.4

- [7.4](https://github.com/kool-dev/docker-php/blob/master/7.4/Dockerfile)
- [7.4-prod](https://github.com/kool-dev/docker-php/blob/master/7.4-prod/Dockerfile)
- [7.4-nginx](https://github.com/kool-dev/docker-php/blob/master/7.4-nginx/Dockerfile)
- [7.4-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.4-nginx-prod/Dockerfile)

### 7.3

- [7.3](https://github.com/kool-dev/docker-php/blob/master/7.3/Dockerfile)
- [7.3-prod](https://github.com/kool-dev/docker-php/blob/master/7.3-prod/Dockerfile)
- [7.3-nginx](https://github.com/kool-dev/docker-php/blob/master/7.3-nginx/Dockerfile)
- [7.3-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.3-nginx-prod/Dockerfile)

### 7.2

- [7.2](https://github.com/kool-dev/docker-php/blob/master/7.2/Dockerfile)
- [7.2-prod](https://github.com/kool-dev/docker-php/blob/master/7.2-prod/Dockerfile)
- [7.2-nginx](https://github.com/kool-dev/docker-php/blob/master/7.2-nginx/Dockerfile)
- [7.2-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.2-nginx-prod/Dockerfile)

### 7.1

- [7.1](https://github.com/kool-dev/docker-php/blob/master/7.1/Dockerfile)
- [7.1-prod](https://github.com/kool-dev/docker-php/blob/master/7.1-prod/Dockerfile)
- [7.1-nginx](https://github.com/kool-dev/docker-php/blob/master/7.1-nginx/Dockerfile)
- [7.1-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.1-nginx-prod/Dockerfile)

## More flavours

We can always extend these images to suit them to our current use case. For example, we have a few extensions for specific use cases:

- [Oracle OCI8 database](https://github.com/kool-dev/docker-php-oci8)
- [MS SQL Server `sqlsrv` database](https://github.com/kool-dev/docker-php-sqlsrv)

## Environment Variables

Variable | Default Value | Description
--- | --- | ---
**ASUSER** | `0` | Changes the user id that executes the commands
**UID** | `0` | Changes the user id that executes the commands **(ignored if ASUSER is provided)**
**COMPOSER_ALLOW_SUPERUSER** | `1` | Allows composer to run with super user
**COMPOSER_MEMORY_LIMIT** | `-1` | Changes composer memory limit
**ENABLE_XDEBUG** | `false` | Enables the Xdebug extension
**PHP_DATE_TIMEZONE** | `UTC` | Changes timezone used by date/time functions
**PHP_MEMORY_LIMIT** | `256M` | Changes PHP memory limit
**PHP_MAX_INPUT_VARS** | `1000`  | Changes how many input variables may be accepted on PHP
**PHP_UPLOAD_MAX_FILESIZE** | `25M` | Changes PHP maximum size of an uploaded file
**PHP_POST_MAX_SIZE** | `25M` | Changes PHP max size of post data allowed
**PHP_MAX_EXECUTION_TIME** | `30` | Changes PHP maximum time is allowed to run a script
**PHP_FPM_LISTEN** | `9000` | Changes the PORT address of the FastCGI requests
**PHP_FPM_MAX_CHILDREN** | `10` | Changes the number of child processes to be used on FPM
**PHP_FPM_REQUEST_TERMINATE_TIMEOUT** | `60` | Changes FPM timeout to serve a single request

### NGINX

Variable | Default Value | Description
--- | --- | ---
**NGINX_LISTEN** | `80` | Changes the PORT address
**NGINX_ROOT** | `/app/public` | Changes NGINX root directive
**NGINX_INDEX** | `index.php` | Changes the index directive
**NGINX_CLIENT_MAX_BODY_SIZE** | `25M` | Changes maximum allowed size of the client request body
**NGINX_PHP_FPM** | `unix:/run/php-fpm.sock` | Changes the address of a FastCGI server
**NGINX_FASTCGI_READ_TIMEOUT** | `60s` | Changes a timeout for reading a response from the FastCGI server
**NGINX_FASTCGI_BUFFERS** | `8 8k` | Changes the number and size of the buffers used for reading a response
**NGINX_FASTCGI_BUFFER_SIZE** | `16k` | Changes the size of the buffer used for reading the first part of the response received

## Usage

With `docker run`:

```sh
docker run -it --rm kooldev/php:7.4 php -v
```

With environment variables:

```sh
docker run -it --rm -e ENABLE_XDEBUG=true kooldev/php:7.4-prod php -v
```

With `docker-compose.yml`:

```yaml
app:
  image: kooldev/php:7.4
  ports:
    - "9773:9773"
  volumes:
    - ".:/app:cached"
    - "$HOME/.ssh/id_rsa:/home/developer/.ssh/id_rsa:cached"
  environment:
    ASUSER: "${$UID}"
```

## Contributing

### Update images with templates

You should change `fwd-template.json` for configuration and `template` folder for the actual base templates.

After any changes, we need to run `kool run template` to parse the templates and generate all versions folder/files.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
