"""Tests for Gmail client module."""

from unittest.mock import Mock, patch

import pytest

from gmail_agent.gmail_client import GmailClient, EmailMessage


class TestGmailClient:
    """Test cases for GmailClient class."""

    @pytest.fixture
    def mock_service(self):
        """Create a mock Gmail service."""
        service = Mock()
        return service

    @pytest.fixture
    def client(self, mock_service):
        """Create a Gmail client with mocked service."""
        return GmailClient(mock_service)

    def test_client_initialization(self, mock_service):
        """Test client initializes with service."""
        client = GmailClient(mock_service)
        assert client.service == mock_service

    def test_search_messages_returns_empty_list_when_no_results(self, client, mock_service):
        """Test search returns empty list when no messages match."""
        mock_service.users().messages().list().execute.return_value = {}

        results = client.search_messages("is:unread")
        assert results == []

    def test_search_messages_fetches_message_details(self, client, mock_service):
        """Test search fetches full message details for each result."""
        mock_list_response = {
            "messages": [{"id": "msg1"}, {"id": "msg2"}]
        }

        mock_msg1 = {
            "id": "msg1",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender1@example.com"},
                    {"name": "Subject", "value": "Test Subject 1"},
                    {"name": "Date", "value": "Mon, 1 Jan 2024 10:00:00 +0000"},
                ]
            },
        }

        mock_msg2 = {
            "id": "msg2",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender2@example.com"},
                    {"name": "Subject", "value": "Test Subject 2"},
                    {"name": "Date", "value": "Tue, 2 Jan 2024 11:00:00 +0000"},
                ]
            },
        }

        mock_service.users().messages().list().execute.return_value = mock_list_response
        mock_service.users().messages().get().execute.side_effect = [mock_msg1, mock_msg2]

        results = client.search_messages("is:unread")

        assert len(results) == 2
        assert results[0].sender == "sender1@example.com"
        assert results[0].subject == "Test Subject 1"
        assert results[1].sender == "sender2@example.com"
        assert results[1].subject == "Test Subject 2"

    def test_search_messages_with_max_results_limit(self, client, mock_service):
        """Test search respects max_results parameter."""
        mock_list_response = {
            "messages": [{"id": f"msg{i}"} for i in range(5)]
        }

        mock_service.users().messages().list().execute.return_value = mock_list_response

        mock_service.users().messages().get().execute.return_value = {
            "id": "msg1",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Test"},
                    {"name": "Date", "value": "Mon, 1 Jan 2024 10:00:00 +0000"},
                ]
            },
        }

        results = client.search_messages("is:unread", max_results=3)

        assert len(results) == 3

    def test_search_messages_only_searches_inbox(self, client, mock_service):
        """Test search only looks in INBOX label."""
        mock_service.users().messages().list().execute.return_value = {}

        client.search_messages("is:unread")

        call_args = mock_service.users().messages().list.call_args
        assert call_args[1]["labelIds"] == ["INBOX"]

    def test_get_header_value_returns_correct_value(self, client):
        """Test helper method extracts correct header value."""
        headers = [
            {"name": "From", "value": "sender@example.com"},
            {"name": "Subject", "value": "Test Subject"},
            {"name": "Date", "value": "Mon, 1 Jan 2024 10:00:00 +0000"},
        ]

        assert client._get_header_value(headers, "From") == "sender@example.com"
        assert client._get_header_value(headers, "Subject") == "Test Subject"
        assert client._get_header_value(headers, "Date") == "Mon, 1 Jan 2024 10:00:00 +0000"

    def test_get_header_value_returns_empty_string_if_not_found(self, client):
        """Test helper method returns empty string for missing headers."""
        headers = [{"name": "From", "value": "sender@example.com"}]

        assert client._get_header_value(headers, "Subject") == ""
        assert client._get_header_value(headers, "NonExistent") == ""


class TestEmailMessage:
    """Test cases for EmailMessage dataclass."""

    def test_email_message_creation(self):
        """Test EmailMessage can be created with all fields."""
        msg = EmailMessage(
            subject="Test Subject",
            sender="sender@example.com",
            date="Mon, 1 Jan 2024 10:00:00 +0000",
        )

        assert msg.subject == "Test Subject"
        assert msg.sender == "sender@example.com"
        assert msg.date == "Mon, 1 Jan 2024 10:00:00 +0000"

    def test_email_message_equality(self):
        """Test EmailMessage equality comparison."""
        msg1 = EmailMessage("Subject", "sender@example.com", "Date")
        msg2 = EmailMessage("Subject", "sender@example.com", "Date")
        msg3 = EmailMessage("Different", "sender@example.com", "Date")

        assert msg1 == msg2
        assert msg1 != msg3
