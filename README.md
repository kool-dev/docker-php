![CI/CD](https://github.com/kool-dev/docker-php/workflows/CI/CD/badge.svg)

## Description

PHP Docker images focused on Laravel applications. They're intended for [kool.dev](https://github.com/kool-dev/kool), but can fit other PHP use cases.

The images with Nginx include [`h5bp/server-configs-nginx`](https://github.com/h5bp/server-configs-nginx) with a hand picked set of configuration active by default. So if you want to change or add a new server configuration you can `include h5bp/...` as you see fit.

### Usage

Simplest example:

[![asciicast](https://asciinema.org/a/388121.svg)](https://asciinema.org/a/388121)

##### About `composer`

> All images currently ship out with Composer 2.x as the default version. If for some reason you still need to use Composer 1.x and cannot make the upgrade, we still ship a `composer1` in the images PATH as well, which is latest Composer 1.x version. Feel free to use it while you prepare to move to 2.0.

## Available Tags

The image built is [`kooldev/php`](https://hub.docker.com/r/kooldev/php/tags?page=1&ordering=last_updated) which has a bunch of tags available:

The default images use Alpine Linux. PHP 8.4 and 8.5 also offer Debian Bookworm variants. All maintained tags are published for `linux/amd64` and `linux/arm64`.

### 8.5

- [8.5](https://github.com/kool-dev/docker-php/blob/master/8.5/Dockerfile) and [8.5-prod](https://github.com/kool-dev/docker-php/blob/master/8.5-prod/Dockerfile)
- [8.5-nginx](https://github.com/kool-dev/docker-php/blob/master/8.5-nginx/Dockerfile) and [8.5-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.5-nginx-prod/Dockerfile)
- [8.5-node](https://github.com/kool-dev/docker-php/blob/master/8.5-node/Dockerfile)
- [8.5-debian](https://github.com/kool-dev/docker-php/blob/master/8.5-debian/Dockerfile) and [8.5-debian-prod](https://github.com/kool-dev/docker-php/blob/master/8.5-debian-prod/Dockerfile)
- [8.5-debian-nginx](https://github.com/kool-dev/docker-php/blob/master/8.5-debian-nginx/Dockerfile) and [8.5-debian-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.5-debian-nginx-prod/Dockerfile)

### 8.4

- [8.4](https://github.com/kool-dev/docker-php/blob/master/8.4/Dockerfile) and [8.4-prod](https://github.com/kool-dev/docker-php/blob/master/8.4-prod/Dockerfile)
- [8.4-nginx](https://github.com/kool-dev/docker-php/blob/master/8.4-nginx/Dockerfile) and [8.4-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.4-nginx-prod/Dockerfile)
- [8.4-node](https://github.com/kool-dev/docker-php/blob/master/8.4-node/Dockerfile)
- [8.4-debian](https://github.com/kool-dev/docker-php/blob/master/8.4-debian/Dockerfile) and [8.4-debian-prod](https://github.com/kool-dev/docker-php/blob/master/8.4-debian-prod/Dockerfile)
- [8.4-debian-nginx](https://github.com/kool-dev/docker-php/blob/master/8.4-debian-nginx/Dockerfile) and [8.4-debian-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.4-debian-nginx-prod/Dockerfile)

### 8.3

- [8.3](https://github.com/kool-dev/docker-php/blob/master/8.3/Dockerfile) and [8.3-prod](https://github.com/kool-dev/docker-php/blob/master/8.3-prod/Dockerfile)
- [8.3-nginx](https://github.com/kool-dev/docker-php/blob/master/8.3-nginx/Dockerfile) and [8.3-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.3-nginx-prod/Dockerfile)
- [8.3-node](https://github.com/kool-dev/docker-php/blob/master/8.3-node/Dockerfile)

### 8.2

- [8.2](https://github.com/kool-dev/docker-php/blob/master/8.2/Dockerfile) and [8.2-prod](https://github.com/kool-dev/docker-php/blob/master/8.2-prod/Dockerfile)
- [8.2-nginx](https://github.com/kool-dev/docker-php/blob/master/8.2-nginx/Dockerfile) and [8.2-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/8.2-nginx-prod/Dockerfile)
- [8.2-node](https://github.com/kool-dev/docker-php/blob/master/8.2-node/Dockerfile)

### Legacy versions

PHP 8.1, 8.0, and 7.4 are end-of-life upstream. Their tags remain on [Docker Hub](https://hub.docker.com/r/kooldev/php/tags), but are no longer built from this repository and receive no updates. Upgrade to a supported PHP version for new deployments.

## More flavours

We can always extend these images to suit them to our current use case. For example, we have a few extensions for specific use cases:

- [Oracle OCI8 database](https://github.com/kool-dev/docker-php-oci8)
- [MS SQL Server `sqlsrv` database](https://github.com/kool-dev/docker-php-sqlsrv)
- [Swoole](https://github.com/kool-dev/docker-php-swoole)

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
**PHP_FPM_PM** | `dynamic` | PHP-FPM process manager strategy
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
**NGINX_ENTRYPOINT_WORKER_PROCESSES_AUTOTUNE** | `true` | Enables auto-tuning of worker processes based on available CPU cores (container instead of host), to disable set it to empty string
**NGINX_HTTPS** | `false` | Enables the HTTPS server
**NGINX_LISTEN_HTTPS** | `443` | Port for the HTTPS server to listen
**NGINX_HTTPS_CERT** | `/kool/ssl/_.localhost.pem` | The path in the container for the SSL certificate file
**NGINX_HTTPS_CERT_KEY** | `/kool/ssl/_.localhost.key` | The path in the container for the SSL certificate key file

## Usage

With `docker run`:

```sh
docker run -it --rm kooldev/php:8.5 php -v
```

With environment variables:

```sh
docker run -it --rm -e ENABLE_XDEBUG=true kooldev/php:8.5 php -v
```

With `docker-compose.yml`:

```yaml
app:
  image: kooldev/php:8.5
  ports:
    - "9773:9773"
  volumes:
    - ".:/app:cached"
    - "$HOME/.ssh/id_rsa:/home/developer/.ssh/id_rsa:cached"
  environment:
    ASUSER: "${UID:-1000}"
```

## Contributing

### Update images with templates

You should change `fwd-template.json` for configuration and `template` folder for the actual base templates.

After any changes, we need to run `kool run template` to parse the templates and generate all versions folder/files.

### Testing and publishing

Run `bash scripts/test-image.sh 8.5` to test a locally built image (replace the tag for other variants). CI uses the same script for every image, building base images before their nginx and node variants so tests use the local base rather than a published tag.

Pull requests build and test without publishing or accessing secrets. Pushes to `master`, weekly scheduled runs, and manual runs on `master` also publish multi-architecture images, with base images published before derived images.

Repository secrets:

- `DOCKER_USERNAME` and `DOCKER_PASSWORD`: Docker Hub credentials for publishing images and syncing this README.
- `DISPATCH_TOKEN`: token with access to the downstream repositories and permission to send repository dispatch events (fine-grained tokens need Contents write). Without it, CI publishes images but warns and skips downstream builds.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
