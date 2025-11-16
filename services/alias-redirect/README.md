# SAP Alias Redirect Service

HTTP redirect and API service for legacy SAP-XXX identifier resolution to modern `chora.domain.capability` namespaces.

## Overview

This service provides backward compatibility for legacy SAP-XXX identifiers during the 6-month sunset period (ending 2026-06-01). It offers:

- **HTTP 301 Redirects**: `/{SAP-ID}` → modern namespace documentation
- **REST API**: `/api/v1/resolve/{SAP-ID}` → JSON response with namespace
- **Deprecation Warnings**: All responses include sunset timeline
- **Health Monitoring**: `/health` endpoint for uptime checks

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app:app --reload --port 8000

# Test service
curl http://localhost:8000/api/v1/resolve/SAP-015
```

### Docker Deployment

```bash
# Build and run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop service
docker-compose down
```

### Production Deployment

```bash
# Build image
docker build -t sap-alias-redirect:1.0.0 .

# Run container
docker run -d \
    --name sap-alias-redirect \
    -p 8000:8000 \
    -v $(pwd)/../../capabilities/alias-mapping.json:/app/capabilities/alias-mapping.json:ro \
    sap-alias-redirect:1.0.0
```

## API Endpoints

### Root - Service Info

```bash
GET /

# Response
{
  "service": "SAP Alias Redirect Service",
  "version": "1.0.0",
  "status": "active",
  "deprecation_notice": "...",
  "sunset_date": "2026-06-01",
  "days_until_sunset": 198,
  "total_aliases": 45,
  "endpoints": {...}
}
```

### Health Check

```bash
GET /health

# Response
{
  "status": "healthy",
  "aliases_loaded": 45,
  "timestamp": "2025-11-15T22:30:00"
}
```

### List All Aliases

```bash
GET /api/v1/aliases

# Response
{
  "SAP-000": {
    "sap_id": "SAP-000",
    "namespace": "chora.infrastructure.sap_framework",
    "status": "deprecated",
    "sunset_date": "2026-06-01",
    "deprecated": true,
    "days_until_sunset": 198
  },
  "SAP-001": {...},
  ...
}
```

### Resolve Single Alias

```bash
GET /api/v1/resolve/SAP-015

# Response
{
  "sap_id": "SAP-015",
  "namespace": "chora.awareness.task_tracking",
  "status": "deprecated",
  "sunset_date": "2026-06-01",
  "deprecated": true,
  "days_until_sunset": 198,
  "deprecation_warning": "ℹ️ NOTICE: Legacy SAP-XXX identifiers are deprecated...",
  "docs_url": "https://github.com/chora-base/chora-base/blob/main/docs/skilled-awareness/task-tracking/",
  "migration_guide_url": "https://github.com/chora-base/chora-base/blob/main/docs/ontology/migration-guide.md"
}
```

### HTTP Redirect

```bash
GET /SAP-015

# Response: 301 Permanent Redirect
# Location: https://github.com/chora-base/chora-base/blob/main/docs/skilled-awareness/task-tracking/
# Headers:
#   X-Deprecated: true
#   X-Sunset-Date: 2026-06-01
#   X-Days-Until-Sunset: 198
#   X-Modern-Namespace: chora.awareness.task_tracking
#   X-Deprecation-Warning: ℹ️ NOTICE: Legacy SAP-XXX identifiers are deprecated...
#   X-Migration-Guide: https://github.com/chora-base/chora-base/blob/main/docs/ontology/migration-guide.md
```

## Deprecation Timeline

| Phase | Date Range | Warning Level | Message |
|-------|------------|---------------|---------|
| **Active Deprecation** | 2025-11-15 - 2026-03-01 | ℹ️ NOTICE | "Legacy SAP-XXX identifiers are deprecated and will be sunset on 2026-06-01" |
| **Critical Warning** | 2026-03-01 - 2026-05-01 | ⚠️ WARNING | "Legacy SAP-XXX identifiers will be sunset in X days" |
| **Final Warning** | 2026-05-01 - 2026-06-01 | ⚠️ CRITICAL | "Legacy SAP-XXX identifiers will be sunset in X days. Migrate immediately" |
| **Sunset** | 2026-06-01+ | ⚠️ DEPRECATED | "Legacy SAP-XXX identifiers are no longer supported" |

## Client Integration

### Python

```python
import requests

