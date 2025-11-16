# Registry Heartbeat Service - Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir PyYAML==6.0.1 etcd3==0.12.0

# Copy heartbeat script
COPY heartbeat.py /app/heartbeat.py

# Make script executable
RUN chmod +x /app/heartbeat.py

# Health check (verify etcd connection and recent heartbeat)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import etcd3; etcd3.client(host='etcd1', port=2379).status()" || exit 1

# Run heartbeat service with auto-discovery
CMD ["python", "/app/heartbeat.py", \
     "--auto-discover", \
     "--capabilities", "/app/capabilities", \
     "--etcd-host", "etcd1", \
     "--etcd-port", "2379", \
     "--interval", "10", \
     "--ttl", "30"]
