"""Web chat: serves web/index.html and a small JSON API around the agent.

    uvicorn server:app --port 8001      (from agent/, backend running on :8000)

The browser never sees the customer's JWT. Login creates a server-side session
holding the token and the conversation thread; the browser only gets a random
session id, so it can't point the agent at someone else's thread.
"""

import secrets
import uuid
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.errors import GraphRecursionError
from pydantic import BaseModel

import config
from api_client import LoginError, login
from graph import build_graph, run_config

WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(title="Assistente financeiro")
graph = build_graph()
sessions = {}  # session id -> {"token", "thread_id", "first_name"}


class LoginRequest(BaseModel):
    document_number: str
    date_of_birth: str


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.post("/api/login")
def do_login(body: LoginRequest):
    try:
        session = login(body.document_number.strip(), body.date_of_birth.strip())
    except LoginError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = {
        "token": session["access"],
        "thread_id": str(uuid.uuid4()),
        "first_name": session["first_name"],
    }
    return {"session_id": session_id, "first_name": session["first_name"], "model": config.MODEL}


@app.post("/api/logout")
def do_logout(x_session_id: str = Header(default="")):
    sessions.pop(x_session_id, None)
    return {"ok": True}


@app.post("/api/chat")
def chat(body: ChatRequest, x_session_id: str = Header(default="")):
    session = sessions.get(x_session_id)
    if session is None:
        raise HTTPException(status_code=401, detail="Sessão expirada. Entre novamente.")
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Mensagem vazia.")

    cfg = run_config(session["token"], session["thread_id"])
    before = len(graph.get_state(cfg).values.get("messages", []))
    try:
        result = graph.invoke({"messages": [HumanMessage(message)]}, cfg)
    except GraphRecursionError:
        return {"answer": "Não consegui concluir essa pergunta. Pode reformular?", "tools": []}

    new_messages = result["messages"][before:]
    tools = [
        call["name"]
        for m in new_messages if isinstance(m, AIMessage) for call in m.tool_calls
    ]
    return {"answer": result["messages"][-1].text, "tools": tools}
