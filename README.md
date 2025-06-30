# Real-Time Chat Backend

This is a real-time chat server built with a Python (FastAPI) backend. The entire application is containerized using Docker and orchestrated with Docker Compose, allowing for easy setup and deployment.

The project demonstrates a modern, event-driven architecture using WebSockets for instant, bidirectional communication between the server and multiple clients.

---

## Key Features

* **Live Group Chat:** Allows multiple clients to connect to a chat room with a unique username and communicate in real-time. Messages are broadcast instantly to all connected participants.
* **Structured JSON Messaging:** Communication is handled via structured JSON objects, including message type (`system` or `chat`), sender, content, and a UTC timestamp, making the data robust and easy for clients to parse.
* **Dynamic User Sessions:** The server manages user connections gracefully, preventing duplicate usernames and broadcasting system messages when users join or leave the chat.
* **Persistent Chat History:** The server maintains a history of the last 10 messages. When a new client connects, they immediately receive this history, providing context to the ongoing conversation.
* **Containerized Environment:** The backend service is fully containerized, managed by a single `docker-compose.yml` file for a clean, isolated, and reproducible setup.

---

## Technology Stack

| Area               | Technology                          |
| :----------------- | :---------------------------------- |
| **Backend** | Python 3.11, FastAPI, Uvicorn       |
| **Real-Time** | WebSockets                          |
| **Containerization** | Docker, Docker Compose              |
| **Testing** | Postman (or any WebSocket client)   |

---

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

* You must have **Docker** and **Docker Compose** installed on your system.
    * [Install Docker Engine](https://docs.docker.com/engine/install/)
    * [Install Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Launch

1.  **Clone the repository:**
    ```bash
    For Linux, Mac

    git clone git@github.com:KingSajxxd/python-chat-server.git
    cd python-chat-server

    For Windows

    git clone https://github.com/KingSajxxd/python-chat-server.git
    cd python-chat-server
    ```

2.  **Build and run the container:**
    From the root directory of the project (where `docker-compose.yml` is located), run the following command:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image for the Python backend service and start the container.

3.  **Connect to the Application:**
    Once the container is running, the WebSocket server is accessible at `ws://localhost:8000`. You can connect to it using a WebSocket client like Postman.
    * **Connection URL:** `ws://localhost:8000/ws/{your_username}`
    * Replace `{your_username}` with a name of your choice (e.g., `ws://localhost:8000/ws/Anura`).

4.  **Stopping the Application:**
    To stop the application, press `Ctrl + C` in the terminal where Docker Compose is running, and then run:
    ```bash
    docker-compose down
    ```

---

## Application Structure
```bash
├── docker-compose.yml      # Orchestrates the backend service
├── Dockerfile              # Dockerfile for the Python backend
├── main.py                 # The FastAPI/WebSocket server code
└── requirements.txt        # Python dependencies
```