# AI Chatbot

An AI-powered chatbot built with **FastAPI** and the **Groq API**, with SQLite-based conversation history and a simple web frontend.

The application provides a conversational interface where users can send messages and receive AI-generated responses. Chat sessions and messages are stored locally using SQLite.

## Overview

This project combines a FastAPI backend with a browser-based chatbot interface.

The main components are:

* FastAPI for the backend and API routes
* Groq API for AI-powered responses
* SQLite for storing chat sessions and messages
* HTML for the chatbot interface
* JavaScript for frontend communication
* Configurable system prompts for chatbot roles

## Features

* AI-powered conversations
* FastAPI backend
* Groq API integration
* SQLite chat history
* Session-based conversations
* Browser `localStorage` session management
* Configurable chatbot system prompts
* Web-based chatbot interface
* API-based message handling
* Simple local setup and deployment

## Project Structure

```text
project/
├── main.py              # FastAPI backend, routes
├── chat.py              # Message handling logic
├── database.py          # SQLite storage (sessions + messages)
├── roles.py             # System prompt config
├── requirements.txt
├── chatbot.html         # Frontend (served by backend)
└── models/
    └── llm.py           # Groq API client
```

## Architecture

```text
User
  |
  v
Chatbot Frontend
(chatbot.html)
  |
  v
FastAPI Backend
(main.py)
  |
  v
Message Handling
(chat.py)
  |
  +------------------+
  |                  |
  v                  v
SQLite Database    Groq API
(database.py)      (models/llm.py)
  |                  |
  +--------+---------+
           |
           v
     AI Response
           |
           v
      Chatbot UI
```

---

## Setup (one-time)

### 1. Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs the Python packages required by the application.

### 2. Get a Free Groq API Key

Go to:

