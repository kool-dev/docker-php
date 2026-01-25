# PRD: CI/CD GitHub Action Refactor

## Introduction

Refactor the CI/CD GitHub Actions workflow to properly handle Docker image build dependencies. The current workflow is broken for Debian images (and potentially fragile for Alpine) because it doesn't correctly handle the dependency between base images and derived images (nginx, node) during multi-architecture builds.

The core problem: multi-arch builds require the `docker-container` buildx driver, which cannot access locally built images. This means derived images (nginx, node) must pull their base images from Docker Hub, requiring the base images to be pushed first.

## Goals

- Enable CI to run on PRs without pushing to Docker Hub (100% local builds)
- Ensure derived images (nginx, node) always build against the locally-built base image during testing
- Support multi-architecture builds (amd64 + arm64) for Docker Hub pushes
- Maintain proper build order: base images must be pushed before derived images
- Preserve all existing test coverage
- Keep downstream repository triggers functional
- Minimize redundant builds (don't rebuild base images unnecessarily)

## User Stories

### US-001: Local build and test for PRs ✅ COMPLETED
**Description:** As a contributor, I want PRs to build and test all images locally so I can validate my changes without pushing to Docker Hub.

**Acceptance Criteria:**
- [x] All builds use `docker` driver (can access local daemon)
- [x] Base images are built and loaded locally first
- [x] Derived images (nginx, node) find base images in local daemon (no Docker Hub pull)
- [x] All tests run against locally built images
- [x] No images are pushed on PR branches
- [x] CI passes for new images that don't exist on Docker Hub yet

### US-002: Multi-arch push with correct dependency order ✅ COMPLETED
**Description:** As a maintainer, I want master branch pushes to build and push multi-arch images in the correct order so derived images can pull their base from Docker Hub.

**Acceptance Criteria:**
- [x] Push jobs only run on master branch and correct repository
- [x] Push jobs use `docker-container` driver for multi-arch support
- [x] Base image push jobs complete before derived image push jobs start
- [x] Derived image builds can pull base from Docker Hub (just pushed)
- [x] All images pushed with platforms: linux/amd64,linux/arm64

### US-003: Alpine image builds ✅ COMPLETED
**Description:** As a maintainer, I want Alpine images (8.1-8.4, dev and prod variants) to build, test, and push correctly.

**Acceptance Criteria:**
- [x] Matrix covers versions: 8.1, 8.2, 8.3, 8.4
- [x] Each version builds both dev and prod variants in same job (no duplicate base builds)
- [x] Base, nginx, and node images all build and test locally per version
- [x] Base images push before nginx/node images (job dependency)
- [x] All existing tests preserved

### US-004: Debian image builds ✅ COMPLETED
**Description:** As a maintainer, I want Debian images (8.4, dev and prod variants) to build, test, and push correctly.

**Acceptance Criteria:**
- [x] Matrix covers types: "" (dev), "-prod"
- [x] Version: 8.4 only (for now)
- [x] Base images build and test locally
- [x] Nginx images build and test locally (using local base)
- [x] Base images push before nginx images (job dependency)
- [x] Debian-specific tests preserved (gosu, bash)
- [x] Supervisord test uses correct flag: `supervisord --version` (not `supervisord version`)

### US-005: Downstream triggers ✅ COMPLETED
**Description:** As a maintainer, I want downstream repositories to be triggered after all images are successfully pushed.

**Acceptance Criteria:**
- [x] Triggers only run on master branch and correct repository
- [x] Triggers wait for ALL push jobs to complete
- [x] Trigger: kool-dev/docker-wordpress
- [x] Trigger: kool-dev/docker-php-sqlsrv
- [x] Trigger: kool-dev/docker-php-swoole
- [x] Trigger: kool-dev/docker-phpqa

## Functional Requirements

### Infrastructure Setup (all jobs)

- FR-1: All jobs must use `actions/checkout@v4` to get source code
- FR-2: All jobs must use `docker/setup-qemu-action@v3` for multi-arch emulation
- FR-3: All jobs must use `docker/setup-buildx-action@v3` to configure buildx
- FR-4: Push jobs must use `docker/login-action@v3` with Docker Hub credentials (`DOCKER_USERNAME`, `DOCKER_PASSWORD` secrets)
- FR-5: Push jobs must have condition: `if: github.ref == 'refs/heads/master' && github.repository == 'kool-dev/docker-php'`

### Job Structure

- FR-6: Create `build-test-alpine` job (matrix: versions 8.1-8.4) that builds and tests ALL images for each version:
  - Build base dev → test
  - Build base prod → test
  - Build nginx dev (uses local base dev) → test
  - Build nginx prod (uses local base prod) → test
  - Build node (uses local base dev) → test
- FR-7: Create `build-test-debian` job (matrix: types dev/prod) that builds and tests base + nginx locally
- FR-8: Create `push-alpine-base` job (master only, needs: build-test-alpine, matrix: 8.1-8.4 × dev/prod) that pushes base images multi-arch
- FR-9: Create `push-alpine-nginx` job (master only, needs: push-alpine-base, matrix: 8.1-8.4 × dev/prod) that pushes nginx images multi-arch
- FR-10: Create `push-alpine-node` job (master only, needs: push-alpine-base, matrix: 8.1-8.4) that pushes node images multi-arch
- FR-11: Create `push-debian-base` job (master only, needs: build-test-debian, matrix: dev/prod) that pushes base images multi-arch
- FR-12: Create `push-debian-nginx` job (master only, needs: push-debian-base, matrix: dev/prod) that pushes nginx images multi-arch
- FR-13: Create trigger jobs (master only, needs: all push jobs) for downstream repositories

### Build Configuration

- FR-14: Test jobs must use `docker` buildx driver with `driver: docker` (enables local image access)
- FR-15: Push jobs must use default `docker-container` buildx driver (enables multi-arch)
- FR-16: Test jobs must use `load: true` to load images into local daemon
- FR-17: Push jobs must use `push: true` and `platforms: linux/amd64,linux/arm64`
- FR-18: Push jobs must NOT use `load: true` (incompatible with multi-platform)

### Tests to Preserve

- FR-19: Basic tests: `php -v`, `composer -V`, `composer1 -V`, ASUSER user switching, readline module
- FR-20: Dockerize tests: version check, template rendering with environment variable
- FR-21: PHP extension tests: bcmath, gd, intl, pdo_mysql, pdo_pgsql, redis, zip, mbstring, ldap
- FR-22: Production tests: OPcache enabled, xdebug NOT loadable even with ENABLE_XDEBUG=true
- FR-23: Development tests: pcov available, xdebug loadable with ENABLE_XDEBUG=true
- FR-24: Nginx tests: `nginx -v`, `nginx -T`, `supervisord --version`
- FR-25: Node tests: `node -v`, `npm -v`, `yarn -v`
- FR-26: Debian-specific tests: `gosu --version`, uid switching test with ASUSER

## Non-Goals

- No changes to Dockerfile content (only CI/CD workflow)
- No changes to image tags or naming conventions
- No support for pushing from PR branches
- No build caching strategy (can be added in future PR)
- No changes to the template system (blade templates)

## Technical Considerations

### Buildx Driver Behavior

| Driver | Local Images | Multi-arch | Use Case |
|--------|--------------|------------|----------|
| `docker` | Yes (daemon access) | No | Local build + test |
| `docker-container` | No (isolated) | Yes | Multi-arch push |

### Job Dependencies (master branch)

```
build-test-alpine ──────► push-alpine-base ─────┬──► push-alpine-nginx
     (4 jobs)                (8 jobs)           │        (8 jobs)
                                                │
                                                └──► push-alpine-node
                                                          (4 jobs)

build-test-debian ──────► push-debian-base ─────────► push-debian-nginx
     (2 jobs)                 (2 jobs)                     (2 jobs)

All push jobs ──────────► trigger-wordpress
                          trigger-extended
```

**Note on matrix dependencies:** When `push-alpine-nginx` depends on `push-alpine-base`, GitHub Actions waits for ALL matrix entries of push-alpine-base to complete before starting ANY matrix entry of push-alpine-nginx. This is a GitHub Actions limitation (no per-matrix-entry dependencies). This is acceptable as it guarantees all base images are available.

### Matrix Definitions

**Alpine test (consolidated - one job per version):**
```yaml
matrix:
  version: ["8.1", "8.2", "8.3", "8.4"]
# Each job builds: base dev, base prod, nginx dev, nginx prod, node
```

**Alpine base push:**
```yaml
matrix:
  version: ["8.1", "8.2", "8.3", "8.4"]
  type: ["", "-prod"]
```

**Alpine nginx push:**
```yaml
matrix:
  version: ["8.1", "8.2", "8.3", "8.4"]
  type: ["", "-prod"]
```

**Alpine node push:**
```yaml
matrix:
  version: ["8.1", "8.2", "8.3", "8.4"]
# Node only has dev variant (no -prod)
```

**Debian test:**
```yaml
matrix:
  type: ["", "-prod"]
# Version fixed at 8.4
```

**Debian base/nginx push:**
```yaml
matrix:
  type: ["", "-prod"]
# Version fixed at 8.4
```

### Build Overhead

Each image gets built multiple times:
1. **Test job:** Single-arch local build (fast, for testing)
2. **Push job:** Multi-arch rebuild (slower, for production)

This is unavoidable because the `docker-container` driver (required for multi-arch) cannot access locally built images. Build caching can mitigate this in a future PR.

## Success Metrics

- CI passes on the debian branch (currently broken)
- CI passes for PRs without any Docker Hub access
- All 4 Debian images successfully pushed to Docker Hub from master
- All Alpine images continue to work as before
- Downstream triggers fire successfully after pushes complete
- No duplicate base image builds within test jobs (consolidated approach)

## Open Questions

- Should we add build caching to speed up CI? (deferred to future PR)
- Should Debian support more PHP versions (8.1-8.3)? (out of scope for this PR)
- Should we add a "dry-run" push option for testing? (out of scope)
