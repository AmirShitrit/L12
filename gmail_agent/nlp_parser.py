"""Natural language to Gmail query parser using Google Gemini."""

import os

import google.generativeai as genai


class GmailQueryParser:
    """Parses natural language queries into Gmail search query strings using Gemini."""

    SYSTEM_PROMPT = """You are a Gmail search query generator. Convert natural language requests into Gmail search query syntax.

Gmail search operators:
- from:sender - emails from specific sender (e.g., from:google.com, from:support@amazon.com)
- to:recipient - emails to specific recipient
- subject:text - emails with text in subject
- is:unread - unread emails
- is:read - read emails
- is:starred - starred emails
- has:attachment - emails with attachments
- newer_than:Xd - emails newer than X days (e.g., newer_than:7d for last week)
- older_than:Xd - emails older than X days
- after:YYYY/MM/DD - emails after specific date
- before:YYYY/MM/DD - emails before specific date

Examples:
Input: "show me unread emails from Google"
Output: from:google.com is:unread

Input: "messages from Amazon last week"
Output: from:amazon.com newer_than:7d

Input: "unread emails with attachments from support@company.com"
Output: from:support@company.com is:unread has:attachment

Input: "emails about invoice from last month"
Output: subject:invoice newer_than:30d

Only output the Gmail search query, nothing else. Do not include explanations or extra text."""

    def __init__(self, api_key: str | None = None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY must be provided or set as environment variable"
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def parse(self, natural_language_query: str) -> str:
        """Convert natural language query to Gmail search query string."""
        prompt = f"{self.SYSTEM_PROMPT}\n\nInput: {natural_language_query}\nOutput:"

        response = self.model.generate_content(prompt)
        return response.text.strip()
