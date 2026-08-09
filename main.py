import uuid
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from chat import process_message
from database import init_db, create_session, get_session_role, get_chat_history


app = FastAPI(title="Chat Backend", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # loosened for local dev — tighten before real deployment
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

init_db()


class ChatRequest(BaseModel):
    message: str
    session_id: str = ""

class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/app")
def serve_app():
    """Chrome mein http://127.0.0.1:8000/app par khuluga mein."""
    return FileResponse("chatbot.html")


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/mode")
def get_mode():
    return {"status": "running"}


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    x_api_key: Optional[str] = Header(default=None)
):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Kuch to likho yaawr :( ")
    if len(request.message) > 2000:
        raise HTTPException(status_code=400, detail="2000 characters se zyada nhi parh sakta mein yaawr :( ")

    session_id = request.session_id.strip() if request.session_id else ""
    if not session_id:
        session_id = str(uuid.uuid4())
        create_session(session_id, "user")
    else:
        registered_role = get_session_role(session_id)
        if not registered_role:
            create_session(session_id, "user")

    response = process_message(
        message=request.message.strip(),
        role="user",
        session_id=session_id
    )

    return ChatResponse(response=response, session_id=session_id)


@app.get("/history/{session_id}")
def get_history(session_id: str):
    if not session_id or len(session_id) > 100:
        raise HTTPException(status_code=400, detail="Bro!Invalid session ID.")
    registered_role = get_session_role(session_id)
    if not registered_role:
        raise HTTPException(status_code=404, detail="Session nahi mil raha.")
    history = get_chat_history(session_id)
    return {"session_id": session_id, "history": history}