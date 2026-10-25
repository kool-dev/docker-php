#!/usr/bin/env bash
set -euo pipefail

tag=${1:?Usage: test-image.sh TAG}
image="kooldev/php:$tag"

run() {
    docker run --rm "$image" "$@"
}

run php -v
run composer -V
run composer1 -V
for command in php composer composer1; do
    docker run --rm -e ASUSER=1000 "$image" "$command" --version
done
test "$(docker run --rm -e ASUSER=1000 "$image" id -u)" = 1000

run dockerize --version
run sh -c 'echo "{{ .Env.TEST_VAR }}" > /tmp/test.tmpl; TEST_VAR=hello dockerize -template /tmp/test.tmpl:/tmp/test.out; test "$(cat /tmp/test.out)" = hello'
# The entrypoint runs dockerize as root, so only root may own it; and the
# release tarball's LICENSE/README.md must not be left behind in /app.
test "$(run stat -c %u:%g /usr/local/bin/dockerize)" = 0:0
run sh -c 'test ! -e /app/LICENSE && test ! -e /app/README.md'

# Read the module list once, and match whole names (e.g. zip, not gzip).
modules=$(run php -m)
for extension in readline bcmath gd intl pdo_mysql pdo_pgsql redis zip mbstring ldap; do
    grep -Fxi "$extension" <<< "$modules"
done

xdebug_modules=$(docker run --rm -e ENABLE_XDEBUG=true "$image" php -m)
if [[ "$tag" == *-prod ]]; then
    grep -Fxi 'Zend OPcache' <<< "$modules"
    if grep -Fxi xdebug <<< "$xdebug_modules"; then
        echo "ERROR: xdebug must not be available in production" >&2
        exit 1
    fi
else
    grep -Fxi pcov <<< "$modules"
    grep -Fxi xdebug <<< "$xdebug_modules"
    if grep -Fxi xdebug <<< "$modules"; then
        echo "ERROR: xdebug must be disabled by default" >&2
        exit 1
    fi
fi

if [[ "$tag" == *-debian* ]]; then
    run gosu --version
    run bash -c 'test -n "$BASH_VERSION"'
fi

if [[ "$tag" == *-nginx* ]]; then
    run nginx -v
    run nginx -T
    run supervisord --version
fi

if [[ "$tag" == *-node ]]; then
    run node -v
    run npm -v
    run yarn -v
fi