[Groq Console](https://console.groq.com)

Sign up or log in, create an API key, and copy it.

The application uses the API key to communicate with the Groq API.

Do not upload or commit your API key to GitHub.

---

## How to Run

Follow these steps every time you want to run the chatbot.

### 1. Set the API Key

On Windows PowerShell, run:

```powershell
$env:GROQ_API_KEY="paste-your-key-here"
```

This environment variable only lasts for the **current terminal session**.

If you open a new terminal, you will need to set the API key again.

### 2. Start the Server

In the same terminal, run:

```bash
uvicorn main:app --reload
```

The FastAPI development server will start locally.

### 3. Open the Chatbot

Open Chrome and go to:

```text
http://127.0.0.1:8000/app
```

The chatbot interface should appear.

The status indicator should turn green when the backend is online.

You can then type a message and send it to the chatbot.

---

## Shortcut — One Line

On Windows PowerShell, you can set the API key and start the server in one command:

```powershell
$env:GROQ_API_KEY="your-key"; uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/app
```

---

## How It Works

### 1. User Sends a Message

The user enters a message through the chatbot frontend.

### 2. FastAPI Receives the Request

The frontend sends the message to the FastAPI backend.

`main.py` handles the application routes and API requests.

### 3. Message Processing

`chat.py` handles the message-processing logic and prepares the conversation context.

### 4. Chat History

`database.py` manages SQLite storage for:

* Chat sessions
* User messages
* Assistant responses

### 5. System Prompt

`roles.py` contains the system prompt configuration that controls the chatbot's behavior and role.

### 6. Groq API

`models/llm.py` communicates with the Groq API and sends the conversation to the selected language model.

### 7. Response

The AI-generated response is returned to the FastAPI backend and displayed in the chatbot interface.

---

## Chat History

Chat history is stored locally in:

```text
chat_history.db
```

The database stores conversations according to their session IDs.

Each browser session receives a session ID that is stored in the browser's `localStorage`.

This means:

* Refreshing the page keeps the same conversation.
* Chat history is associated with the current session.
* Opening the chatbot in another browser creates a new session.
* Using another device creates a new session.

## Database

SQLite is used because it provides a lightweight local database without requiring a separate database server.

The database is managed through:

```text
database.py
```

The database stores both session information and individual chat messages.

---

## Chatbot Roles

The chatbot's system prompt is configured through:

```text
roles.py
```

This allows the chatbot's behavior and instructions to be modified without changing the main application logic.

For example, the system prompt can define:

* Assistant personality
* Response style
* Areas of expertise
* Instructions for answering questions
* Conversation behavior

---

## Backend

The backend is built using **FastAPI**.

The main backend file is:

```text
main.py
```

It is responsible for:

* Starting the FastAPI application
* Defining API routes
* Serving the chatbot frontend
* Handling chatbot-related requests
* Connecting the different application components

The application is started using:

```bash
uvicorn main:app --reload
```

---

## Frontend

The chatbot interface is contained in:

```text
chatbot.html
```

The HTML file is served directly by the FastAPI backend.

The frontend communicates with the backend using HTTP requests and displays the returned AI responses in the chat interface.

The application can be accessed through:

```text
http://127.0.0.1:8000/app
```

---

## Groq Integration

The Groq API client is implemented in:

```text
models/llm.py
```

The API key is obtained from the environment variable:

```text
GROQ_API_KEY
```

This approach prevents the API key from being hard-coded directly into the source code.

The API key should never be committed to a public GitHub repository.

---

## Requirements

A typical `requirements.txt` for this project contains the Python dependencies required for:

* FastAPI
* Uvicorn
* Groq
* Additional backend functionality

Install them using:

```bash
pip install -r requirements.txt
```

The project should be run with a supported Python version compatible with the packages specified in `requirements.txt`.

---

## Troubleshooting

| Problem                               | Cause                                                           | Fix                                                                           |
| ------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `groq.GroqError: api_key must be set` | `GROQ_API_KEY` was not set before starting the server           | Set the API key first using `$env:GROQ_API_KEY="your-key"`                    |
| `Internal Server Error` on `/app`     | The HTML filename in `main.py` does not match the actual file   | Check the filename used in `FileResponse(...)` inside `main.py`               |
| Status dot stays red                  | Server is not running or the `/mode` endpoint cannot be reached | Check the Uvicorn terminal and make sure the server is running without errors |
| Chat sends but no reply               | Groq API key may be invalid or expired                          | Generate a new API key from the Groq Console                                  |
| `ModuleNotFoundError`                 | Required dependencies are not installed                         | Run `pip install -r requirements.txt`                                         |
| Port already in use                   | Another application is using port 8000                          | Stop the other process or start Uvicorn on another port                       |

---

## Important Notes

### API Key

Never commit your Groq API key to GitHub.

Use the environment variable:

```text
GROQ_API_KEY
```

instead of placing the key directly inside Python files.

### Chat History

Chat history is stored locally in:

```text
chat_history.db
```

The session ID is stored in the browser's `localStorage`.

Switching browsers or devices starts a fresh conversation because the session information is browser-specific.

### No Streaming

This version does not use streaming responses.

The complete AI response is returned after the model finishes generating it.

A word-by-word typing effect can be added in a future version.

### No Image Upload

This version focuses on text-based conversations.

Image uploading and multimodal input are not included.

These features can be added later if required.

---

## Limitations

The current version is intentionally simple and focuses on the core chatbot functionality.

Current limitations include:

* No streaming responses
* No image upload
* Local SQLite storage
* Session-specific browser history
* Requires an active Groq API key
* Requires an internet connection for Groq API requests
* No built-in user authentication

---

## Future Improvements

Possible improvements include:

* Streaming AI responses
* Image upload and vision support
* User authentication
* Multiple chatbot personalities
* Conversation management
* Delete and rename conversations
* Export chat history
* Cloud database integration
* Persistent user accounts
* Voice input
* Text-to-speech responses
* Markdown rendering
* Code syntax highlighting
* Deployment to a cloud platform

---

## Running Locally

The complete local workflow is:

```text
1. Install dependencies
        |
        v
2. Set GROQ_API_KEY
        |
        v
3. Run Uvicorn
        |
        v
4. Open /app
        |
        v
5. Start chatting
```

Start the application with:

```powershell
$env:GROQ_API_KEY="your-key"; uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/app
```

## Conclusion

This project demonstrates how to build a simple AI chatbot by combining **FastAPI, Groq, SQLite, and a browser-based frontend**.

The modular structure separates the backend routes, message handling, database management, chatbot configuration, and LLM communication, making the project easier to understand and extend.
