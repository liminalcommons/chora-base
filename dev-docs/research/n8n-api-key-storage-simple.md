# n8n API Key Storage (Simple Approach)

**Status:** ✅ Implemented (using existing `.env` pattern)
**Priority:** P0 (Critical)
**Created:** 2025-10-22
**Updated:** 2025-10-22 - Clarified 2-environment strategy

---

## Environment Strategy: 2 Environments

### Environment 1: Production (Port 5678)
- **File:** `docker-compose.yml`
- **API Key:** `.env`
- **Purpose:** Real Claude Desktop usage, personal workflows
- **Data:** Persistent (your real workflows - **don't develop here**)

### Environment 2: Dev/Test (Port 5679)
- **File:** `docker-compose.test.yml`
- **API Key:** `.env.test`
- **Purpose:** Daily development, E2E testing, experimentation
- **Data:** Ephemeral (safe to destroy anytime)

---

## Setup (One-time per environment)

### Production Environment Setup

1. **Start production n8n:**
   ```bash
   docker-compose up -d n8n
   ```

2. **Create API key in n8n UI:**
   - Open http://localhost:5678
   - Navigate to: Settings → API
   - Click "Create API Key"
   - Copy the key

3. **Store in `.env` file:**
   ```bash
   # Add to .env in project root
   echo "N8N_API_KEY=your-production-key-here" >> .env
   ```

### Dev/Test Environment Setup

1. **Start dev/test n8n:**
   ```bash
   docker-compose -f docker-compose.test.yml up -d n8n-test
   ```

2. **Create API key in n8n UI:**
   - Open http://localhost:5679 (different port!)
   - Navigate to: Settings → API
   - Click "Create API Key"
   - Copy the key

3. **Store in `.env.test` file:**
   ```bash
   # Create .env.test in project root
   cat > .env.test << 'EOF'
   # Dev/Test Environment Configuration
   N8N_API_KEY=your-dev-test-key-here
   N8N_HOST=http://localhost:5679
   TZ=America/Los_Angeles
   GENERIC_TIMEZONE=America/Los_Angeles
   EOF
   ```

---

## Daily Workflow

### For Development Work

**Always develop against the dev/test environment (port 5679):**

```bash
# Start dev/test environment
docker-compose -f docker-compose.test.yml up -d

# Load test environment variables
source .env.test

# Work on http://localhost:5679
# Build workflows, test, break things - it's safe!

# When done, tear it down (data is ephemeral)
docker-compose -f docker-compose.test.yml down -v
```

### For Production (Claude Desktop)

**Only use production environment for real workflows:**

```bash
# Start production environment
docker-compose up -d

# Use http://localhost:5678
# Your real, persistent workflows

# Stop (but don't remove volumes - data is persistent)
docker-compose down
```

### For E2E Testing

```bash
# Load test environment variables
source .env.test

# Run E2E setup script
./tests/e2e/fixtures/n8n/setup_n8n_tests.sh

# Run E2E tests
pytest tests/e2e/test_n8n_integration_e2e.py -v

# Or use justfile
just e2e-all
```

---

## Summary

✅ **Production (port 5678):**
- API key in `.env`
- Persistent data
- **Don't develop here**

✅ **Dev/Test (port 5679):**
- API key in `.env.test`
- Ephemeral data
- **Develop here daily**

This separation keeps your production workflows safe while allowing you to freely experiment in development.

---

## Future Research (Deferred)

More sophisticated approaches can be researched later:
- Automated key generation
- Per-environment key management
- Secrets manager integration (cloud)
- Key rotation strategies

For now: Manual creation + `.env` storage is adequate.
