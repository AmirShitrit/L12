# AI Gmail Agent – Requirements Specification

## 1. Overview

The goal of this project is to develop a simple AI agent that connects to the user’s Gmail account, searches for emails
in the Inbox according to criteria expressed in natural language, and displays the matching messages in a formatted
table.  
This is the first version of the agent, designed for simplicity while keeping future extensibility in mind.

---

## 2. Objectives

- Connect securely to Gmail using the official Gmail API (OAuth 2.0).
- Accept a natural language prompt describing the search criteria (from stdin or user input).
- Parse the natural language prompt using **Google ADK** for accurate intent extraction.
- Retrieve and list matching emails from the Inbox.
- Display results (subject, sender, date) in a formatted table in the console.
- Store credentials securely for reuse between sessions.

---

## 3. Functional Requirements

### 3.1 Authentication

- Use Google’s OAuth 2.0 flow to obtain access to Gmail.
- Save the access/refresh token locally in an encrypted file (`token.enc`).
- The encryption key is stored in an environment variable (e.g., `GMAIL_AGENT_KEY`).
- On startup, if `token.enc` exists and is decryptable, reuse the credentials; otherwise, prompt for authentication.

### 3.2 Natural Language Query

- The user provides a prompt describing what to look for, such as:
  > show me unread messages from Google last week
- The agent uses **Google ADK** to interpret the natural language and convert it into a Gmail search query string (e.g.,
  `from:google.com is:unread newer_than:7d`).
- Only messages from the **Inbox** are considered in this version.

### 3.3 Message Retrieval

- Use the Gmail API to fetch matching messages (metadata only).
- Retrieve and display:
    - **Subject**
    - **Sender**
    - **Date**

### 3.4 Output

- Print results as a **formatted table** in the console.
- If no messages match, display:
  > No results found.

### 3.5 Execution Mode

- The agent runs manually from the terminal.
- It accepts the prompt via:
    - **stdin** (e.g., `echo "show me unread emails from Amazon" | python gmail_agent.py`), or
    - Interactive input when no stdin is provided.
- Generate a Taskfile.yml (gotasks) for easy triggering of the agent.

---

## 4. Non-Functional Requirements

### 4.1 Security

- No plain-text credential storage.
- Use encryption for stored tokens.
- Use environment variables for secrets and keys.
- Follow Google API and OAuth security best practices.

### 4.2 Extensibility

- Modular design to support future extensions (e.g., label, forward, summarize actions).
- Easy integration of new AI models or parsing components.

### 4.3 Maintainability

- Code should be **self-explanatory** and readable.
- Use clear variable names, modular functions, and logical structure instead of excessive comments.
- Adhere to Python best practices (PEP 8).

---

## 5. Tech Stack

| Component                | Choice                                     |
|--------------------------|--------------------------------------------|
| Language                 | Python                                     |
| Gmail Access             | Gmail API (via `google-api-python-client`) |
| Authentication           | OAuth 2.0                                  |
| Token Encryption         | Python `cryptography` library              |
| Natural Language Parsing | Google ADK                                 |
| Console Table Formatting | `tabulate` or similar package              |


## 6. Implementation Guidelines
- Use the [google_ai_agent_adk](https://github.com/rmisegal/google_ai_agent_adk) GitHub repo as a reference implementation.

---

## 7. Future Enhancements


- Support for other Gmail labels/folders.
- Automatic or scheduled runs.
- Richer criteria (date ranges, attachments, etc.).
- Additional actions: mark as read, label, archive, forward, summarize, respond.
- Web or chat-based interface.
- Persistent configuration file for default settings.
