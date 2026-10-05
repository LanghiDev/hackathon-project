"""Terminal chat: log in as a customer, then ask about your money.

    python cli.py           # chat
    python cli.py --debug   # also print every message (tool calls and results)
"""

import sys
import uuid

from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError

import config
from api_client import LoginError, login
from graph import build_graph, run_config

EXIT_WORDS = {"sair", "exit", "quit", "salir"}


def main():
    debug = "--debug" in sys.argv
    print(f"Assistente financeiro ({config.MODEL}) - digite 'sair' para encerrar.\n")
    try:
        session = login(input("Documento: ").strip(), input("Data de nascimento (AAAA-MM-DD): ").strip())
    except LoginError as exc:
        print(exc)
        return

    graph = build_graph()
    cfg = run_config(session["access"], str(uuid.uuid4()), session["first_name"])
    print(f"\nOlá, {session['first_name']}! Como posso ajudar?\n")

    seen = 0  # messages already shown; the result holds the whole thread history
    while True:
        try:
            question = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        if question.lower() in EXIT_WORDS:
            break
        try:
            result = graph.invoke({"messages": [HumanMessage(question)]}, cfg)
        except GraphRecursionError:
            print("Assistente: Não consegui concluir essa pergunta. Pode reformular?\n")
            continue
        messages = result["messages"]
        if debug:
            # This turn's steps (question, tool calls, tool results); the
            # final answer is printed once, below.
            for message in messages[seen:-1]:
                message.pretty_print()
        seen = len(messages)
        print(f"Assistente: {messages[-1].text}\n")


if __name__ == "__main__":
    main()
