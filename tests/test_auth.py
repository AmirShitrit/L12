"""Tests for authentication module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from gmail_agent.auth import TokenManager, get_gmail_service


class TestTokenManager:
    """Test cases for TokenManager class."""

    @pytest.fixture
    def temp_token_file(self):
        """Create a temporary token file for testing."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".enc") as f:
            token_path = f.name
        yield token_path
        if os.path.exists(token_path):
            os.unlink(token_path)

    @pytest.fixture
    def encryption_key(self):
        """Provide a test encryption key."""
        return "test_encryption_key_32_chars!!"

    def test_token_manager_init_with_env_key(self, temp_token_file, encryption_key):
        """Test TokenManager initializes with encryption key from environment."""
        with patch.dict(os.environ, {"GMAIL_AGENT_KEY": encryption_key}):
            manager = TokenManager(temp_token_file)
            assert manager.token_path == Path(temp_token_file)
            assert manager.encryption_key is not None

    def test_token_manager_init_without_env_key(self, temp_token_file):
        """Test TokenManager raises error if encryption key is not in environment."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GMAIL_AGENT_KEY"):
                TokenManager(temp_token_file)

    def test_encrypt_and_decrypt_token(self, temp_token_file, encryption_key):
        """Test token encryption and decryption works correctly."""
        with patch.dict(os.environ, {"GMAIL_AGENT_KEY": encryption_key}):
            manager = TokenManager(temp_token_file)
            test_token = {"token": "test_access_token", "refresh_token": "test_refresh"}

            encrypted = manager._encrypt_token(test_token)
            assert encrypted != test_token
            assert isinstance(encrypted, bytes)

            decrypted = manager._decrypt_token(encrypted)
            assert decrypted == test_token

    def test_save_and_load_token(self, temp_token_file, encryption_key):
        """Test saving and loading encrypted tokens from file."""
        with patch.dict(os.environ, {"GMAIL_AGENT_KEY": encryption_key}):
            manager = TokenManager(temp_token_file)
            test_token = {"token": "test_access_token", "refresh_token": "test_refresh"}

            manager.save_token(test_token)
            assert os.path.exists(temp_token_file)

            loaded_token = manager.load_token()
            assert loaded_token == test_token

    def test_load_token_returns_none_if_not_exists(self, temp_token_file, encryption_key):
        """Test load_token returns None if token file doesn't exist."""
        with patch.dict(os.environ, {"GMAIL_AGENT_KEY": encryption_key}):
            manager = TokenManager(temp_token_file)
            token = manager.load_token()
            assert token is None

    def test_load_token_returns_none_on_decryption_failure(
        self, temp_token_file, encryption_key
    ):
        """Test load_token returns None if decryption fails."""
        with patch.dict(os.environ, {"GMAIL_AGENT_KEY": encryption_key}):
            manager = TokenManager(temp_token_file)

            with open(temp_token_file, "wb") as f:
                f.write(b"invalid_encrypted_data")

            token = manager.load_token()
            assert token is None


class TestGetGmailService:
    """Test cases for get_gmail_service function."""

    @pytest.fixture
    def mock_credentials(self):
        """Create mock credentials."""
        creds = Mock()
        creds.valid = True
        creds.expired = False
        creds.refresh_token = "test_refresh"
        return creds

    def test_get_gmail_service_with_valid_cached_token(
        self, mock_credentials, tmp_path
    ):
        """Test service creation with valid cached token."""
        token_file = tmp_path / "token.enc"
        encryption_key = "test_encryption_key_32_chars!!"

        with patch.dict(os.environ, {"GMAIL_AGENT_KEY": encryption_key}):
            with patch("gmail_agent.auth.TokenManager") as MockTokenManager:
                with patch("gmail_agent.auth.build") as mock_build:
                    mock_manager = MockTokenManager.return_value
                    mock_manager.load_token.return_value = {
                        "token": "access_token",
                        "refresh_token": "refresh_token",
                    }

                    with patch(
                        "gmail_agent.auth.Credentials.from_authorized_user_info",
                        return_value=mock_credentials,
                    ):
                        service = get_gmail_service(str(token_file))

                        assert service is not None
                        mock_build.assert_called_once()

    def test_get_gmail_service_requires_oauth_credentials(self, tmp_path):
        """Test service raises error if OAuth credentials not in environment."""
        token_file = tmp_path / "token.enc"
        encryption_key = "test_encryption_key_32_chars!!"

        with patch.dict(
            os.environ,
            {"GMAIL_AGENT_KEY": encryption_key},
            clear=True
        ):
            with patch("gmail_agent.auth.TokenManager") as MockTokenManager:
                mock_manager = MockTokenManager.return_value
                mock_manager.load_token.return_value = None

                with pytest.raises(ValueError, match="GOOGLE_CLIENT_ID"):
                    get_gmail_service(str(token_file))
