# n8n Workflow Examples for chora-compose

**Purpose**: Production-ready n8n workflow examples for integrating chora-compose with automation platforms.

**Audience**: DevOps engineers, automation teams, Docker modality users

**Last Updated**: 2025-11-04

---

## Overview

This directory contains three n8n workflow examples demonstrating chora-compose integration patterns:

1. **[workflow-1-scheduled-generation.json](./workflow-1-scheduled-generation.json)** - Scheduled content generation with notifications
2. **[workflow-2-webhook-assembly.json](./workflow-2-webhook-assembly.json)** - Webhook-triggered artifact assembly with GitHub PR integration
3. **[workflow-3-batch-docs.json](./workflow-3-batch-docs.json)** - Batch documentation generation using collections

All workflows use the **Docker modality** for chora-compose integration (see [protocol-spec.md §2.4](../protocol-spec.md#contract-4-docker-integration-team-deployment)).

---

## Prerequisites

### Required Software

1. **n8n** (v1.0.0+)
   - Installation: `npm install -g n8n` or use Docker: `docker run -p 5678:5678 n8nio/n8n`
   - Documentation: https://docs.n8n.io/

2. **Docker** (v20.10+)
   - Installation: https://docs.docker.com/get-docker/
   - Required for running chora-compose container in workflows

3. **chora-compose Docker Image**
   - Pull: `docker pull ghcr.io/liminalcommons/chora-compose:latest`
   - Verify: `docker images | grep chora-compose`

### Optional Integrations

**Workflow 1** (Scheduled Generation):
- Slack workspace with bot token for notifications
- Webhook credentials for HTTP requests

**Workflow 2** (Webhook Assembly):
- GitHub API token for PR integration
- Cloud storage (Google Drive, S3, etc.) for artifact uploads

**Workflow 3** (Batch Docs):
- GitHub API token for summary issue creation
- Slack workspace for batch completion notifications

---

## Workflow 1: Scheduled Content Generation

**File**: [workflow-1-scheduled-generation.json](./workflow-1-scheduled-generation.json)

**Use Case**: Automatically generate content on a schedule (e.g., daily metrics, weekly reports).

### Features

- **Schedule Trigger**: Runs every 6 hours (configurable)
- **Docker Execution**: Uses chora-compose Docker image
- **Success Detection**: Checks exit code for generation success
- **Notifications**: Posts to Slack on success/failure
- **Metadata Logging**: Captures execution time and paths

### Workflow Diagram

```
┌──────────────────┐
│ Schedule Trigger │ (Every 6 hours)
└────────┬─────────┘
         │
         v
┌──────────────────────────┐
│ Execute chora-compose    │ (Docker run)
│ generate content         │
└────────┬─────────────────┘
         │
         v
┌──────────────────────────┐
│ Check Generation Success │ (If exit_code == 0)
└────────┬─────────────────┘
         │
         ├─── Success ──> Read Generated Content ──> Notify Slack ✓
         │
         └─── Failure ──> Notify Slack ✗
```

### Setup Instructions

1. **Import Workflow**:
   - Open n8n UI (http://localhost:5678)
   - Go to: Workflows → Import from File
   - Select: `workflow-1-scheduled-generation.json`

2. **Configure Schedule Trigger**:
   - Click "Schedule Trigger" node
   - Adjust interval (default: every 6 hours)
   - Options: hours, days, weeks, cron expression

3. **Update chora-compose Config Path**:
   - Click "Execute chora-compose Generation" node
   - Update `--config` path to your config file (default: `configs/content/daily-metrics.yaml`)
   - Ensure config file exists in your workspace

4. **Configure Slack Credentials** (optional):
   - Create Slack app: https://api.slack.com/apps
   - Add bot token scope: `chat:write`
   - In n8n: Credentials → Add Credential → Header Auth
   - Name: "Slack Bot Token"
   - Header Name: `Authorization`
   - Header Value: `Bearer xoxb-your-slack-token`
   - Assign credential to "Notify Slack" nodes

5. **Test Workflow**:
   - Click "Execute Workflow" button
   - Check execution status in n8n UI
   - Verify output file exists and Slack notification sent

### Configuration Example

**Required config**: `configs/content/daily-metrics.yaml`

```yaml
version: "3.1"
content_id: daily-metrics
generator_type: jinja2
output_path: output/metrics/daily-metrics.md

template: |
  # Daily Metrics - {{ date }}

  ## Repository Activity
  - Commits: {{ commits_today }}
  - Pull Requests: {{ prs_today }}
  - Issues Closed: {{ issues_closed_today }}

  ## Team Velocity
  - Story Points Completed: {{ story_points }}
  - Sprint Progress: {{ sprint_progress }}%

context:
  inline_data:
    date: "{{ now().strftime('%Y-%m-%d') }}"
  external_file:
    path: metrics/latest-stats.json
    format: json
```

### Troubleshooting

**Issue**: "Docker not found" error

**Solution**:
1. Ensure Docker Desktop is running
2. Verify n8n has access to Docker socket
3. If using n8n Docker container, mount Docker socket:
   ```bash
   docker run -p 5678:5678 \
     -v /var/run/docker.sock:/var/run/docker.sock \
     n8nio/n8n
   ```

**Issue**: "Config file not found" error

**Solution**:
1. Verify config path in "Execute chora-compose Generation" node
2. Ensure volume mount includes config directory: `-v $(pwd):/workspace`
3. Use absolute paths inside container: `/workspace/configs/...`

---

## Workflow 2: Webhook-Triggered Artifact Assembly

**File**: [workflow-2-webhook-assembly.json](./workflow-2-webhook-assembly.json)

**Use Case**: Trigger artifact assembly via webhook (e.g., GitHub PR, manual API call, CI/CD pipeline).

### Features

- **Webhook Trigger**: POST endpoint for external integrations
- **Payload Parsing**: Extracts artifact_id, config_path, metadata
- **GitHub PR Integration**: Fetches PR data and injects as context
- **Docker Execution**: Runs chora-compose artifact assembly
- **Cloud Upload**: Uploads generated artifact to cloud storage
- **Webhook Response**: Returns JSON with artifact URL and status

### Workflow Diagram

```
┌──────────────────┐
│ Webhook Trigger  │ (POST /chora-compose/assemble-docs)
└────────┬─────────┘
         │
         v
┌──────────────────────┐
│ Parse Webhook Payload│ (Extract artifact_id, config_path)
└────────┬─────────────┘
         │
         v
┌──────────────────────┐
│ Check Trigger Type   │ (If trigger_source == "github_pr")
└────────┬─────────────┘
         │
         ├─── GitHub PR ──> Fetch PR Data ──> Execute Assembly (with PR context)
         │
         └─── Standard ──> Execute Assembly (standard)
         │
         v
┌────────────────────────────┐
│ Check Assembly Success     │ (If exit_code == 0)
└────────┬───────────────────┘
         │
         ├─── Success ──> Extract Output Path ──> Read Artifact ──> Upload to Storage ──> Respond Success
         │
         └─── Failure ──> Respond Failure
```

### Setup Instructions

1. **Import Workflow**: Import `workflow-2-webhook-assembly.json` in n8n UI

2. **Configure Webhook**:
   - Click "Webhook Trigger" node
   - Note webhook URL (e.g., `http://n8n.yourcompany.com/webhook/chora-compose/assemble-docs`)
   - Set authentication if needed (Basic Auth, Header Auth)

3. **Configure GitHub Credentials** (for PR integration):
   - In n8n: Credentials → Add Credential → Header Auth
   - Name: "GitHub Token"
   - Header Name: `Authorization`
   - Header Value: `token ghp_your_github_token`
   - Assign to "Fetch PR Data (GitHub)" node

4. **Configure Cloud Storage** (optional):
   - Example: Google Drive integration
   - In n8n: Credentials → Add Credential → Google Drive OAuth2 API
   - Follow OAuth flow to authorize access
   - Assign to "Upload to Cloud Storage" node

5. **Test Webhook**:
   ```bash
   curl -X POST http://localhost:5678/webhook/chora-compose/assemble-docs \
     -H "Content-Type: application/json" \
     -d '{
       "artifact_id": "api-docs",
       "config_path": "configs/artifacts/api-docs.yaml",
       "trigger_source": "manual"
     }'
   ```

### Webhook Payload Schema

**Standard Trigger**:
```json
{
  "artifact_id": "api-docs",                    // Required
  "config_path": "configs/artifacts/api-docs.yaml",  // Optional (default: configs/artifacts/{artifact_id}.yaml)
  "trigger_source": "manual",                   // Optional (default: "webhook")
  "metadata": {}                                // Optional
}
```

**GitHub PR Trigger**:
```json
{
  "artifact_id": "pr-summary",
  "config_path": "configs/artifacts/pr-summary.yaml",
  "trigger_source": "github_pr",
  "metadata": {
    "repo": "liminalcommons/chora-base",
    "pr_number": 42
  }
}
```

### GitHub Webhook Integration

To trigger from GitHub PR events:

1. **Create GitHub Webhook**:
   - Go to: Repository → Settings → Webhooks → Add webhook
   - Payload URL: `http://n8n.yourcompany.com/webhook/chora-compose/assemble-docs`
   - Content type: `application/json`
   - Events: Pull request opened, synchronized

2. **Configure Webhook Payload** (GitHub Actions example):
   ```yaml
   # .github/workflows/assemble-pr-docs.yml
   name: Assemble PR Documentation
   on:
     pull_request:
       types: [opened, synchronize]

   jobs:
     assemble-docs:
       runs-on: ubuntu-latest
       steps:
         - name: Trigger n8n Workflow
           run: |
             curl -X POST ${{ secrets.N8N_WEBHOOK_URL }} \
               -H "Content-Type: application/json" \
               -d '{
                 "artifact_id": "pr-summary",
                 "trigger_source": "github_pr",
                 "metadata": {
                   "repo": "${{ github.repository }}",
                   "pr_number": ${{ github.event.pull_request.number }}
                 }
               }'
   ```

### Troubleshooting

**Issue**: "Webhook not found" (404)

**Solution**:
1. Ensure workflow is activated in n8n UI
2. Verify webhook path matches exactly
3. Check n8n logs for webhook registration

**Issue**: GitHub API rate limit exceeded

**Solution**:
1. Use authenticated GitHub token (higher rate limit)
2. Add caching for PR data (if fetching multiple times)

---

## Workflow 3: Batch Documentation Generation

**File**: [workflow-3-batch-docs.json](./workflow-3-batch-docs.json)

**Use Case**: Generate multiple documents in parallel using chora-compose collections.

### Features

- **Webhook/Manual Trigger**: Flexible triggering (webhook or manual execution)
- **Cache Invalidation**: Optional cache clearing before generation
- **Parallel Execution**: Configurable parallel workers (default: 4)
- **Collection Generation**: Bulk generation via chora-compose collections
- **Result Parsing**: Extracts statistics (success rate, cache hit rate, time)
- **GitHub Integration**: Creates summary issue with generation report
- **Slack Notifications**: Posts batch completion summary
- **Webhook Response**: Returns detailed execution statistics

### Workflow Diagram

```
┌──────────────────────┐
│ Manual/Webhook       │ (POST /chora-compose/generate-all-docs)
│ Trigger              │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Configure Batch      │ (Parse collection_config, parallel_workers)
│ Execution            │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Check Cache          │ (If invalidate_cache == true)
│ Invalidation         │
└──────────┬───────────┘
           │
           ├─── Yes ──> Invalidate Cache ─┐
           │                               │
           └─── No ─────────────────────┐  │
                                        │  │
                                        v  v
                               ┌─────────────────┐
                               │ Merge Cache     │
                               │ Branch          │
                               └────────┬────────┘
                                        │
                                        v
                               ┌─────────────────────┐
                               │ Execute Collection  │ (Docker run, parallel)
                               │ Generation          │
                               └────────┬────────────┘
                                        │
                                        v
                               ┌─────────────────────┐
                               │ Parse Collection    │ (Extract stats)
                               │ Results             │
                               └────────┬────────────┘
                                        │
                                        v
                               ┌─────────────────────┐
                               │ Check Generation    │ (If success)
                               │ Success             │
                               └────────┬────────────┘
                                        │
         ├────────── Success ──────────┴─────────── Failure ────┐
         │                                                       │
         v                                                       v
┌─────────────────────┐                              ┌──────────────────┐
│ List Generated Files│                              │ Notify Slack     │
└────────┬────────────┘                              │ (Failure)        │
         │                                            └──────────────────┘
         v
┌─────────────────────┐
│ Format File List    │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│ Create GitHub       │
│ Summary Issue       │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│ Notify Slack        │
│ (Success)           │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│ Respond Webhook     │
└─────────────────────┘
```

### Setup Instructions

1. **Import Workflow**: Import `workflow-3-batch-docs.json` in n8n UI

2. **Configure Collection Config**:
   - Create collection config: `configs/collections/all-docs.yaml`
   - Example collection config:
     ```yaml
     version: "1.0"
     collection_id: all-docs
     execution_strategy: parallel
     max_workers: 4

     artifacts:
       - config_path: configs/artifacts/api-docs.yaml
       - config_path: configs/artifacts/user-guide.yaml
       - config_path: configs/artifacts/architecture-docs.yaml
     ```

3. **Configure GitHub Credentials**:
   - In n8n: Credentials → Add Credential → GitHub API
   - Enter GitHub token
   - Assign to "Create GitHub Summary Issue" node

4. **Configure Slack Credentials**:
   - Add Slack bot token (see Workflow 1 setup)
   - Assign to "Notify Slack" nodes

5. **Test Workflow**:
   ```bash
   curl -X POST http://localhost:5678/webhook/chora-compose/generate-all-docs \
     -H "Content-Type: application/json" \
     -d '{
       "collection_config": "configs/collections/all-docs.yaml",
       "parallel_workers": 4,
       "invalidate_cache": false,
       "trigger_source": "manual"
     }'
   ```

### Webhook Payload Schema

```json
{
  "collection_config": "configs/collections/all-docs.yaml",  // Optional (default: configs/collections/all-docs.yaml)
  "parallel_workers": 4,                                      // Optional (default: 4)
  "invalidate_cache": false,                                  // Optional (default: false)
  "trigger_source": "manual"                                  // Optional (default: "manual")
}
```

### Performance Tuning

**Parallel Workers**:
- Default: 4 workers
- Recommendation: Set to number of CPU cores (or fewer for I/O-bound generation)
- Higher values: Faster completion, higher CPU/memory usage
- Lower values: Slower completion, lower resource usage

**Cache Strategy**:
- `invalidate_cache: false` (default): Use cached results (95%+ faster for unchanged content)
- `invalidate_cache: true`: Force regeneration (use when context sources changed)

**Timeout**:
- Default: 600000ms (10 minutes)
- Adjust in "Execute Collection Generation" node if collection is large

### Example GitHub Summary Issue

```markdown
## Batch Documentation Generation Summary

**Execution ID**: `batch-1730736000000`
**Timestamp**: 2025-11-04T12:00:00.000Z

### Statistics
- **Items Generated**: 18/18 (100% success)
- **Total Time**: 142.5s
- **Cache Hit Rate**: 94.4% (17 hits, 1 misses)

### Generated Files (18)
```
output/docs/sap-000-framework/protocol-spec.md
output/docs/sap-001-git-workflows/protocol-spec.md
...
output/docs/sap-017-chora-compose-integration/protocol-spec.md
```

### Next Steps
- [ ] Review generated documentation for accuracy
- [ ] Update any outdated content sources
- [ ] Deploy documentation to production

---
*Generated by chora-compose n8n workflow*
```

### Troubleshooting

**Issue**: "Collection generation timeout" error

**Solution**:
1. Increase timeout in "Execute Collection Generation" node
2. Reduce `parallel_workers` to lower resource usage
3. Split large collections into smaller batches

**Issue**: High memory usage during batch generation

**Solution**:
1. Reduce `parallel_workers` (e.g., from 4 to 2)
2. Enable cache to reduce regeneration load
3. Monitor Docker container resources: `docker stats`

---

## Common Configuration

### Environment Variables

All workflows support these environment variables (passed via Docker `-e` flag):

- `CHORA_COMPOSE_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `CHORA_COMPOSE_CACHE_DIR`: Cache directory path (default: `/workspace/.chora-compose`)
- `PARALLEL_WORKERS`: Number of parallel workers for collection generation

**Example**:
```bash
docker run --rm \
  -v $(pwd):/workspace \
  -e CHORA_COMPOSE_LOG_LEVEL=DEBUG \
  -e PARALLEL_WORKERS=8 \
  ghcr.io/liminalcommons/chora-compose:latest \
  generate collection --config /workspace/configs/collections/all-docs.yaml
```

### Volume Mounts

All workflows require these Docker volume mounts:

- **Workspace**: `-v $(pwd):/workspace` (required)
  - Contains configs, templates, output directories
  - Mounted as read-write for output generation

**Optional mounts**:
- **Configs (read-only)**: `-v $(pwd)/configs:/configs:ro`
- **Output (write-only)**: `-v $(pwd)/output:/output:rw`

### Error Handling

All workflows implement consistent error handling:

1. **Exit Code Checking**: Validate `exitCode == 0` for success
2. **stderr Capture**: Log error output for debugging
3. **Notifications**: Alert team on failures (Slack, email, etc.)
4. **Webhook Response**: Return error details to caller (for webhook triggers)

---

## Customization Guide

### Adding Custom Integrations

**Example: Add email notification**

1. Add "Send Email" node after "Check Generation Success"
2. Configure SMTP credentials in n8n
3. Connect success/failure branches to email nodes
4. Customize email template with execution details

**Example: Add metrics tracking**

1. Add "HTTP Request" node to send metrics to analytics platform
2. Extract metrics from execution results (items generated, time, cache hit rate)
3. POST metrics to endpoint (e.g., Prometheus, Datadog, custom API)

### Modifying Schedules

**Workflow 1** schedule options:

- **Hourly**: Every N hours (e.g., every 6 hours)
- **Daily**: Specific time (e.g., 9:00 AM daily)
- **Weekly**: Day and time (e.g., Monday 9:00 AM)
- **Cron Expression**: Custom schedule (e.g., `0 */6 * * *` for every 6 hours)

### Workflow Variables

Use n8n "Set" node to define workflow-level variables:

```json
{
  "workspace_path": "/workspace",
  "config_directory": "configs",
  "output_directory": "output",
  "docker_image": "ghcr.io/liminalcommons/chora-compose:latest",
  "slack_channel": "#documentation"
}
```

Reference variables in downstream nodes: `{{$node['Variables'].json.workspace_path}}`

---

## Security Considerations

### Credential Management

1. **Never hardcode credentials** in workflow JSON
2. **Use n8n credential system** for all API tokens, passwords
3. **Rotate credentials regularly** (GitHub tokens, Slack tokens, etc.)
4. **Limit credential scope** (minimum required permissions)

### Volume Mount Security

1. **Mount only required directories**: Avoid `-v /:/workspace` (entire filesystem)
2. **Use read-only mounts** where possible: `-v $(pwd)/configs:/configs:ro`
3. **Validate output paths**: Ensure generated files stay within workspace

### Webhook Security

1. **Enable authentication**: Use Basic Auth or Header Auth for webhook endpoints
2. **Validate payloads**: Check required fields, sanitize inputs
3. **Rate limiting**: Configure n8n or reverse proxy to limit webhook requests
4. **HTTPS only**: Never expose webhooks over HTTP in production

### Docker Security

1. **Use specific image tags**: Avoid `:latest` in production (pin to version like `:v1.5.0`)
2. **Pull image before execution**: Ensure latest security patches
3. **Resource limits**: Set Docker memory/CPU limits to prevent DoS
4. **Non-root user**: chora-compose Docker image runs as non-root by default

---

## Performance Benchmarks

### Workflow 1: Scheduled Content Generation

| Metric | Value | Notes |
|--------|-------|-------|
| Execution Time | 2-5 seconds | Single content piece, cache hit |
| Cold Start | 10-15 seconds | First execution, cache miss |
| Network Overhead | < 1 second | Docker image already pulled |
| Notification Latency | 1-2 seconds | Slack API call |

### Workflow 2: Webhook-Triggered Artifact Assembly

| Metric | Value | Notes |
|--------|-------|-------|
| Webhook Response Time | 8-12 seconds | 5-piece artifact, 90% cache hit |
| GitHub API Latency | 200-500ms | Fetch PR data |
| Cloud Upload Time | 2-4 seconds | 1MB artifact to Google Drive |
| Total End-to-End | 15-20 seconds | Webhook → artifact uploaded |

### Workflow 3: Batch Documentation Generation

| Metric | Value | Notes |
|--------|-------|-------|
| Collection Size | 18 artifacts | chora-base SAP documentation |
| Execution Time (cached) | 45-60 seconds | 95% cache hit, 4 workers |
| Execution Time (cold) | 3-5 minutes | Cache miss, full regeneration |
| Cache Hit Rate | 90-95% | Typical for stable configs |
| Parallel Speedup | 3-4x | vs sequential execution |

**Test Environment**: M1 Mac, 16GB RAM, Docker Desktop 4.25, n8n v1.12.0

---

## Troubleshooting

### Common Issues

**Issue**: n8n workflow execution stuck

**Diagnosis**:
```bash
# Check n8n logs
docker logs -f n8n

# Check Docker container status
docker ps -a | grep chora-compose
```

**Solution**:
1. Check Docker container logs for errors
2. Verify volume mount paths are correct
3. Ensure chora-compose image is pulled and accessible

**Issue**: "Permission denied" when writing to output directory

**Diagnosis**:
```bash
# Check output directory permissions
ls -la output/

# Check Docker container user
docker run --rm ghcr.io/liminalcommons/chora-compose:latest whoami
```

**Solution**:
1. Fix output directory permissions: `chmod -R u+w output/`
2. Ensure Docker has write access to mounted volumes
3. On Linux: Check user ID matches between host and container

**Issue**: Slow generation performance

**Diagnosis**:
```bash
# Monitor Docker resource usage
docker stats

# Check cache hit rate in workflow output
# Look for: "Cache hits: X, misses: Y (Z% hit rate)"
```

**Solution**:
1. Ensure cache is enabled (don't invalidate unnecessarily)
2. Increase parallel workers if CPU usage < 80%
3. Check context sources for network latency (external_file, git_reference)

---

## Additional Resources

### Documentation

- [SAP-017 Protocol Specification](../protocol-spec.md) - Complete integration guide
- [SAP-017 Awareness Guide](../awareness-guide.md) - Quick reference for AI agents
- [SAP-017 Adoption Blueprint](../adoption-blueprint.md) - Step-by-step adoption guide
- [chora-compose Documentation](https://github.com/liminalcommons/chora-compose/tree/main/docs) - Comprehensive chora-compose docs

### n8n Resources

- [n8n Documentation](https://docs.n8n.io/) - Official n8n docs
- [n8n Workflows](https://n8n.io/workflows/) - Community workflow library
- [n8n Docker Integration](https://docs.n8n.io/hosting/docker/) - Docker deployment guide

### Community

- Report issues: [chora-base GitHub Issues](https://github.com/liminalcommons/chora-base/issues)
- Request features: Tag with `SAP-017` label
- Share workflows: Contribute n8n workflow examples to this directory

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-04 | Initial n8n workflow examples (3 workflows) |

---

**Maintainer**: Victor
**SAP ID**: SAP-017
**Last Updated**: 2025-11-04