# Resolve alias
response = requests.get("http://localhost:8000/api/v1/resolve/SAP-015")
data = response.json()

namespace = data["namespace"]  # "chora.awareness.task_tracking"
docs_url = data["docs_url"]
warning = data["deprecation_warning"]

print(f"⚠️ {warning}")
print(f"Modern namespace: {namespace}")
print(f"Documentation: {docs_url}")
```

### JavaScript

```javascript
// Resolve alias
fetch('http://localhost:8000/api/v1/resolve/SAP-015')
  .then(res => res.json())
  .then(data => {
    console.warn(data.deprecation_warning);
    console.log(`Modern namespace: ${data.namespace}`);
    console.log(`Documentation: ${data.docs_url}`);
  });
```

### Bash/cURL

```bash
# Resolve alias
curl -s http://localhost:8000/api/v1/resolve/SAP-015 | jq '.'

# Follow redirect
curl -L http://localhost:8000/SAP-015

# Check headers
curl -I http://localhost:8000/SAP-015
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |
| `ALIAS_MAPPING_PATH` | `../../capabilities/alias-mapping.json` | Path to alias mapping file |

### Custom Alias Mapping

To use a custom alias mapping file:

```bash
# Mount custom mapping
docker run -d \
    -v /path/to/custom-mapping.json:/app/capabilities/alias-mapping.json:ro \
    sap-alias-redirect:1.0.0
```

## Monitoring

### Health Checks

```bash
# Docker health check
docker inspect --format='{{.State.Health.Status}}' sap-alias-redirect

# Manual health check
curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker logs -f sap-alias-redirect

# Filter for errors
docker logs sap-alias-redirect 2>&1 | grep ERROR
```

### Metrics

The service exposes the following metrics:
- Total alias lookups
- 404 errors (invalid SAP IDs)
- Response times
- Active connections

## Deployment Options

### Option 1: Standalone Service

Deploy as a standalone service on port 8000:

```bash
docker-compose up -d
```

Access at: `http://localhost:8000`

### Option 2: Behind Reverse Proxy

Deploy behind nginx/Traefik for production:

```nginx
# nginx config
location /sap/ {
    proxy_pass http://sap-alias-redirect:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Access at: `https://chora-base.dev/sap/SAP-015`

### Option 3: Kubernetes

Deploy with Kubernetes:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sap-alias-redirect
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sap-alias-redirect
  template:
    metadata:
      labels:
        app: sap-alias-redirect
    spec:
      containers:
      - name: sap-alias-redirect
        image: sap-alias-redirect:1.0.0
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 30
```

## Troubleshooting

### Service won't start

**Problem**: Container exits immediately

**Solution**: Check alias mapping file exists
```bash
ls -la ../../capabilities/alias-mapping.json
docker logs sap-alias-redirect
```

### 404 errors for valid SAP IDs

**Problem**: SAP-XXX not found

**Solution**: Reload alias mapping
```bash
# Restart service to reload mapping
docker-compose restart
```

### Slow response times

**Problem**: High latency on alias lookups

**Solution**: Increase workers
```bash
# Dockerfile: increase --workers
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Format code
black app.py

# Lint code
ruff check app.py

# Type check
mypy app.py
```

## Related Documentation

- [Migration Guide](../../docs/ontology/migration-guide.md) - How to migrate from SAP-XXX to modern namespaces
- [Namespace Specification](../../docs/ontology/namespace-spec.md) - Modern namespace format
- [Phase 3 Summary](../../docs/ontology/PHASE3-COMPLETE.md) - Ontology migration completion report

## Support

- **Issues**: https://github.com/chora-base/chora-base/issues
- **Documentation**: https://github.com/chora-base/chora-base/blob/main/docs/
- **Migration Support**: See [migration-guide.md](../../docs/ontology/migration-guide.md)

## License

MIT License - See [LICENSE](../../LICENSE) for details

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Status**: Production Ready ✅
