# From Alpine to Debian: Migration Guide

This document outlines the key differences between the Alpine and Debian variants of the kooldev/php Docker images.

## Quick Comparison

| Feature | Alpine | Debian |
|---------|--------|--------|
| Base Image | `php:8.x-fpm-alpine` | `php:8.x-fpm-bookworm` (Debian 12 stable) |
| Image Size | Smaller (~150MB) | Larger (~400MB) |
| Package Manager | `apk` | `apt-get` |
| Shell | `sh` (BusyBox) | `bash` |
| Privilege Drop | `su-exec` | `gosu` |
| Supervisord | Python supervisor (Alpine package) | Python supervisor (Debian package) |
| Architecture | amd64 + arm64 | amd64 + arm64 |
| glibc | musl libc | glibc |

## When to Use Debian

Choose the Debian variant when:

- **Compatibility issues with Alpine** - Some PHP extensions or native libraries may have issues with musl libc
- **Debugging needs** - Debian includes more debugging tools out of the box
- **Familiarity** - Teams more familiar with Debian/Ubuntu environments
- **Native library compatibility** - Some C libraries behave differently with glibc vs musl

## When to Use Alpine

Choose the Alpine variant when:

- **Minimal image size is critical** - Alpine images are significantly smaller
- **Security through minimalism** - Smaller attack surface with fewer packages
- **musl libc is acceptable** - Your application has no compatibility issues with musl

**Note:** Both Alpine and Debian variants now support multi-arch (amd64 + arm64).

## Key Differences in Detail

### 1. Supervisord Implementation

Both **Alpine** and **Debian** now use the official Python-based supervisord package (installed via `apk add supervisor` and `apt-get install supervisor` respectively). The configuration format is identical:

```ini
# supervisor.conf (both Alpine and Debian)
[supervisord]
logfile=/dev/stdout
logfile_maxbytes=0
pidfile=/run/supervisord.pid
nodaemon=true

[program:php-fpm]
command = php-fpm
priority = 10
autorestart = true
stopasgroup = true
killasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
stderr_logfile_maxbytes = 0
stdout_logfile_maxbytes = 0

[program:nginx]
command = nginx -g "daemon off;"
priority = 20
autorestart = true
stopasgroup = true
killasgroup = true
stderr_logfile = /dev/stderr
stdout_logfile = /dev/stdout
stderr_logfile_maxbytes = 0
stdout_logfile_maxbytes = 0
```

**Key configuration points:**
- `priority` controls startup order (lower number starts first)
- `nodaemon=true` keeps supervisord in foreground
- `stdout_logfile_maxbytes=0` disables log rotation for stdout/stderr

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

2. **Shell scripts:** Update any scripts that use:
   - `su-exec` → `gosu`
   - BusyBox-specific commands → standard GNU coreutils
   - `sh` shebang → `bash` shebang (if using bash features)

3. **Test thoroughly:** The glibc vs musl difference can cause subtle behavior changes in some applications

**Note:** Supervisor configuration format is now identical between Alpine and Debian, so no changes needed for custom supervisor configs.

## Available Debian Image Tags

- `kooldev/php:8.4-debian` - Base FPM image
- `kooldev/php:8.4-debian-prod` - Production FPM image (no dev tools)
- `kooldev/php:8.4-debian-nginx` - FPM + Nginx with supervisord
- `kooldev/php:8.4-debian-nginx-prod` - Production FPM + Nginx
