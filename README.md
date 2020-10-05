![CI/CD](https://github.com/kool-dev/docker-php/workflows/CI/CD/badge.svg)

## Description

Minimal PHP Docker image focused on Laravel applications. It's use is intended for [kool.dev](https://github.com/kool-dev/kool), but can fit in any other PHP use-case.

## Available Tags

### 7.1

- [7.1](https://github.com/kool-dev/docker-php/blob/master/7.1/Dockerfile)
- [7.1-prod](https://github.com/kool-dev/docker-php/blob/master/7.1-prod/Dockerfile)
- [7.1-nginx](https://github.com/kool-dev/docker-php/blob/master/7.1-nginx/Dockerfile)
- [7.1-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.1-nginx-prod/Dockerfile)
- [7.1-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.1-wkhtmltopdf/Dockerfile)
- [7.1-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.1-wkhtmltopdf-prod/Dockerfile)
- [7.1-nginx-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.1-nginx-wkhtmltopdf/Dockerfile)
- [7.1-nginx-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.1-nginx-wkhtmltopdf-prod/Dockerfile)

### 7.2

- [7.2](https://github.com/kool-dev/docker-php/blob/master/7.2/Dockerfile)
- [7.2-prod](https://github.com/kool-dev/docker-php/blob/master/7.2-prod/Dockerfile)
- [7.2-nginx](https://github.com/kool-dev/docker-php/blob/master/7.2-nginx/Dockerfile)
- [7.2-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.2-nginx-prod/Dockerfile)
- [7.2-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.2-wkhtmltopdf/Dockerfile)
- [7.2-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.2-wkhtmltopdf-prod/Dockerfile)
- [7.2-nginx-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.2-nginx-wkhtmltopdf/Dockerfile)
- [7.2-nginx-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.2-nginx-wkhtmltopdf-prod/Dockerfile)

### 7.3

- [7.3](https://github.com/kool-dev/docker-php/blob/master/7.3/Dockerfile)
- [7.3-prod](https://github.com/kool-dev/docker-php/blob/master/7.3-prod/Dockerfile)
- [7.3-nginx](https://github.com/kool-dev/docker-php/blob/master/7.3-nginx/Dockerfile)
- [7.3-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.3-nginx-prod/Dockerfile)
- [7.3-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.3-wkhtmltopdf/Dockerfile)
- [7.3-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.3-wkhtmltopdf-prod/Dockerfile)
- [7.3-nginx-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.3-nginx-wkhtmltopdf/Dockerfile)
- [7.3-nginx-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.3-nginx-wkhtmltopdf-prod/Dockerfile)

### 7.4

- [7.4](https://github.com/kool-dev/docker-php/blob/master/7.4/Dockerfile)
- [7.4-prod](https://github.com/kool-dev/docker-php/blob/master/7.4-prod/Dockerfile)
- [7.4-nginx](https://github.com/kool-dev/docker-php/blob/master/7.4-nginx/Dockerfile)
- [7.4-nginx-prod](https://github.com/kool-dev/docker-php/blob/master/7.4-nginx-prod/Dockerfile)
- [7.4-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.4-wkhtmltopdf/Dockerfile)
- [7.4-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.4-wkhtmltopdf-prod/Dockerfile)
- [7.4-nginx-wkhtmltopdf](https://github.com/kool-dev/docker-php/blob/master/7.4-nginx-wkhtmltopdf/Dockerfile)
- [7.4-nginx-wkhtmltopdf-prod](https://github.com/kool-dev/docker-php/blob/master/7.4-nginx-wkhtmltopdf-prod/Dockerfile)

## Environment Variables

Variable | Description | Default Value
--- | --- | ---
**ASUSER** | Changes the user id that executes the commands | `-0`
**UID** | Changes the user id that executes the commands **(ignored if ASUSER is provided)** | `-0`
**COMPOSER_ALLOW_SUPERUSER** | Allows composer to run with super user | `1`
**COMPOSER_MEMORY_LIMIT** | Changes composer memory limit | `-1`
**ENABLE_XDEBUG** | Enables the Xdebug extension **(only prod versions)** | `false`
**PHP_MEMORY_LIMIT** | Changes PHP memory limit | `256M`
**PHP_MAX_INPUT_VARS** | Changes how many input variables may be accepted on PHP | `1000` 
**PHP_UPLOAD_MAX_FILESIZE** | Changes PHP maximum size of an uploaded file | `25M`
**PHP_POST_MAX_SIZE** | Changes PHP max size of post data allowed | `25M`
**PHP_MAX_EXECUTION_TIME** | Changes PHP maximum time is allowed to run a script | `30`
**PHP_FPM_LISTEN** | Changes the PORT address of the FastCGI requests | `9000`
**PHP_FPM_MAX_CHILDREN** | Changes the number of child processes to be used on FPM | `10`
**PHP_FPM_REQUEST_TERMINATE_TIMEOUT** | Changes FPM timeout to serve a single request | `60`

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

### Dependencies

- [fwd](https://github.com/fireworkweb/fwd#fireworkwebfwd)

You should change `fwd-template.json` and `template` folder.

After your changes, just run `fwd template` to compile the template and generate all version folder/files.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
