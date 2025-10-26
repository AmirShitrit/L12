"""Gmail authentication and token management."""

import json
import os
from pathlib import Path

from cryptography.fernet import Fernet
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class TokenManager:
    """Manages encrypted storage and retrieval of OAuth tokens."""

    def __init__(self, token_path: str):
        self.token_path = Path(token_path)
        encryption_key = os.getenv("GMAIL_AGENT_KEY")
        if not encryption_key:
            raise ValueError(
                "GMAIL_AGENT_KEY environment variable must be set for token encryption"
            )
        self.encryption_key = self._derive_key(encryption_key)

    def _derive_key(self, key_string: str) -> bytes:
        """Derive a valid Fernet key from the encryption key string."""
        import base64
        import hashlib

        key_bytes = hashlib.sha256(key_string.encode()).digest()
        return base64.urlsafe_b64encode(key_bytes)

    def _encrypt_token(self, token_data: dict) -> bytes:
        """Encrypt token data."""
        fernet = Fernet(self.encryption_key)
        token_json = json.dumps(token_data)
        return fernet.encrypt(token_json.encode())

    def _decrypt_token(self, encrypted_data: bytes) -> dict:
        """Decrypt token data."""
        fernet = Fernet(self.encryption_key)
        decrypted_bytes = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_bytes.decode())

    def save_token(self, token_data: dict) -> None:
        """Save encrypted token to file."""
        encrypted = self._encrypt_token(token_data)
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.token_path, "wb") as f:
            f.write(encrypted)

    def load_token(self) -> dict | None:
        """Load and decrypt token from file. Returns None if file doesn't exist or decryption fails."""
        if not self.token_path.exists():
            return None

        try:
            with open(self.token_path, "rb") as f:
                encrypted_data = f.read()
            return self._decrypt_token(encrypted_data)
        except Exception:
            return None


def get_gmail_service(token_file: str = "token.enc"):
    """Create and return Gmail API service, handling OAuth authentication."""
    token_manager = TokenManager(token_file)
    creds = None

    token_data = token_manager.load_token()
    if token_data:
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

            if not client_id or not client_secret:
                raise ValueError(
                    "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables must be set"
                )

            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost"],
                }
            }

            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        token_manager.save_token(json.loads(creds.to_json()))

    return build("gmail", "v1", credentials=creds)
