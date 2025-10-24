# AI Gmail Agent – Requirements Specification

## 1. Overview
The goal of this project is to develop a simple AI agent that connects to the user’s Gmail account, searches for emails in the Inbox according to criteria expressed in natural language, and displays the matching messages in a formatted table.  
This is the first version of the agent, designed for simplicity while keeping future extensibility in mind.

---

## 2. Objectives
- Allow the agent to connect securely to Gmail using the official Gmail API (OAuth 2.0).  
- Accept a natural language prompt describing the search criteria.  
- Retrieve and list matching emails from the Inbox.  
- Display results (subject, sender, date) in a nicely formatted table in the console.  
- Store credentials securely for reuse between sessions.

---

## 3. Functional Requirements

### 3.1 Authentication
- Use Google’s OAuth 2.0 flow to obtain access to Gmail.  
- Save the access/refresh token locally in an encrypted file (`token.enc`).  
- Encryption key is stored in an environment variable (e.g., `GMAIL_AGENT_KEY`).  
- On startup, if `token.enc` exists and is decryptable, reuse the credentials; otherwise, prompt for authentication.

### 3.2 Natural Language Query
- The user enters a natural language prompt (e.g., “show me unread messages from Google last week”).  
- The agent interprets the prompt and converts it into a Gmail search query string (e.g., `from:google.com is:unread newer_than:7d`).  
- Only messages from the **Inbox** are considered in this version.

### 3.3 Message Retrieval
- Use the Gmail API to fetch matching messages (message metadata only).  
- Retrieve and display the following fields for each message:
  - **Subject**
  - **Sender**
  - **Date**

### 3.4 Output
- Print the results to the console as a formatted table.  
- If no messages match, display a friendly “No results found” message.

### 3.5 Execution Mode
- The agent runs manually via a CLI command (e.g., `python gmail_agent.py`).  
- The user is prompted to input a natural language search query at runtime.
- Alternatively, it should be possible to "pipe" the search query via stdin.

---

## 4. Non-Functional Requirements

### 4.1 Security
- No plain-text credential storage.  
- Use encryption for any stored tokens.  
- Use environment variables for secrets and keys.  
- Comply with Google API security best practices.

### 4.2 Extensibility
- Code should be modular enough to support future extensions (e.g., actions such as labeling, forwarding, summarizing).  
- Future versions may add configuration files or plugin-based actions.

### 4.3 Maintainability
- Code will follow Python best practices (PEP 8).  
- Include clear inline comments and docstrings.

---

## 5. Tech Stack

| Component | Choice |
|------------|---------|
| Language | Python |
| Gmail Access | Gmail API (via `google-api-python-client`) |
| Authentication | OAuth 2.0 |
| Token Encryption | Python `cryptography` library |
| Console Table Formatting | `tabulate` or similar package |

---

## 6. Future Enhancements
- Support for other Gmail labels/folders.  
- Automatic or scheduled runs.  
- Richer criteria (date ranges, attachments, etc.).  
- Additional actions: mark as read, label, archive, forward, summarize, respond.  
- Web-based or chat-style interface.
