# Docker Basics for Chora-Base

**Audience**: Developers using Docker with chora-base
**Prerequisites**: Docker installed
**Related**: [SAP-011: Docker Operations](../../skilled-awareness/docker-operations/)

---

## Quick Start

```bash
# Build image
docker build -t myproject:latest .

# Run container
docker run -p 8000:8000 myproject:latest

# Run with volume mount (for development)
docker run -v $(pwd):/app myproject:latest pytest
```

---

## Dockerfile Overview

Chora-base projects include a multi-stage Dockerfile:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ ./src/
CMD ["python", "-m", "myproject"]
```

---

## Common Docker Commands

### Build and Run

```bash
# Build
docker build -t myproject:latest .

# Run interactively
docker run -it myproject:latest /bin/bash

# Run with environment variables
docker run -e API_KEY=secret myproject:latest

# Run with port mapping
docker run -p 8000:8000 myproject:latest
```

### Development Workflow

```bash
# Mount source code (live reload)
docker run -v $(pwd)/src:/app/src myproject:latest

# Run tests in container
docker run myproject:latest pytest

# Run with Docker Compose
docker-compose up
```

### Debugging

```bash
# View logs
docker logs <container-id>

# Execute command in running container
docker exec -it <container-id> /bin/bash

# Inspect container
docker inspect <container-id>
```

---

## Docker Compose

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
    environment:
      - DEBUG=true
    depends_on:
      - postgres

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: dev
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Usage**:
```bash
docker-compose up          # Start services
docker-compose up -d       # Start in background
docker-compose down        # Stop services
docker-compose logs -f app # Follow logs
```

---

## Best Practices

1. **Use .dockerignore**:
```
__pycache__
*.pyc
.git
.venv
htmlcov/
.coverage
```

2. **Multi-stage builds** (reduce image size)
3. **Layer caching** (order commands from least to most frequently changing)
4. **Non-root user** (security)
5. **Health checks**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

---

## Related Documentation

- [SAP-011: Docker Operations](../../skilled-awareness/docker-operations/)
- [SAP-017: chora-compose Integration](../../skilled-awareness/chora-compose-integration/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: 2025-10-29
