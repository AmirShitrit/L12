# Gmail AI Agent

An intelligent agent that connects to Gmail and searches emails using natural language queries powered by Google Gemini.

## Features

- Natural language email search using Google Gemini AI
- Secure OAuth 2.0 authentication with Gmail
- Encrypted token storage for credential security
- Formatted table display of search results
- Support for both stdin and interactive input
- Inbox-focused search for relevant results

## Requirements

- Python 3.10 or higher
- Gmail account with API access enabled
- Google API credentials (OAuth 2.0)
- Google Gemini API key

## Installation

### 1. Clone the repository

```bash
cd /path/to/project
```

### 2. Install dependencies using uv

```bash
uv pip install -e ".[dev]"
```

Or using task:

```bash
task install
```

### 3. Set up Gmail API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop application type)
5. Copy the Client ID and Client Secret (you'll add these to .env file)

### 4. Get Google Gemini API key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Set it as an environment variable

### 5. Set up environment variables

Create a `.env` file in the project root (or copy from `.env.example`):

```bash
# Encryption key for token storage (already generated for you)
GMAIL_AGENT_KEY=<token goes here>

# Google Gemini API key (ADD YOUR KEY HERE)
GOOGLE_API_KEY=your-gemini-api-key-here

# Google OAuth 2.0 credentials (from Google Cloud Console)
GOOGLE_CLIENT_ID=<client ID goes here>
GOOGLE_CLIENT_SECRET=<secret goes here>
```

**Note:** The `.env` file is automatically loaded when you run the agent - no need to manually source it!

## Usage

### Interactive Mode

Run the agent and enter your query when prompted:

```bash
python -m gmail_agent.main
```

Or using task:

```bash
task agent
```

Example:
```
Enter your search query: show me unread emails from Google last week
```

### Stdin Mode

Pipe your query directly:

```bash
echo "show me unread messages from Amazon" | python -m gmail_agent.main
```

Or using task:

```bash
task search QUERY="show me unread messages from Amazon"
```

Ready made example:
```bash
task search-example
```

### Example Queries

- "show me unread emails"
- "messages from Google last week"
- "emails from support@example.com with attachments"
- "unread messages about invoice from last month"
- "emails with 'meeting' in the subject"

## Query Syntax

The agent converts natural language to Gmail search operators:

- `from:sender` - emails from specific sender
- `to:recipient` - emails to specific recipient
- `subject:text` - emails with text in subject
- `is:unread` - unread emails
- `is:starred` - starred emails
- `has:attachment` - emails with attachments
- `newer_than:Xd` - emails from last X days
- `older_than:Xd` - emails older than X days

## Development

### Run Tests

```bash
pytest
```

Or with verbose output:

```bash
task test-verbose
```

### Run Tests with Coverage

```bash
task test-coverage
```

### Project Structure

```
gmail_agent/
├── __init__.py
├── auth.py           # OAuth authentication and token management
├── nlp_parser.py     # Natural language query parser
├── gmail_client.py   # Gmail API client
├── display.py        # Results formatting and display
└── main.py           # Main orchestration

tests/
├── test_auth.py
├── test_nlp_parser.py
├── test_gmail_client.py
├── test_display.py
└── test_main.py
```

## Security

- OAuth tokens are stored encrypted using the `cryptography` library
- Encryption key must be set via `GMAIL_AGENT_KEY` environment variable
- OAuth tokens are saved in `token.enc` (encrypted)
- OAuth credentials (client ID and secret) are stored in environment variables
- Never commit `token.enc` or `.env` to version control (already in .gitignore)

## First Run

On first run, the agent will:

1. Open your browser for Gmail OAuth authorization
2. Ask you to grant read-only access to your Gmail
3. Save the encrypted token to `token.enc`
4. Subsequent runs will reuse the saved token

## Troubleshooting

### "GMAIL_AGENT_KEY environment variable must be set"

Make sure you have a `.env` file in the project root with the encryption key:

```bash
GMAIL_AGENT_KEY=your-secure-key-here
```

### "GOOGLE_API_KEY must be provided"

Add your Gemini API key to the `.env` file:

```bash
GOOGLE_API_KEY=your-api-key-here
```

### "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables must be set"

Make sure you've added the OAuth credentials to your `.env` file:

```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

The `.env` file is automatically loaded - just make sure it exists in the project root directory.

### Token decryption fails

If you changed the `GMAIL_AGENT_KEY`, delete `token.enc` and re-authenticate.

## Future Enhancements

- Support for other Gmail labels/folders
- Scheduled or automatic runs
- Additional actions (mark as read, archive, forward, summarize)
- Web or chat-based interface
- Configuration file for default settings
- Email response capabilities

## License

This project is for educational purposes as part of an AI course assignment.
