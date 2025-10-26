"""Tests for NLP parser module."""

from unittest.mock import Mock, patch

import pytest

from gmail_agent.nlp_parser import GmailQueryParser


class TestGmailQueryParser:
    """Test cases for GmailQueryParser class."""

    @pytest.fixture
    def parser(self):
        """Create a parser instance with mocked Gemini model."""
        with patch("gmail_agent.nlp_parser.genai.GenerativeModel") as mock_model_class:
            mock_model = Mock()
            mock_model_class.return_value = mock_model
            parser = GmailQueryParser(api_key="test_api_key")
            parser.model = mock_model
            return parser

    def test_parser_initialization(self):
        """Test parser initializes with API key."""
        with patch("gmail_agent.nlp_parser.genai.configure") as mock_configure:
            with patch("gmail_agent.nlp_parser.genai.GenerativeModel"):
                parser = GmailQueryParser(api_key="test_key")
                mock_configure.assert_called_once_with(api_key="test_key")
                assert parser is not None

    def test_parse_simple_unread_query(self, parser):
        """Test parsing simple unread emails query."""
        mock_response = Mock()
        mock_response.text = "is:unread"
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("show me unread messages")
        assert query == "is:unread"
        parser.model.generate_content.assert_called_once()

    def test_parse_sender_query(self, parser):
        """Test parsing query with sender filter."""
        mock_response = Mock()
        mock_response.text = "from:google.com"
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("emails from Google")
        assert query == "from:google.com"

    def test_parse_date_range_query(self, parser):
        """Test parsing query with date range."""
        mock_response = Mock()
        mock_response.text = "newer_than:7d"
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("messages from last week")
        assert query == "newer_than:7d"

    def test_parse_complex_query(self, parser):
        """Test parsing complex multi-criteria query."""
        mock_response = Mock()
        mock_response.text = "from:amazon.com is:unread newer_than:7d"
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("show me unread emails from Amazon last week")
        assert query == "from:amazon.com is:unread newer_than:7d"

    def test_parse_with_subject_filter(self, parser):
        """Test parsing query with subject filter."""
        mock_response = Mock()
        mock_response.text = "subject:invoice"
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("emails with invoice in subject")
        assert query == "subject:invoice"

    def test_parse_strips_extra_whitespace(self, parser):
        """Test parser strips extra whitespace from result."""
        mock_response = Mock()
        mock_response.text = "  is:unread  from:google.com  "
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("unread from google")
        assert query == "is:unread  from:google.com"

    def test_parse_handles_empty_response(self, parser):
        """Test parser handles empty response gracefully."""
        mock_response = Mock()
        mock_response.text = ""
        parser.model.generate_content.return_value = mock_response

        query = parser.parse("invalid query")
        assert query == ""

    def test_parse_from_env_api_key(self):
        """Test parser can initialize from environment variable."""
        with patch.dict("os.environ", {"GOOGLE_API_KEY": "env_key"}):
            with patch("gmail_agent.nlp_parser.genai.configure") as mock_configure:
                with patch("gmail_agent.nlp_parser.genai.GenerativeModel"):
                    parser = GmailQueryParser()
                    mock_configure.assert_called_once_with(api_key="env_key")

    def test_parse_raises_error_without_api_key(self):
        """Test parser raises error if no API key provided."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
                GmailQueryParser()
