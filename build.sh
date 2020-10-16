#! /bin/bash

docker build --pull -t kooldev/php:7.1 7.1
docker build --pull -t kooldev/php:7.1-prod 7.1-prod
docker build -t kooldev/php:7.1-nginx 7.1-nginx
docker build -t kooldev/php:7.1-nginx-prod 7.1-nginx-prod
docker build -t kooldev/php:7.1-full 7.1-full
docker build -t kooldev/php:7.1-full-prod 7.1-full-prod

docker build --pull -t kooldev/php:7.2 7.2
docker build --pull -t kooldev/php:7.2-prod 7.2-prod
docker build -t kooldev/php:7.2-nginx 7.2-nginx
docker build -t kooldev/php:7.2-nginx-prod 7.2-nginx-prod
docker build -t kooldev/php:7.2-full 7.2-full
docker build -t kooldev/php:7.2-full-prod 7.2-full-prod

docker build --pull -t kooldev/php:7.3 7.3
docker build --pull -t kooldev/php:7.3-prod 7.3-prod
docker build -t kooldev/php:7.3-nginx 7.3-nginx
docker build -t kooldev/php:7.3-nginx-prod 7.3-nginx-prod
docker build -t kooldev/php:7.3-full 7.3-full
docker build -t kooldev/php:7.3-full-prod 7.3-full-prod

docker build --pull -t kooldev/php:7.4 7.4
docker build --pull -t kooldev/php:7.4-prod 7.4-prod
docker build -t kooldev/php:7.4-nginx 7.4-nginx
docker build -t kooldev/php:7.4-nginx-prod 7.4-nginx-prod
