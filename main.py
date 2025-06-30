from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
from collections import deque
import datetime
import json


class ConnectionManager:
    def __init__(self):
        # store all active WebSocket connections as a dictionary
        self.active_connections: Dict[str, WebSocket] = {}
        
        self.message_history = deque(maxlen=10) #deque to store the last 10 messages sent.

    async def connect(self, websocket: WebSocket, username: str):
        # function to handle a new WebSocket connection
        # Accept the WebSocket connection
        await websocket.accept()

        # store the connection in the active connections dictionary
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        # remove the user from the active connections when they disconnect.
        if username in self.active_connections:
            del self.active_connections[username]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # helper to send the history message to the specific user
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # add messages to the history.
        self.message_history.append(message)
        # send the message.
        for connection in self.active_connections.values():
            await connection.send_text(message)

# FastAPI steup

# Creating a FastAPI Instance
app = FastAPI()

#  Create a single instance of FastAPI's WebSocket manager
manager = ConnectionManager()

#WebSocket Endpoint

#  the URL will now include a username
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username:str):

    #check if the username is already connected
    if username in manager.active_connections:
        # if so, close the connection.
        await websocket.close(code=1008, reason=f"Username '{username}' is already taken.")
        return

    #if unique, connect the user.
    await manager.connect(websocket, username)
    print(f"Client '{username}' has connected.")

    #send the chat history to the new user.
    print(f"Sending message history to '{username}'.")
    for msg in manager.message_history:
        await manager.send_personal_message(msg, websocket)

    # welcome message to the new user.
    now = datetime.datetime.now(datetime.timezone.utc)
    join_message = {
        "type": "system_message",
        "content": f"'{username}' joined the chat",
        "timestamp": now.isoformat()
    }
    await manager.broadcast(json.dumps(join_message))

    try:
        # Loop for messages from this user.
        while True:
            data = await websocket.receive_text()
            print(f"Message received from '{username}': {data}")
            
            # structure the message to include the username, content and timestamp
            now = datetime.datetime.now(datetime.timezone.utc)
            chat_message = {
                "type": "chat_message",
                "sender": username,
                "content": data,
                "timestamp": now.isoformat() ## format the timestamp in ISO 8601 format
            }
            await manager.broadcast(json.dumps(chat_message))
            
    except WebSocketDisconnect:
        # handle webSocket disconnection
        manager.disconnect(username)
        print(f"Client '{username}' has disconnected.")
        now = datetime.datetime.now(datetime.timezone.utc)
        goodbye_message = {
            "type": "system_message",
            "content": f"'{username}' left the chat",
            "timestamp": now.isoformat()
        }
        await manager.broadcast(json.dumps(goodbye_message))
