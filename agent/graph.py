"""The agent as a LangGraph graph.

    START -> agent --(asked for tools?)--> tools -> agent -> ... -> END

The "agent" node calls the LLM with the conversation so far. If the reply asks
for tool calls, the "tools" node runs them and the results go back to the LLM.
When the LLM answers without asking for tools, the graph ends.
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

import config
from prompts import SYSTEM_PROMPT
from tools import TOOLS


def build_llm():
    # Opus 5.5 always thinks; low effort keeps a simple chat fast and cheap.
    # Haiku 4.5 rejects the effort parameter, so it is only sent to Opus.
    extra = {"effort": "low"} if config.MODEL.startswith("claude-opus") else {}
    return ChatAnthropic(model=config.MODEL, max_tokens=16000, **extra)


def build_graph(checkpointer=None):
    llm_with_tools = build_llm().bind_tools(TOOLS)

    def agent(state: MessagesState):
        messages = [SystemMessage(SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [llm_with_tools.invoke(messages)]}

    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    # The checkpointer stores each thread's messages: that's the chat memory.
    return builder.compile(checkpointer=checkpointer or InMemorySaver())


def run_config(token, thread_id):
    """Per-session config: the token reaches the tools, never the LLM."""
    return {
        "configurable": {"token": token, "thread_id": thread_id},
        "recursion_limit": config.RECURSION_LIMIT,
    }
