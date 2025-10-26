"""Gmail API client for searching and retrieving messages."""

from dataclasses import dataclass


@dataclass
class EmailMessage:
    """Represents an email message with basic metadata."""

    subject: str
    sender: str
    date: str


class GmailClient:
    """Client for interacting with Gmail API to search and retrieve messages."""

    def __init__(self, service):
        self.service = service

    def search_messages(self, query: str, max_results: int = 50) -> list[EmailMessage]:
        """Search for messages in INBOX matching the given query.

        Args:
            query: Gmail search query string
            max_results: Maximum number of results to return

        Returns:
            List of EmailMessage objects
        """
        try:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, labelIds=["INBOX"], maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])

            email_messages = []
            for msg_ref in messages[:max_results]:
                msg = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg_ref["id"], format="metadata")
                    .execute()
                )

                headers = msg["payload"]["headers"]
                email_messages.append(
                    EmailMessage(
                        subject=self._get_header_value(headers, "Subject"),
                        sender=self._get_header_value(headers, "From"),
                        date=self._get_header_value(headers, "Date"),
                    )
                )

            return email_messages

        except Exception:
            return []

    def _get_header_value(self, headers: list[dict], name: str) -> str:
        """Extract header value by name from headers list."""
        for header in headers:
            if header["name"] == name:
                return header["value"]
        return ""
