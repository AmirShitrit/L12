"""Tests for display formatter module."""

from io import StringIO
from unittest.mock import patch

import pytest

from gmail_agent.display import format_messages, display_results
from gmail_agent.gmail_client import EmailMessage


class TestFormatMessages:
    """Test cases for format_messages function."""

    def test_format_empty_list(self):
        """Test formatting empty message list returns appropriate message."""
        result = format_messages([])
        assert result == "No results found."

    def test_format_single_message(self):
        """Test formatting a single message."""
        messages = [
            EmailMessage(
                subject="Test Subject",
                sender="sender@example.com",
                date="Mon, 1 Jan 2024 10:00:00 +0000",
            )
        ]

        result = format_messages(messages)

        assert "Test Subject" in result
        assert "sender@example.com" in result
        assert "Mon, 1 Jan 2024 10:00:00 +0000" in result
        assert "Subject" in result
        assert "Sender" in result
        assert "Date" in result

    def test_format_multiple_messages(self):
        """Test formatting multiple messages."""
        messages = [
            EmailMessage("Subject 1", "sender1@example.com", "Date 1"),
            EmailMessage("Subject 2", "sender2@example.com", "Date 2"),
            EmailMessage("Subject 3", "sender3@example.com", "Date 3"),
        ]

        result = format_messages(messages)

        assert "Subject 1" in result
        assert "Subject 2" in result
        assert "Subject 3" in result
        assert "sender1@example.com" in result
        assert "sender2@example.com" in result
        assert "sender3@example.com" in result

    def test_format_includes_table_headers(self):
        """Test formatted output includes proper headers."""
        messages = [EmailMessage("Test", "test@example.com", "Date")]

        result = format_messages(messages)

        assert "Subject" in result
        assert "Sender" in result
        assert "Date" in result

    def test_format_uses_grid_table_format(self):
        """Test formatted output uses grid table format."""
        messages = [EmailMessage("Test", "test@example.com", "Date")]

        result = format_messages(messages)

        assert "+" in result or "|" in result or "-" in result


class TestDisplayResults:
    """Test cases for display_results function."""

    def test_display_results_prints_to_stdout(self):
        """Test display_results prints formatted output to stdout."""
        messages = [EmailMessage("Test", "test@example.com", "Date")]

        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_results(messages)
            output = fake_out.getvalue()

            assert "Test" in output
            assert "test@example.com" in output

    def test_display_results_with_empty_list(self):
        """Test display_results handles empty list properly."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_results([])
            output = fake_out.getvalue()

            assert "No results found." in output

    def test_display_results_with_multiple_messages(self):
        """Test display_results prints all messages."""
        messages = [
            EmailMessage("Subject 1", "sender1@example.com", "Date 1"),
            EmailMessage("Subject 2", "sender2@example.com", "Date 2"),
        ]

        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_results(messages)
            output = fake_out.getvalue()

            assert "Subject 1" in output
            assert "Subject 2" in output
            assert "sender1@example.com" in output
            assert "sender2@example.com" in output
