"""Agent settings, read from the repo-root .env (see .env.example)."""

import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000/api")

# Haiku while developing (cheap), Opus for the demo: switch in .env.
MODEL = os.getenv("AGENT_MODEL", "claude-haiku-4-5")

# The dataset ends on 2026-06-18, so the agent lives on that day.
SIMULATED_TODAY = date(2026, 6, 18)
DEFAULT_PERIOD_DAYS = 30

# Max graph steps per question, so a tool-calling loop can't run up costs.
RECURSION_LIMIT = 12
