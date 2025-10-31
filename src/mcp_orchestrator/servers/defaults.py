"""Default catalog of known MCP servers.

This module provides a curated list of popular MCP servers that users can
easily add to their configurations.
"""

from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)


def get_default_servers() -> list[ServerDefinition]:
    """Get list of default MCP server definitions.

    Returns:
        List of ServerDefinition objects for common MCP servers
    """
    return [
        # =================================================================
        # STDIO SERVERS
        # =================================================================
        ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem Access",
            description="Read, write, and search local files and directories",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-filesystem", "{path}"],
            parameters=[
                ParameterDefinition(
                    name="path",
                    type="path",
                    description="Root directory path to expose",
                    required=True,
                    example="/Users/you/Documents",
                )
            ],
            npm_package="@modelcontextprotocol/server-filesystem",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem",
            tags=["files", "storage", "local"],
        ),
        ServerDefinition(
            server_id="brave-search",
            display_name="Brave Search",
            description="Web search using Brave Search API",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-brave-search"],
            required_env=["BRAVE_API_KEY"],
            npm_package="@modelcontextprotocol/server-brave-search",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search",
            tags=["search", "web", "internet"],
        ),
        ServerDefinition(
            server_id="github",
            display_name="GitHub Integration",
            description="Search repositories, create issues, manage pull requests",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-github"],
            required_env=["GITHUB_TOKEN"],
            npm_package="@modelcontextprotocol/server-github",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/github",
            tags=["git", "github", "version-control"],
        ),
        ServerDefinition(
            server_id="memory",
            display_name="Memory Storage",
            description="Key-value storage for maintaining context across conversations",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-memory"],
            npm_package="@modelcontextprotocol/server-memory",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/memory",
            tags=["storage", "persistence", "memory"],
        ),
        ServerDefinition(
            server_id="fetch",
            display_name="Web Fetch",
            description="Fetch and process content from web URLs",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-fetch"],
            npm_package="@modelcontextprotocol/server-fetch",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/fetch",
            tags=["web", "http", "fetch"],
        ),
        ServerDefinition(
            server_id="postgres",
            display_name="PostgreSQL Database",
            description="Query and manage PostgreSQL databases",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=[
                "-y",
                "@modelcontextprotocol/server-postgres",
                "{connection_string}",
            ],
            parameters=[
                ParameterDefinition(
                    name="connection_string",
                    type="string",
                    description="PostgreSQL connection string",
                    required=True,
                    example="postgresql://user:password@localhost:5432/dbname",
                )
            ],
            npm_package="@modelcontextprotocol/server-postgres",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/postgres",
            tags=["database", "sql", "postgres"],
        ),
        ServerDefinition(
            server_id="sqlite",
            display_name="SQLite Database",
            description="Query and manage SQLite databases",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-sqlite", "{db_path}"],
            parameters=[
                ParameterDefinition(
                    name="db_path",
                    type="path",
                    description="Path to SQLite database file",
                    required=True,
                    example="/path/to/database.db",
                )
            ],
            npm_package="@modelcontextprotocol/server-sqlite",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite",
            tags=["database", "sql", "sqlite"],
        ),
        ServerDefinition(
            server_id="slack",
            display_name="Slack Integration",
            description="Read channels, send messages, manage Slack workspace",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-slack"],
            required_env=["SLACK_BOT_TOKEN", "SLACK_TEAM_ID"],
            npm_package="@modelcontextprotocol/server-slack",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/slack",
            tags=["chat", "communication", "slack"],
        ),
        ServerDefinition(
            server_id="puppeteer",
            display_name="Browser Automation",
            description="Automate web browser interactions using Puppeteer",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-puppeteer"],
            npm_package="@modelcontextprotocol/server-puppeteer",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer",
            tags=["browser", "automation", "web"],
        ),
        ServerDefinition(
            server_id="google-maps",
            display_name="Google Maps",
            description="Search places, get directions, geocoding via Google Maps API",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-google-maps"],
            required_env=["GOOGLE_MAPS_API_KEY"],
            npm_package="@modelcontextprotocol/server-google-maps",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps",
            tags=["maps", "location", "google"],
        ),
        # =================================================================
        # HTTP/SSE SERVERS (will be auto-wrapped with mcp-remote)
        # =================================================================
        ServerDefinition(
            server_id="n8n",
            display_name="n8n Workflows",
            description="Execute n8n workflow automations via HTTP/SSE",
            transport=TransportType.SSE,
            http_url="http://localhost:{port}/mcp/sse",
            http_auth_type="bearer",
            parameters=[
                ParameterDefinition(
                    name="port",
                    type="int",
                    description="n8n server port",
                    required=False,
                    default=5679,
                    example="5679",
                )
            ],
            required_env=["N8N_API_KEY"],
            documentation_url="https://docs.n8n.io/mcp/",
            tags=["automation", "workflow", "remote"],
        ),
        ServerDefinition(
            server_id="custom-api",
            display_name="Custom API Server",
            description="Example HTTP MCP server for custom integrations",
            transport=TransportType.HTTP,
            http_url="http://{host}:{port}/mcp",
            http_auth_type="none",
            parameters=[
                ParameterDefinition(
                    name="host",
                    type="string",
                    description="Server hostname or IP",
                    required=False,
                    default="localhost",
                    example="api.example.com",
                ),
                ParameterDefinition(
                    name="port",
                    type="int",
                    description="Server port",
                    required=False,
                    default=8080,
                    example="8080",
                ),
            ],
            documentation_url="https://modelcontextprotocol.io/",
            tags=["custom", "http", "remote"],
        ),
        ServerDefinition(
            server_id="everything",
            display_name="Everything Search (Windows)",
            description="Lightning-fast file search on Windows using Everything",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-everything"],
            npm_package="@modelcontextprotocol/server-everything",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/everything",
            tags=["search", "files", "windows"],
        ),
        ServerDefinition(
            server_id="sequential-thinking",
            display_name="Sequential Thinking",
            description="Structured thinking and reasoning workflow",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
            npm_package="@modelcontextprotocol/server-sequential-thinking",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/sequential-thinking",
            tags=["reasoning", "thinking", "workflow"],
        ),
        ServerDefinition(
            server_id="sentry",
            display_name="Sentry Error Tracking",
            description="Query and manage Sentry error tracking data",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-sentry"],
            required_env=["SENTRY_AUTH_TOKEN", "SENTRY_ORG_SLUG"],
            npm_package="@modelcontextprotocol/server-sentry",
            documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/sentry",
            tags=["monitoring", "errors", "debugging"],
        ),
    ]
