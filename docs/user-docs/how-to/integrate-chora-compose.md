# How to Integrate chora-compose with Your chora-base Project

**Audience**: Python developers using chora-base
**Time**: 30-60 minutes
**Difficulty**: Intermediate

---

## Overview

This guide walks you through integrating [chora-compose](https://github.com/liminalcommons/chora-compose) - a Docker Compose-based orchestration system - with your chora-base Python project. You'll learn how to set up containerized development environments with databases, caches, and other services.

**What You'll Build**:
- Docker Compose configuration for your project
- Containerized application with service dependencies
- Development workflow with live code reloading
- Environment configuration management

**Prerequisites**:
- Existing chora-base project (see [SAP-003](../../skilled-awareness/project-bootstrap/))
- Docker Desktop 4.0+ installed
- Basic Docker and Docker Compose knowledge

---

## Quick Start (5 Minutes)

### 1. Create docker-compose.yml

In your project root:

```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/workspace:delegated
    environment:
      - PYTHONUNBUFFERED=1
    ports:
      - "8000:8000"
    command: python -m your_module.server

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres-data:
```

### 2. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "your_module.server"]
```

### 3. Start Services

```bash
docker compose up -d
```

### 4. Verify

```bash
# Check services are running
docker compose ps

# View logs
docker compose logs -f app

# Test your application
curl http://localhost:8000
```

**Done!** Your application is now running in Docker with a PostgreSQL database.

---

## Detailed Setup

### Step 1: Plan Your Services

Identify what services your project needs:

**Common Services**:
- **Database**: PostgreSQL, MySQL, MongoDB
- **Cache**: Redis, Memcached
- **Message Queue**: RabbitMQ, Redis
- **Search**: Elasticsearch, Meilisearch
- **Monitoring**: Prometheus, Grafana

**Example Decision Tree**:
```
Does your project need data persistence?
├─ Yes: Add database service (PostgreSQL recommended)
└─ No: Skip database

Does your project need caching?
├─ Yes: Add Redis
└─ No: Skip cache

Does your project have long-running tasks?
├─ Yes: Add message queue (Redis + Celery)
└─ No: Skip queue
```

### Step 2: Write docker-compose.yml

**Basic Template**:

```yaml
version: '3.8'

services:
  # Your application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ${PROJECT_NAME:-myproject}-app
    volumes:
      # Source code (live reload)
      - .:/workspace:delegated
      # Dependency cache
      - pip-cache:/root/.cache/pip
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONPATH=/workspace
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
    env_file:
      - .env.local
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    ports:
      - "${APP_PORT:-8000}:8000"
    command: python -m your_module.server

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    container_name: ${PROJECT_NAME:-myproject}-db
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-myapp}
      POSTGRES_USER: ${POSTGRES_USER:-dev}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dev}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USER:-dev}"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  postgres-data:
  pip-cache:

networks:
  app-network:
    driver: bridge
```

**Customization**:
- Replace `your_module.server` with your actual module path
- Add more services as needed (see patterns below)
- Adjust ports if you have conflicts

### Step 3: Create Dockerfile

**Basic Dockerfile**:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package in development mode
RUN if [ -f pyproject.toml ]; then pip install -e .; fi

# Default command
CMD ["python", "-m", "your_module.server"]
```

**Optimized Dockerfile** (faster rebuilds):

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /workspace
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /workspace
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "-m", "your_module.server"]
```

### Step 4: Configure Environment

**Create `.env.local`** (gitignored - for local development):

```bash
# .env.local - DO NOT COMMIT

# Project
PROJECT_NAME=myproject

# Application
DEBUG=true
LOG_LEVEL=DEBUG
APP_PORT=8000

# Database
POSTGRES_DB=myapp_dev
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev_change_me
POSTGRES_PORT=5432

# Redis (if using)
REDIS_URL=redis://redis:6379

# API Keys
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=your-key
```

**Create `.env.defaults`** (committed - safe defaults):

```bash
# .env.defaults - Safe to commit

# Project
PROJECT_NAME=myproject

# Application
DEBUG=false
LOG_LEVEL=INFO
APP_PORT=8000

# Database
POSTGRES_DB=myapp
POSTGRES_USER=user
POSTGRES_PORT=5432

# Feature Flags
ENABLE_CACHING=true
```

**Update `.gitignore`**:

```gitignore
# Environment
.env.local
.env.*.local

# Docker
docker-compose.override.yml
```

### Step 5: Test Your Setup

```bash
# Build and start services
docker compose up -d --build

# Check service status
docker compose ps

# View logs
docker compose logs -f

# Test database connection
docker compose exec db psql -U dev -d myapp_dev -c "SELECT version();"

# Exec into app container
docker compose exec app bash

