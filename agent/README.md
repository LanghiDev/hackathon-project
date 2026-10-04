# Agent

Personal-finance chat on top of the backend API, built with LangGraph and Claude.
A customer logs in with document number + birth date; every tool reads only that
customer's data (the JWT travels in the run config, never through the LLM).

| File | What it does |
|---|---|
| `config.py` | Settings from the repo-root `.env` (model, API URL, simulated "today" = 2026-06-18) |
| `api_client.py` | Login + paginated GETs against the backend with the customer's JWT |
| `tools.py` | `list_transactions`, `spending_summary`, `declined_transactions`, `get_my_accounts` |
| `prompts.py` | System prompt (language, no invented data, currencies, privacy rules) |
| `graph.py` | LangGraph: `agent` node <-> `ToolNode`, memory via `InMemorySaver` |
| `cli.py` | Terminal chat (`--debug` prints every tool call and result) |
| `evals/run_questions.py` | Fixed questions, including prompt-injection attempts |

## Run

1. Backend running on `localhost:8000` (see `backend/`).
2. `cp .env.example .env` at the repo root and set `ANTHROPIC_API_KEY`.
3. From `agent/`:

```
python3.14 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cli.py --debug
python evals/run_questions.py
```

Demo login (synthetic data): document `78481769`, birth date `1982-02-05`.
