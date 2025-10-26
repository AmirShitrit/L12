"""Tests for main orchestration module."""

import sys
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from gmail_agent.main import get_user_query, run_agent


class TestGetUserQuery:
    """Test cases for get_user_query function."""

    def test_get_query_from_stdin(self):
        """Test reading query from stdin."""
        with patch("sys.stdin.isatty", return_value=False):
            with patch("sys.stdin.read", return_value="test query from stdin\n"):
                query = get_user_query()
                assert query == "test query from stdin"

    def test_get_query_from_interactive_input(self):
        """Test reading query from interactive input."""
        with patch("sys.stdin.isatty", return_value=True):
            with patch("builtins.input", return_value="test interactive query"):
                query = get_user_query()
                assert query == "test interactive query"

    def test_get_query_strips_whitespace(self):
        """Test query whitespace is stripped."""
        with patch("sys.stdin.isatty", return_value=False):
            with patch("sys.stdin.read", return_value="  query with spaces  \n"):
                query = get_user_query()
                assert query == "query with spaces"


class TestRunAgent:
    """Test cases for run_agent function."""

    @pytest.fixture
    def mock_components(self):
        """Create mocked components for the agent."""
        mock_service = Mock()
        mock_parser = Mock()
        mock_client = Mock()

        return {
            "service": mock_service,
            "parser": mock_parser,
            "client": mock_client,
        }

    def test_run_agent_with_valid_query(self, mock_components):
        """Test agent runs successfully with valid query."""
        user_query = "show me unread emails"
        gmail_query = "is:unread"

        mock_components["parser"].parse.return_value = gmail_query
        mock_components["client"].search_messages.return_value = []

        with patch("gmail_agent.main.get_gmail_service") as mock_get_service:
            with patch("gmail_agent.main.GmailQueryParser") as MockParser:
                with patch("gmail_agent.main.GmailClient") as MockClient:
                    with patch("gmail_agent.main.display_results") as mock_display:
                        mock_get_service.return_value = mock_components["service"]
                        MockParser.return_value = mock_components["parser"]
                        MockClient.return_value = mock_components["client"]

                        run_agent(user_query)

                        mock_components["parser"].parse.assert_called_once_with(user_query)
                        mock_components["client"].search_messages.assert_called_once_with(
                            gmail_query, max_results=50
                        )
                        mock_display.assert_called_once()

    def test_run_agent_creates_gmail_service(self, mock_components):
        """Test agent creates Gmail service with correct parameters."""
        with patch("gmail_agent.main.get_gmail_service") as mock_get_service:
            with patch("gmail_agent.main.GmailQueryParser"):
                with patch("gmail_agent.main.GmailClient"):
                    with patch("gmail_agent.main.display_results"):
                        mock_get_service.return_value = mock_components["service"]

                        run_agent("test query")

                        mock_get_service.assert_called_once()

    def test_run_agent_passes_messages_to_display(self, mock_components):
        """Test agent passes retrieved messages to display function."""
        from gmail_agent.gmail_client import EmailMessage

        test_messages = [
            EmailMessage("Subject 1", "sender1@example.com", "Date 1"),
            EmailMessage("Subject 2", "sender2@example.com", "Date 2"),
        ]

        mock_components["parser"].parse.return_value = "is:unread"
        mock_components["client"].search_messages.return_value = test_messages

        with patch("gmail_agent.main.get_gmail_service") as mock_get_service:
            with patch("gmail_agent.main.GmailQueryParser") as MockParser:
                with patch("gmail_agent.main.GmailClient") as MockClient:
                    with patch("gmail_agent.main.display_results") as mock_display:
                        mock_get_service.return_value = mock_components["service"]
                        MockParser.return_value = mock_components["parser"]
                        MockClient.return_value = mock_components["client"]

                        run_agent("test query")

                        mock_display.assert_called_once_with(test_messages)

    def test_run_agent_with_custom_token_file(self, mock_components):
        """Test agent accepts custom token file path."""
        with patch("gmail_agent.main.get_gmail_service") as mock_get_service:
            with patch("gmail_agent.main.GmailQueryParser"):
                with patch("gmail_agent.main.GmailClient"):
                    with patch("gmail_agent.main.display_results"):
                        mock_get_service.return_value = mock_components["service"]

                        run_agent("test query", token_file="custom_token.enc")

                        call_args = mock_get_service.call_args
                        assert call_args[1]["token_file"] == "custom_token.enc"
