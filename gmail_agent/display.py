"""Display formatter for email messages."""

from tabulate import tabulate

from gmail_agent.gmail_client import EmailMessage


def format_messages(messages: list[EmailMessage]) -> str:
    """Format email messages as a table string.

    Args:
        messages: List of EmailMessage objects to format

    Returns:
        Formatted table string, or "No results found." if list is empty
    """
    if not messages:
        return "No results found."

    table_data = [
        [msg.subject, msg.sender, msg.date]
        for msg in messages
    ]

    headers = ["Subject", "Sender", "Date"]

    return tabulate(table_data, headers=headers, tablefmt="grid")


def display_results(messages: list[EmailMessage]) -> None:
    """Print formatted email messages to stdout.

    Args:
        messages: List of EmailMessage objects to display
    """
    print(format_messages(messages))
