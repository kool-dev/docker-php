# From Alpine to Debian: Migration Guide

This document outlines the key differences between the Alpine and Debian variants of the kooldev/php Docker images.

## Quick Comparison

| Feature | Alpine | Debian |
|---------|--------|--------|
| Base Image | `php:8.x-fpm-alpine` | `php:8.x-fpm` (Debian) |
| Image Size | Smaller (~150MB) | Larger (~400MB) |
| Package Manager | `apk` | `apt-get` |
| Shell | `sh` (BusyBox) | `bash` |
| Privilege Drop | `su-exec` | `gosu` |
| Supervisord | ochinchina/supervisord (Go static binary) | Official supervisor package (Python) |
| Architecture | amd64 only (nginx variants) | amd64 + arm64 |
| glibc | musl libc | glibc |

## When to Use Debian

Choose the Debian variant when:

- **ARM64/Apple Silicon support is needed** - The Debian variant has native multi-arch support
- **Compatibility issues with Alpine** - Some PHP extensions or native libraries may have issues with musl libc
- **Debugging needs** - Debian includes more debugging tools out of the box
- **Familiarity** - Teams more familiar with Debian/Ubuntu environments

## When to Use Alpine

Choose the Alpine variant when:

- **Minimal image size is critical** - Alpine images are significantly smaller
- **Security through minimalism** - Smaller attack surface with fewer packages
- **amd64-only deployments** - No need for ARM64 support

## Key Differences in Detail

### 1. Supervisord Implementation

**Alpine** uses [ochinchina/supervisord](https://github.com/ochinchina/supervisord), a Go-based reimplementation:

```ini
# Alpine supervisor.conf
[program:nginx]
depends_on = php-fpm
command = nginx -g "daemon off;"
stopasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout

[program:php-fpm]
command = php-fpm
stopasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
```

**Debian** uses the official Python-based supervisord package:

```ini
# Debian supervisor.conf
[supervisord]
nodaemon=true
user=root
logfile=/dev/null
logfile_maxbytes=0
pidfile=/run/supervisord.pid

[program:php-fpm]
command=php-fpm
priority=10
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:nginx]
command=nginx -g "daemon off;"
priority=20
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```

**Key differences:**
- Alpine uses `depends_on` for process ordering
- Debian uses `priority` (lower number starts first)
- Debian requires a `[supervisord]` section with `nodaemon=true`
- Debian needs `stdout_logfile_maxbytes=0` to disable log rotation for stdout/stderr

### 2. Entrypoint Script

**Alpine** uses `sh` shell with `su-exec`:

```bash
#!/bin/sh
# ...
exec su-exec kool "$@"
```

**Debian** uses `bash` with `gosu`:

```bash
#!/bin/bash
# ...
exec gosu kool "$@"
```

### 3. Package Installation

**Alpine:**
```dockerfile
RUN apk add --no-cache nginx \
    && apk add --no-cache --virtual .build-deps ... \
    && apk del .build-deps
```

**Debian:**
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*
```

### 4. nginx Directory Structure

**Alpine:**
```dockerfile
chmod 770 /var/lib/nginx/tmp
```

**Debian:**
```dockerfile
chmod 770 /var/lib/nginx
```

## Migration Steps

To migrate from Alpine to Debian:

1. **Update your image tag:**
   ```yaml
   # docker-compose.yml
   # From:
   image: kooldev/php:8.4-nginx
   # To:
   image: kooldev/php:8.4-debian-nginx
   ```

2. **Custom supervisor configs:** If you've customized the supervisor configuration, update to use `priority` instead of `depends_on`

3. **Shell scripts:** Update any scripts that rely on Alpine-specific paths or BusyBox commands

4. **Test thoroughly:** The glibc vs musl difference can cause subtle behavior changes in some applications

## Available Debian Image Tags

- `kooldev/php:8.4-debian` - Base FPM image
- `kooldev/php:8.4-debian-prod` - Production FPM image (no dev tools)
- `kooldev/php:8.4-debian-nginx` - FPM + Nginx with supervisord
- `kooldev/php:8.4-debian-nginx-prod` - Production FPM + Nginx
