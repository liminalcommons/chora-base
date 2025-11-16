# GitOps Sync Service - Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir PyYAML==6.0.1 etcd3==0.12.0

# Copy sync script
COPY ../../scripts/gitops-sync-registry.py /app/gitops-sync.py

# Copy capabilities directory (will be mounted as volume in production)
# COPY ../../capabilities /app/capabilities

# Make script executable
RUN chmod +x /app/gitops-sync.py

# Health check (verify etcd connection)
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import etcd3; etcd3.client(host='etcd1', port=2379).status()" || exit 1

# Run sync service in watch mode
CMD ["python", "/app/gitops-sync.py", \
     "--capabilities", "/app/capabilities", \
     "--etcd-host", "etcd1", \
     "--etcd-port", "2379", \
     "--watch", \
     "--interval", "60"]
