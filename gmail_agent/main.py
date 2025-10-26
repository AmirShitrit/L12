"""Main orchestration for the Gmail AI agent."""

import sys

from dotenv import load_dotenv

from gmail_agent.auth import get_gmail_service
from gmail_agent.display import display_results
from gmail_agent.gmail_client import GmailClient
from gmail_agent.nlp_parser import GmailQueryParser

load_dotenv()


def get_user_query() -> str:
    """Get user query from stdin or interactive input.

    Returns:
        User query string with whitespace stripped
    """
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    else:
        return input("Enter your search query: ").strip()


def run_agent(
    user_query: str,
    token_file: str = "token.enc",
    max_results: int = 50,
) -> None:
    """Run the Gmail agent with the given query.

    Args:
        user_query: Natural language search query from user
        token_file: Path to encrypted token file
        max_results: Maximum number of results to retrieve
    """
    service = get_gmail_service(token_file=token_file)

    parser = GmailQueryParser()

    gmail_query = parser.parse(user_query)
    print(f"Gmail search query: {gmail_query}\n")

    client = GmailClient(service)
    messages = client.search_messages(gmail_query, max_results=max_results)

    display_results(messages)


def main() -> None:
    """Main entry point for the Gmail agent."""
    user_query = get_user_query()

    if not user_query:
        print("Error: No query provided.")
        sys.exit(1)

    run_agent(user_query)


if __name__ == "__main__":
    main()
