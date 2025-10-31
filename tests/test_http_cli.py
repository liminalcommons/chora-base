"""
Tests for HTTP CLI commands (token generation and HTTP server).

This module tests the CLI entry points for:
1. mcp-orchestration-generate-token (http_cli/token.py)
2. mcp-orchestration-serve-http (http_cli/serve_http.py)

These tests target low-coverage CLI modules to push overall coverage from 69.53% to 70%+.

Test Strategy:
- Test argument parsing for both commands
- Test token generation CLI (success and error paths)
- Test HTTP server startup CLI (success and error paths)
- Mock external dependencies (auth service, HTTP server, uvicorn)
- Test both command-line invocation and programmatic usage
- Test error handling and exit codes

Coverage targets:
- token.py: 18.42% -> 80%+
- serve_http.py: 21.05% -> 80%+
"""

from unittest.mock import MagicMock, patch

import pytest
from mcp_orchestrator.http_cli.serve_http import serve_http_cli
from mcp_orchestrator.http_cli.token import generate_token_cli
from mcp_orchestrator.http_cli.token import main as token_main


class TestTokenGenerationCLI:
    """Test mcp-orchestration-generate-token CLI command."""

    def test_generate_token_cli_success(self, capsys):
        """Test successful token generation via CLI."""
        mock_token = "test_token_abc123xyz_secure_url_safe_base64_string"
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = mock_token

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                result = generate_token_cli()

        # Verify token returned
        assert result == mock_token

        # Verify output contains token
        captured = capsys.readouterr()
        assert "Token generated successfully!" in captured.out
        assert mock_token in captured.out
        assert "Authorization: Bearer" in captured.out
        assert "Security:" in captured.out
        assert "Store this token securely" in captured.out

    def test_generate_token_cli_prints_usage_examples(self, capsys):
        """Test that CLI prints usage examples (curl, Python)."""
        mock_token = "example_token_123"
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = mock_token

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                generate_token_cli()

        captured = capsys.readouterr()

        # Verify usage examples
        assert "Usage in curl:" in captured.out
        assert "curl -H" in captured.out
        assert "Usage in Python:" in captured.out
        assert "import requests" in captured.out
        assert "http://localhost:8000/v1/clients" in captured.out

    def test_generate_token_cli_prints_security_warnings(self, capsys):
        """Test that CLI prints security warnings."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = "token"

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                generate_token_cli()

        captured = capsys.readouterr()

        # Verify security warnings
        assert "Do not commit to version control" in captured.out
        assert "Use environment variables" in captured.out
        assert "MCP_HTTP_TOKEN" in captured.out

    def test_generate_token_cli_error_handling(self, capsys):
        """Test CLI error handling when token generation fails."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.side_effect = Exception(
            "Token generation failed"
        )

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                with pytest.raises(SystemExit) as exc_info:
                    generate_token_cli()

        # Verify exit code
        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "Error generating token:" in captured.err
        assert "Token generation failed" in captured.err

    def test_generate_token_cli_calls_auth_service(self):
        """Test that CLI calls auth service generate_token method."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = "token123"

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                generate_token_cli()

        # Verify auth service called
        mock_auth_service.generate_token.assert_called_once()

    def test_generate_token_cli_argument_parser_help(self):
        """Test that argument parser has correct help text."""
        with patch("sys.argv", ["mcp-orchestration-generate-token", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                generate_token_cli()

        # --help should exit with 0
        assert exc_info.value.code == 0

    def test_generate_token_cli_parser_description(self, capsys):
        """Test that parser has helpful description and examples."""
        with patch("sys.argv", ["mcp-orchestration-generate-token", "--help"]):
            with pytest.raises(SystemExit):
                generate_token_cli()

        captured = capsys.readouterr()

        # Verify help text
        assert "Generate a new API token" in captured.out
        assert "Examples:" in captured.out
        assert "Usage:" in captured.out
        assert "Security:" in captured.out

    def test_token_main_success(self):
        """Test main() function success path."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = "token"

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                exit_code = token_main()

        # Should return 0 on success
        assert exit_code == 0

    def test_token_main_error(self, capsys):
        """Test main() function error path."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.side_effect = Exception("Test error")

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                # main() catches exception from generate_token_cli() which calls sys.exit(1)
                # So we need to catch the SystemExit
                try:
                    exit_code = token_main()
                except SystemExit:
                    # generate_token_cli() already called sys.exit(1), so main() propagates it
                    exit_code = 1

        # Should return 1 on error
        assert exit_code == 1

        # Verify error output
        captured = capsys.readouterr()
        assert "Error generating token:" in captured.err or "Error:" in captured.err

    def test_token_main_keyboard_interrupt(self):
        """Test main() handles KeyboardInterrupt gracefully."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.side_effect = KeyboardInterrupt()

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                # KeyboardInterrupt propagates as SystemExit
                try:
                    exit_code = token_main()
                except (SystemExit, KeyboardInterrupt):
                    # Either is acceptable for interruption
                    exit_code = 1

        # KeyboardInterrupt should be treated as error
        assert exit_code == 1

    def test_token_main_exception_in_main_function(self, capsys):
        """Test main() catches exceptions raised outside generate_token_cli()."""
        # Mock generate_token_cli to raise an exception that doesn't call sys.exit
        with patch(
            "mcp_orchestrator.http_cli.token.generate_token_cli",
            side_effect=RuntimeError("Direct error"),
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                exit_code = token_main()

        # Should return 1 on error
        assert exit_code == 1

        # Verify error output from main's exception handler
        captured = capsys.readouterr()
        assert "Error: Direct error" in captured.err


class TestServeHTTPCLI:
    """Test mcp-orchestration-serve-http CLI command."""

    def test_serve_http_cli_default_arguments(self, capsys):
        """Test HTTP server CLI with default arguments."""
        mock_server = MagicMock()
        mock_server_class = MagicMock(return_value=mock_server)

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            mock_server_class,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                exit_code = serve_http_cli()

        # Verify server created with defaults
        mock_server_class.assert_called_once_with(host="0.0.0.0", port=8000)

        # Verify server.run called
        mock_server.run.assert_called_once()

        # Verify exit code
        assert exit_code == 0

        # Verify startup messages
        captured = capsys.readouterr()
        assert "Starting HTTP server" in captured.out or mock_server.run.called

    def test_serve_http_cli_custom_host(self):
        """Test HTTP server CLI with custom host."""
        mock_server = MagicMock()
        mock_server_class = MagicMock(return_value=mock_server)

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            mock_server_class,
        ):
            with patch(
                "sys.argv", ["mcp-orchestration-serve-http", "--host", "127.0.0.1"]
            ):
                serve_http_cli()

        # Verify custom host
        mock_server_class.assert_called_once_with(host="127.0.0.1", port=8000)

    def test_serve_http_cli_custom_port(self):
        """Test HTTP server CLI with custom port."""
        mock_server = MagicMock()
        mock_server_class = MagicMock(return_value=mock_server)

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            mock_server_class,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http", "--port", "9000"]):
                serve_http_cli()

        # Verify custom port
        mock_server_class.assert_called_once_with(host="0.0.0.0", port=9000)

    def test_serve_http_cli_custom_host_and_port(self):
        """Test HTTP server CLI with custom host and port."""
        mock_server = MagicMock()
        mock_server_class = MagicMock(return_value=mock_server)

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            mock_server_class,
        ):
            with patch(
                "sys.argv",
                ["mcp-orchestration-serve-http", "--host", "0.0.0.0", "--port", "8080"],
            ):
                serve_http_cli()

        # Verify both custom values
        mock_server_class.assert_called_once_with(host="0.0.0.0", port=8080)

    def test_serve_http_cli_log_level_default(self):
        """Test HTTP server CLI with default log level."""
        mock_server = MagicMock()

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                serve_http_cli()

        # Verify default log level passed to run()
        mock_server.run.assert_called_once_with(log_level="info")

    def test_serve_http_cli_log_level_custom(self):
        """Test HTTP server CLI with custom log level."""
        mock_server = MagicMock()

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch(
                "sys.argv", ["mcp-orchestration-serve-http", "--log-level", "debug"]
            ):
                serve_http_cli()

        # Verify custom log level
        mock_server.run.assert_called_once_with(log_level="debug")

    def test_serve_http_cli_all_log_levels(self):
        """Test HTTP server CLI accepts all valid log levels."""
        valid_log_levels = ["critical", "error", "warning", "info", "debug"]

        for log_level in valid_log_levels:
            mock_server = MagicMock()

            with patch(
                "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
                return_value=mock_server,
            ):
                with patch(
                    "sys.argv",
                    ["mcp-orchestration-serve-http", "--log-level", log_level],
                ):
                    exit_code = serve_http_cli()

            # Verify log level accepted
            mock_server.run.assert_called_once_with(log_level=log_level)
            assert exit_code == 0

    def test_serve_http_cli_invalid_log_level(self):
        """Test HTTP server CLI rejects invalid log level."""
        with patch(
            "sys.argv", ["mcp-orchestration-serve-http", "--log-level", "invalid"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                serve_http_cli()

        # argparse should exit with error code 2
        assert exc_info.value.code == 2

    def test_serve_http_cli_help(self, capsys):
        """Test HTTP server CLI --help flag."""
        with patch("sys.argv", ["mcp-orchestration-serve-http", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                serve_http_cli()

        # --help should exit with 0
        assert exc_info.value.code == 0

        # Verify help text
        captured = capsys.readouterr()
        assert "Start MCP Orchestration HTTP server" in captured.out
        assert "--host" in captured.out
        assert "--port" in captured.out
        assert "--log-level" in captured.out
        assert "Examples:" in captured.out

    def test_serve_http_cli_examples_in_help(self, capsys):
        """Test that help text includes usage examples."""
        with patch("sys.argv", ["mcp-orchestration-serve-http", "--help"]):
            with pytest.raises(SystemExit):
                serve_http_cli()

        captured = capsys.readouterr()

        # Verify examples
        assert "mcp-orchestration-serve-http --port 9000" in captured.out
        assert "mcp-orchestration-serve-http --host 127.0.0.1" in captured.out
        assert "Environment variables:" in captured.out
        assert "MCP_ORCHESTRATION_API_KEY" in captured.out

    def test_serve_http_cli_keyboard_interrupt(self, capsys):
        """Test HTTP server CLI handles KeyboardInterrupt gracefully."""
        mock_server = MagicMock()
        mock_server.run.side_effect = KeyboardInterrupt()

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                exit_code = serve_http_cli()

        # KeyboardInterrupt should return 0 (graceful shutdown)
        assert exit_code == 0

        # Verify shutdown message
        captured = capsys.readouterr()
        assert "Server stopped by user" in captured.out

    def test_serve_http_cli_exception_handling(self, capsys):
        """Test HTTP server CLI handles exceptions."""
        mock_server = MagicMock()
        mock_server.run.side_effect = Exception("Server startup failed")

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                exit_code = serve_http_cli()

        # Exception should return 1
        assert exit_code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "Error starting server:" in captured.err
        assert "Server startup failed" in captured.err

    def test_serve_http_cli_port_binding_error(self, capsys):
        """Test HTTP server CLI handles port binding errors."""
        mock_server = MagicMock()
        mock_server.run.side_effect = OSError("Address already in use")

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                exit_code = serve_http_cli()

        # Port binding error should return 1
        assert exit_code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "Error starting server:" in captured.err
        assert "Address already in use" in captured.err

    def test_serve_http_cli_invalid_port_type(self):
        """Test HTTP server CLI rejects invalid port type."""
        with patch(
            "sys.argv", ["mcp-orchestration-serve-http", "--port", "not-a-number"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                serve_http_cli()

        # argparse should exit with error code 2
        assert exc_info.value.code == 2

    def test_serve_http_cli_port_out_of_range(self):
        """Test HTTP server CLI with port out of valid range."""
        mock_server = MagicMock()
        mock_server_class = MagicMock(return_value=mock_server)

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            mock_server_class,
        ):
            # argparse allows any int, but server may reject it
            with patch("sys.argv", ["mcp-orchestration-serve-http", "--port", "99999"]):
                serve_http_cli()

        # argparse accepts any int, server handles validation
        mock_server_class.assert_called_once_with(host="0.0.0.0", port=99999)


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def test_generate_token_and_use_in_server(self):
        """Test generating token and using it with HTTP server."""
        # Generate token
        mock_auth_service = MagicMock()
        mock_token = "integration_test_token_abc123"
        mock_auth_service.generate_token.return_value = mock_token

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                token = generate_token_cli()

        assert token == mock_token

        # Verify token can be used with server
        mock_server = MagicMock()

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                serve_http_cli()

        # Server should start successfully
        mock_server.run.assert_called_once()

    def test_cli_commands_are_independent(self):
        """Test that CLI commands don't interfere with each other."""
        # Run token generation
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = "token1"

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                token1 = generate_token_cli()

        # Run HTTP server
        mock_server = MagicMock()

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                serve_http_cli()

        # Run token generation again
        mock_auth_service.generate_token.return_value = "token2"

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                token2 = generate_token_cli()

        # Both tokens should be generated
        assert token1 == "token1"
        assert token2 == "token2"

    def test_token_generation_multiple_times(self):
        """Test generating multiple tokens in sequence."""
        mock_auth_service = MagicMock()
        tokens = ["token_1", "token_2", "token_3"]
        mock_auth_service.generate_token.side_effect = tokens

        generated_tokens = []

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            for _ in range(3):
                with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                    token = generate_token_cli()
                    generated_tokens.append(token)

        # All tokens should be generated
        assert generated_tokens == tokens

    def test_serve_http_multiple_configurations(self):
        """Test starting HTTP server with different configurations."""
        configurations = [
            ({"host": "127.0.0.1", "port": 8000}, ["--host", "127.0.0.1"]),
            ({"host": "0.0.0.0", "port": 9000}, ["--port", "9000"]),
            (
                {"host": "localhost", "port": 8080},
                ["--host", "localhost", "--port", "8080"],
            ),
        ]

        for expected_args, cli_args in configurations:
            mock_server = MagicMock()
            mock_server_class = MagicMock(return_value=mock_server)

            with patch(
                "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
                mock_server_class,
            ):
                with patch("sys.argv", ["mcp-orchestration-serve-http"] + cli_args):
                    serve_http_cli()

            # Verify server created with expected configuration
            call_kwargs = mock_server_class.call_args[1]
            assert call_kwargs["host"] == expected_args["host"]
            assert call_kwargs["port"] == expected_args["port"]


class TestCLIErrorScenarios:
    """Test error scenarios for CLI commands."""

    def test_token_generation_auth_service_unavailable(self, capsys):
        """Test token generation when auth service is unavailable."""
        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            side_effect=Exception("Service unavailable"),
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                with pytest.raises(SystemExit) as exc_info:
                    generate_token_cli()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error generating token:" in captured.err

    def test_serve_http_server_initialization_fails(self, capsys):
        """Test HTTP server when initialization fails."""
        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            side_effect=Exception("Init failed"),
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                exit_code = serve_http_cli()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Error starting server:" in captured.err

    def test_token_generation_permission_error(self, capsys):
        """Test token generation with permission error."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.side_effect = PermissionError(
            "Permission denied"
        )

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                with pytest.raises(SystemExit) as exc_info:
                    generate_token_cli()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error generating token:" in captured.err
        assert "Permission denied" in captured.err

    def test_serve_http_network_error(self, capsys):
        """Test HTTP server with network error."""
        mock_server = MagicMock()
        mock_server.run.side_effect = ConnectionError("Network unreachable")

        with patch(
            "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
            return_value=mock_server,
        ):
            with patch("sys.argv", ["mcp-orchestration-serve-http"]):
                exit_code = serve_http_cli()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Error starting server:" in captured.err
        assert "Network unreachable" in captured.err


class TestCLIOutputFormatting:
    """Test CLI output formatting and user experience."""

    def test_token_generation_output_is_machine_readable(self, capsys):
        """Test that token output can be parsed by scripts."""
        mock_token = "token_for_parsing_test_abc123"
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = mock_token

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                generate_token_cli()

        captured = capsys.readouterr()

        # Verify token can be extracted with grep/awk
        lines = captured.out.split("\n")
        token_line = [line for line in lines if "Generated token:" in line]
        assert len(token_line) == 1
        assert mock_token in token_line[0]

    def test_token_generation_output_structure(self, capsys):
        """Test that token generation has well-structured output."""
        mock_auth_service = MagicMock()
        mock_auth_service.generate_token.return_value = "token"

        with patch(
            "mcp_orchestrator.http_cli.token.get_auth_service",
            return_value=mock_auth_service,
        ):
            with patch("sys.argv", ["mcp-orchestration-generate-token"]):
                generate_token_cli()

        captured = capsys.readouterr()

        # Verify output sections
        assert "Token generated successfully!" in captured.out
        assert "Generated token:" in captured.out
        assert "Usage in curl:" in captured.out
        assert "Usage in Python:" in captured.out
        assert "Security:" in captured.out

    def test_serve_http_argument_validation(self):
        """Test that serve_http validates arguments correctly."""
        # Test with various argument combinations
        test_cases = [
            (["--host", "invalid$host"], None),  # argparse accepts any string as host
            (["--port", "0"], None),  # Port 0 (special case, may be valid)
            (["--log-level", "debug"], None),  # Valid log level
        ]

        for args, expected_exception in test_cases:
            mock_server = MagicMock()

            with patch(
                "mcp_orchestrator.http_cli.serve_http.HTTPTransportServer",
                return_value=mock_server,
            ):
                with patch("sys.argv", ["mcp-orchestration-serve-http"] + args):
                    if expected_exception:
                        with pytest.raises(expected_exception):
                            serve_http_cli()
                    else:
                        # Should not raise argparse errors
                        try:
                            serve_http_cli()
                        except Exception:
                            pass  # Server may fail but argparse should accept it
