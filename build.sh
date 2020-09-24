#! /bin/bash

docker build --pull -t kooldev/php:7.1 7.1
docker build --pull -t kooldev/php:7.1-prod 7.1-prod
docker build -t kooldev/php:7.1-wkhtmltopdf 7.1-wkhtmltopdf
docker build -t kooldev/php:7.1-wkhtmltopdf-prod 7.1-wkhtmltopdf-prod
docker build --pull -t kooldev/php:7.2 7.2
docker build --pull -t kooldev/php:7.2-prod 7.2-prod
docker build -t kooldev/php:7.2-wkhtmltopdf 7.2-wkhtmltopdf
docker build -t kooldev/php:7.2-wkhtmltopdf-prod 7.2-wkhtmltopdf-prod
docker build --pull -t kooldev/php:7.3 7.3
docker build --pull -t kooldev/php:7.3-prod 7.3-prod
docker build -t kooldev/php:7.3-wkhtmltopdf 7.3-wkhtmltopdf
docker build -t kooldev/php:7.3-wkhtmltopdf-prod 7.3-wkhtmltopdf-prod
docker build --pull -t kooldev/php:7.4 7.4
docker build --pull -t kooldev/php:7.4-prod 7.4-prod
docker build -t kooldev/php:7.4-wkhtmltopdf 7.4-wkhtmltopdf
docker build -t kooldev/php:7.4-wkhtmltopdf-prod 7.4-wkhtmltopdf-prod
docker build -t kooldev/php:7.4-nginx 7.4-nginx
docker build -t kooldev/php:7.4-nginx-prod 7.4-nginx-prod
docker build -t kooldev/php:7.4-nginx-wkhtmltopdf 7.4-nginx-wkhtmltopdf
docker build -t kooldev/php:7.4-nginx-wkhtmltopdf-prod 7.4-nginx-wkhtmltopdf-prod