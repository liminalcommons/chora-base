# Claude Docker Assistance - mcp-orchestration

**Purpose:** Claude-specific patterns for Docker containerization of mcp-orchestration MCP server.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic Docker guide.

---

## Claude's Docker Strengths for MCP Servers

Claude excels at Docker tasks for mcp-orchestration because:

- **Multi-stage build optimization** - Minimal Python MCP server images
- **MCP server patterns** - Understands MCP protocol deployment requirements
- **Security** - Non-root containers, minimal attack surface
- **Troubleshooting** - Diagnoses container networking and volume issues
- **Documentation** - Generates deployment guides

---

## mcp-orchestration Dockerfile Pattern

### Current Dockerfile Structure

The project uses multi-stage builds:

1. **Builder stage** - Installs dependencies, builds package
2. **Runtime stage** - Minimal Python image with MCP server only

### Key Considerations

- **Storage volumes:** Content-addressable storage in `var/storage`
- **Crypto keys:** Ed25519 keys in `var/keys`
- **Telemetry:** Event logs in `var/telemetry`
- **Network:** MCP server exposes stdio transport (no network ports)

---

## Common Docker Tasks with Claude

### Build and Test Container

```markdown
"Build mcp-orchestration Docker image and test:

1. Build with tag: mcp-orchestration:test
2. Run container with volume mounts for var/
3. Test MCP tool invocation via stdio
4. Verify storage and crypto work in container
5. Check telemetry events written

Show me any errors from build or runtime."
```

### Optimize Image Size

```markdown
"Current mcp-orchestration image is XXX MB.

Optimize:
1. Review Dockerfile for unnecessary layers
2. Check for unused dependencies in pyproject.toml
3. Use .dockerignore for test files
4. Combine RUN commands where possible
5. Target < 150 MB final image

Show me size comparison before/after."
```

### Debug Container Issues

```markdown
"mcp-orchestration container failing with:

Error: [paste error]

Debug steps:
1. Check volume mounts for var/ directory
2. Verify permissions for non-root user
3. Test storage initialization
4. Check crypto key generation
5. Review MCP server stdio transport

Show me debug commands to run."
```

---

## docker-compose for Development

### Development Setup Request

```markdown
"Create docker-compose.yml for mcp-orchestration development:

Services:
1. mcp-orchestration - Main MCP server
   - Volume mount src/ for hot reload
   - Volume mount var/ for persistent storage
   - Expose stdio transport

Requirements:
- Development profile with code mounting
- Persistent volumes for storage/keys/telemetry
- Easy log access
- Health check

Follow MCP server patterns."
```

---

## Deployment Patterns

### Claude Desktop Integration

```markdown
"Help me deploy mcp-orchestration Docker container for Claude Desktop:

Requirements:
1. Container runs MCP server via stdio
2. Claude Desktop config points to container
3. Storage persists between container restarts
4. Keys persist and are secure

Generate:
1. Dockerfile (if optimization needed)
2. docker-compose.yml for deployment
3. Claude Desktop config snippet
4. Deployment instructions
```

### Volume Management

```markdown
"Configure Docker volumes for mcp-orchestration:

Volumes needed:
1. var/storage - Content-addressable artifacts (must persist)
2. var/keys - Ed25519 keypairs (must persist, secure)
3. var/telemetry - Event logs (can be ephemeral)

Requirements:
- Storage and keys MUST persist
- Proper permissions for non-root container user
- Backup strategy for keys

Generate volume configuration and backup script."
```

---

## Troubleshooting with Claude

### Storage Permission Issues

```markdown
"Container error: Permission denied writing to var/storage

Context:
- Running as non-root user 'mcp_orchestrator'
- Volume mounted from host
- Content-addressable storage needs write access

Debug and fix:
1. Check volume mount permissions
2. Verify user ID matches
3. Test storage initialization
4. Show me corrected Dockerfile/compose
```

### MCP Server Connection Issues

```markdown
"Claude Desktop can't connect to containerized mcp-orchestration:

Error: [paste error from Claude Desktop logs]

Diagnose:
1. Verify stdio transport configuration
2. Check container is running
3. Test manual stdio communication
4. Review Claude Desktop config JSON
5. Show me test commands
```

---

## Security Best Practices

### Secrets Management

```markdown
"Secure Ed25519 private keys in mcp-orchestration container:

Current: Keys in var/keys/ volume

Improve:
1. Use Docker secrets or bind mount for keys
2. Restrict permissions (600 for private keys)
3. Prevent accidental logging of key material
4. Document key rotation process

Show me secure configuration."
```

---

## Metrics and Monitoring

### Container Health

```markdown
"Add health check for mcp-orchestration container:

Health criteria:
1. MCP server responds to stdio
2. Storage directory accessible
3. Crypto keys loaded successfully
4. No critical errors in recent telemetry

Generate HEALTHCHECK Dockerfile directive and monitoring script."
```

---

## Resources

- **Project Dockerfile:** [Dockerfile](../Dockerfile)
- **Docker Best Practices:** [DOCKER_BEST_PRACTICES.md](../DOCKER_BEST_PRACTICES.md)
- **MCP Protocol:** https://modelcontextprotocol.io
- **Parent Claude Guide:** [../CLAUDE.md](../CLAUDE.md)
- **Generic Docker Guide:** [AGENTS.md](AGENTS.md)

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
