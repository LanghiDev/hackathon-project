"""Web chat: serves web/index.html and a small JSON API around the agent.

    uvicorn server:app --port 8001      (from agent/, backend running on :8000)

The browser never sees the customer's JWT. Login creates a server-side session
holding the token and the conversation thread; the browser only gets a random
session id, so it can't point the agent at someone else's thread.
"""

import json
import secrets
import uuid
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from pydantic import BaseModel

import config
from api_client import LoginError, login
from graph import build_graph, run_config

WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(title="Finance assistant")
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
        raise HTTPException(status_code=401, detail="Session expired. Please sign in again.")
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Empty message.")

    cfg = run_config(session["token"], session["thread_id"], session["first_name"])
    before = len(graph.get_state(cfg).values.get("messages", []))
    try:
        result = graph.invoke({"messages": [HumanMessage(message)]}, cfg)
    except GraphRecursionError:
        return {"answer": "I couldn't finish that question. Could you rephrase it?", "tools": [], "charts": []}

    new_messages = result["messages"][before:]
    tools = [
        call["name"]
        for m in new_messages if isinstance(m, AIMessage) for call in m.tool_calls
    ]
    return {"answer": result["messages"][-1].text, "tools": tools, "charts": _charts(new_messages)}


def _charts(messages):
    """Chart specs from this turn's show_spending_chart results (numbers computed by code)."""
    charts = []
    for m in messages:
        if isinstance(m, ToolMessage) and m.name == "show_spending_chart" and m.status != "error":
            try:
                result = json.loads(m.content)
            except (TypeError, ValueError):
                continue
            charts.extend({**chart, "period": result["period"]} for chart in result["charts"])
    return charts
