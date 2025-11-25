# Orchestration Health Monitor - Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    PyYAML==6.0.1 \
    etcd3==0.12.0 \
    docker==7.0.0

# Copy health monitor script
COPY health_monitor.py /app/health_monitor.py

# Make script executable
RUN chmod +x /app/health_monitor.py

# Health check (verify etcd and Docker connections)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import etcd3, docker; etcd3.client(host='etcd1', port=2379).status(); docker.DockerClient(base_url='unix://var/run/docker.sock').ping()" || exit 1

# Run health monitor service
CMD ["python", "/app/health_monitor.py", \
     "--etcd-host", "etcd1", \
     "--etcd-port", "2379", \
     "--interval", "10", \
     "--ttl", "30", \
     "--docker-host", "unix://var/run/docker.sock"]