# Run tests (if applicable)
docker compose exec app pytest tests/
```

**Expected Output**:
```
NAME                IMAGE                   STATUS      PORTS
myproject-app       myproject-app:latest    Up          0.0.0.0:8000->8000/tcp
myproject-db        postgres:15-alpine      Up (healthy) 0.0.0.0:5432->5432/tcp
```

---

## Common Patterns

### Pattern 1: Adding Redis Cache

**docker-compose.yml** (add service):

```yaml
services:
  # ... existing app and db services

  redis:
    image: redis:7-alpine
    container_name: ${PROJECT_NAME:-myproject}-redis
    volumes:
      - redis-data:/data
    networks:
      - app-network
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3

volumes:
  redis-data:  # Add to volumes section
```

**Update app service**:

```yaml
services:
  app:
    # ...
    depends_on:
      - db
      - redis  # Add dependency
    environment:
      - REDIS_URL=redis://redis:6379
```

### Pattern 2: Development with Hot Reload

**For Flask**:

```yaml
services:
  app:
    # ...
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    command: flask run --host=0.0.0.0 --reload
```

**For FastAPI**:

```yaml
services:
  app:
    # ...
    command: uvicorn your_module.server:app --host 0.0.0.0 --reload
```

**For Django**:

```yaml
services:
  app:
    # ...
    command: python manage.py runserver 0.0.0.0:8000
```

### Pattern 3: Running Tests in Docker

**docker-compose.yml** (add test service):

```yaml
services:
  test:
    build: .
    volumes:
      - .:/workspace:delegated
    depends_on:
      test-db:
        condition: service_healthy
    environment:
      - TESTING=true
      - DATABASE_URL=postgresql://test:test@test-db:5432/test_db
    command: pytest tests/ -v

  test-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    tmpfs:
      - /var/lib/postgresql/data  # In-memory for speed
```

**Run tests**:

```bash
docker compose run --rm test
```

### Pattern 4: Hybrid Development (Local Python + Docker Services)

**docker-compose.yml** (services only):

```yaml
version: '3.8'

services:
  # No app service - run Python locally

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"  # Expose to host
    # ... rest of db config

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"  # Expose to host
```

**Local Python**:

```bash
# Start Docker services
docker compose up -d

# Run Python locally
python -m your_module.server

# Use localhost in connection strings
export DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp
```

---

## Troubleshooting

### Problem: "Port already allocated"

**Symptom**: `Error: bind: address already in use`

**Solution**:

```bash
# Find what's using the port
lsof -i :5432  # Replace 5432 with your port

# Kill the process or change port in docker-compose.yml
ports:
  - "5433:5432"  # Use different external port
```

### Problem: Code changes not reflected

**Symptom**: Edit code, but container still runs old code

**Solution**:

```bash
# Ensure volume mount exists
docker compose config | grep volumes

# Restart container
docker compose restart app

# If Dockerfile changed, rebuild
docker compose up -d --build app
```

### Problem: "Connection refused" to database

**Symptom**: App can't connect to database

**Solution**:

```yaml
# Use service name, not localhost
environment:
  - DATABASE_URL=postgresql://user:pass@db:5432/myapp  # ✅ db (service name)
  # Not: postgresql://user:pass@localhost:5432/myapp  # ❌ localhost
```

### Problem: Slow performance on macOS/Windows

**Symptom**: Container very slow, high CPU usage

**Solution**:

```yaml
services:
  app:
    volumes:
      - .:/workspace:delegated  # Add :delegated
      - /workspace/node_modules  # Exclude if using Node.js
      - /workspace/.venv         # Exclude Python venv
```

---

## Next Steps

### Learn More

- **[SAP-017: chora-compose Integration](../../skilled-awareness/chora-compose-integration/)** - Comprehensive integration guide
- **[SAP-018: chora-compose Meta](../../skilled-awareness/chora-compose-meta/)** - Deep dive into chora-compose architecture
- **[chora-compose Repository](https://github.com/liminalcommons/chora-compose)** - Pre-configured stacks and templates

### Advanced Topics

- **Multi-stage builds** for smaller images
- **Docker secrets** for production
- **CI/CD integration** with Docker Compose
- **Production deployment** patterns
- **Monitoring and logging** with Prometheus/Grafana

---

## Related Documentation

**SAP Documentation**:
- [SAP-017: chora-compose Integration](../../skilled-awareness/chora-compose-integration/) - Full integration guide
- [SAP-003: Project Bootstrap](../../skilled-awareness/project-bootstrap/) - chora-base project structure
- [SAP-014: MCP Server Development](../../skilled-awareness/mcp-server-development/) - MCP server patterns

**External Resources**:
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Official docs
- [chora-compose Repository](https://github.com/liminalcommons/chora-compose) - Pre-configured stacks

---

**Version**: 1.0.0
**Last Updated**: 2025-10-29
