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

CI builds and tests all 28 variants once per architecture on native `ubuntu-24.04` (amd64) and `ubuntu-24.04-arm` (arm64) runners: 24 build/test groups. Only base builds pull their upstream PHP image fresh. Derived builds do not force-pull `kooldev/php`; the Docker driver keeps the fresh local base available to nginx/node builds. Before derived runtime tests, CI verifies that the local base still has its tested image ID and that its entire layer chain prefixes the derived image's layers. Tests use the build's immutable local image ID.

Pull requests, forks, and manual feature-branch runs never log in, stage images on Docker Hub, upload release metadata, publish stable images, or dispatch. Only trusted `master` runs (push, weekly schedule, or manual) stage the tested IDs as `kooldev/php:ci-php-RUN_ID-RUN_ATTEMPT-VARIANT-ARCH`. These temporary tags do not overwrite stable architecture tags. Staging tags remain in the registry; cleanup is not part of this workflow.

Each tested tag uploads its registry digest in a `php-RUN_ID-RUN_ATTEMPT-VARIANT-ARCH` artifact. The final publication job requires every build/test group to succeed and downloads only the current attempt's metadata. It validates all 28 tags, exactly amd64 and arm64 per tag, repository, run scope, and digest format before changing any stable tag. Stable manifests reference those recorded digests; publication does not rebuild images or use QEMU. Dispatch starts only after every stable manifest succeeds.

**Rerun the entire workflow**, not just failed jobs: a new attempt cannot reuse metadata from an earlier attempt. Missing metadata fails closed before publication. Stable-tag updates across 28 tags are not a registry transaction: a registry failure during publication can leave a partially promoted release, but never triggers downstream dispatch. Investigate and rerun the whole workflow to recover.

Run `python3 -m unittest discover -s scripts -p 'test_*.py' -v` for the mocked publication and workflow contracts. `python3 scripts/registry_roundtrip.py` exercises real staging and manifest publication against an ephemeral loopback registry with tiny synthetic images for both platforms; it verifies the registry config digests against the original local image exports. It never pushes to Docker Hub and is not a PHP runtime test. CI also runs this registry test, actionlint, and the real template generator before native builds.

PHP owns the rebuild schedule. After publication it notifies WordPress, SQL Server, and Swoole via `docker-php-updated`. Swoole notifies OCI8 only after all its images are published, so OCI8 does not race its Swoole parents or rebuild twice for the same PHP refresh. PHPQA is discontinued and no longer receives rebuild notifications. Downstream repositories have no separate cron schedules. Failed notifications must be investigated and retried manually; an accepted dispatch is not confirmation of downstream publication.

Repository or inherited organization secrets:

- `DOCKER_USERNAME` and `DOCKER_PASSWORD`: Docker Hub credentials for publishing images and syncing this README.
- Downstream dispatch uses `DISPATCH_TOKEN` when configured, otherwise the inherited `WORKFLOW_TOKEN`. The existing organization token normally avoids new credential setup; an optional dedicated `DISPATCH_TOKEN` can restrict access to the downstream repositories. The selected token needs permission to send repository dispatch events (fine-grained tokens need Contents write). Secret metadata does not establish token expiration or cross-repository permissions. If neither secret is available, the dispatch jobs fail visibly after images have been published.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
