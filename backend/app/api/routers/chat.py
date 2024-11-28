from typing import List
import os
import pickle
from fastapi.responses import StreamingResponse, JSONResponse
from llama_index.chat_engine.types import BaseChatEngine
from app.engine.index import get_chat_engine
from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile
from llama_index.llms.base import ChatMessage
from llama_index.llms.types import MessageRole
from pydantic import BaseModel
from app.engine.constants import DATA_DIR

chat_router = r = APIRouter()

class _Message(BaseModel):
    role: MessageRole
    content: str

class _ChatData(BaseModel):
    messages: List[_Message]

# Initialize history as a 2D array
history = []

# File path to save conversation history
HISTORY_FILE = os.path.join(DATA_DIR, "history.pkl")

# Function to save history to pickle
def save_history_to_file(history):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(history, f)

# Function to load history from pickle
def load_history_from_file():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "rb") as f:
            return pickle.load(f)
    return []

# Load existing history at startup
history = load_history_from_file()

@r.post("")
async def chat(
    request: Request,
    data: _ChatData,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    # Check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    last_message = data.messages.pop()
    if last_message.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )

    # Convert messages coming from the request to ChatMessage type
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]

    # Create a new conversation
    conversation = [last_message.dict()]
    
    # Query chat engine
    response = chat_engine.stream_chat(last_message.content, messages)

    # Stream response
    async def event_generator():
        content = ""
        for token in response.response_gen:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            content += token
            yield token

        # Once the full response is generated, append to the history
        if content and history:
            history[-1].append({"role": MessageRole.SYSTEM, "content": content})
            save_history_to_file(history)

    return StreamingResponse(event_generator(), media_type="text/plain")

@r.post("/history")
async def start_new_chat_history():
    """
    Handles POST requests to /history by starting a new empty conversation.
    """
    global history
    # Start a new empty conversation
    history.append([])  # Append an empty list to history
    save_history_to_file(history)
    return JSONResponse(content={"message": "New conversation started", "history": history})


@r.get("/history")
async def get_chat_history():
    """
    Handles GET requests to /history by appending a message to the latest conversation 
    if history exists.
    """
    global history
    if history:  # Check if there's an existing conversation
        last_conversation = history[-1]
        save_history_to_file(history)
    else:
        return JSONResponse(content={"history": [], "message": "No conversation history found"}) 
    return JSONResponse(content={"history": history})


@r.post("/upload")
async def upload_document(file: UploadFile):
    file_path = os.path.join(DATA_DIR, file.filename)
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the directory exists
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"Uploaded {file.filename} successfully"}