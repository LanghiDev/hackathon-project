"""Tools the agent can call. Each one only ever sees the logged-in customer's data.

Security: the customer's token comes from the run config
(``config["configurable"]["token"]``), which the code sets at login. It is not a
tool argument, so the LLM cannot choose whose data to read, and the backend
filters every query by the customer inside the token.
"""

from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

import config as settings
from api_client import BankAPI

# Q4: money that left the customer's pocket. Transfers may go to the customer's
# own accounts, so they don't count as spending.
SPENDING_TYPES = {"Purchase", "Payment", "Withdrawal"}

# Q8: ISO 8583 response codes present in the dataset.
DECLINE_REASONS = {
    "51": "Saldo ou limite insuficiente",
    "14": "Número de cartão inválido",
    "54": "Cartão vencido",
    "05": "Não autorizada pelo emissor",
}

TransactionType = Literal["Purchase", "Payment", "Withdrawal", "Transfer", "Deposit", "Adjustment"]
TransactionStatus = Literal["Approved", "Declined", "Pending", "Reversed"]


def _api(config):
    return BankAPI(config["configurable"]["token"])


def _period(start_date, end_date, default_start=None):
    end = date.fromisoformat(end_date) if end_date else settings.SIMULATED_TODAY
    if start_date:
        start = date.fromisoformat(start_date)
    else:
        start = default_start or end - timedelta(days=settings.DEFAULT_PERIOD_DAYS)
    if start > end:
        raise ValueError("start_date must be on or before end_date.")
    return start, end


def _tx_date(tx):
    return datetime.fromisoformat(tx["transaction_date"]).date()


def _transactions_in(config, start, end, **filters):
    rows = _api(config).get_all("/transactions/", **filters)
    return [tx for tx in rows if start <= _tx_date(tx) <= end]


def _category(tx):
    if tx["transaction_type"] == "Withdrawal":
        return "Saque"
    return tx["transaction_category"] or tx["merchant_category"] or "Sem categoria"


def _decline_reason(tx):
    code = tx["response_code"]
    if not code:
        return "Motivo não informado pelo processador"
    code = f"{int(float(code)):02d}"
    return DECLINE_REASONS.get(code, f"Código de recusa {code}")


def _brief(tx):
    return {
        "id": tx["transaction_id"],
        "date": tx["transaction_date"],
        "type": tx["transaction_type"],
        "status": tx["transaction_status"],
        "amount": tx["amount"],
        "currency": tx["currency"],
        "merchant": tx["merchant_name"] or None,
        "category": _category(tx),
        "channel": tx["channel"],
        "city": tx["transaction_city"],
    }


def _period_info(start, end):
    return {"start": start.isoformat(), "end": end.isoformat()}


@tool
def list_transactions(
    start_date: str | None = None,
    end_date: str | None = None,
    transaction_type: TransactionType | None = None,
    status: TransactionStatus | None = None,
    category: str | None = None,
    spending_only: bool = False,
    order_by: Literal["date", "amount"] = "date",
    limit: int = 20,
    *,
    config: RunnableConfig,
) -> dict:
    """List the customer's transactions, newest first or largest first.

    Use for questions like "what did I buy yesterday?" or, with
    spending_only=True and order_by="amount", "what was my biggest expense in
    June?". spending_only keeps only approved Purchase, Payment and Withdrawal
    transactions (the same rule as spending_summary). Dates are ISO
    (YYYY-MM-DD) and inclusive; when omitted the period is the last 30 days.
    `category` is one of Food, Transport, Services, Entertainment, Health,
    Other, Saque. Returns at most `limit` rows (max 50) plus the total matching.
    """
    start, end = _period(start_date, end_date)
    filters = {}
    if transaction_type:
        filters["transaction_type"] = transaction_type
    if status:
        filters["transaction_status"] = status
    rows = _transactions_in(config, start, end, **filters)
    if spending_only:
        rows = [
            tx for tx in rows
            if tx["transaction_type"] in SPENDING_TYPES and tx["transaction_status"] == "Approved"
        ]
    if category:
        rows = [tx for tx in rows if _category(tx).lower() == category.lower()]
    if order_by == "amount":
        rows.sort(key=lambda tx: Decimal(tx["amount"]), reverse=True)
    else:
        rows.sort(key=lambda tx: tx["transaction_date"], reverse=True)
    limit = max(1, min(limit, 50))
    return {
        "period": _period_info(start, end),
        "total_matching": len(rows),
        "transactions": [_brief(tx) for tx in rows[:limit]],
    }


@tool
def spending_summary(
    start_date: str | None = None,
    end_date: str | None = None,
    group_by: Literal["category", "month", "merchant"] = "category",
    *,
    config: RunnableConfig,
) -> dict:
    """Total spending of the customer in a period, grouped by category, month or merchant.

    Spending = approved Purchase, Payment and Withdrawal ("Saque") transactions.
    Totals are separate per currency and must never be added across currencies.
    Dates are ISO (YYYY-MM-DD) and inclusive; when omitted the period is the
    last 30 days.
    """
    start, end = _period(start_date, end_date)
    rows = [
        tx for tx in _transactions_in(config, start, end, transaction_status="Approved")
        if tx["transaction_type"] in SPENDING_TYPES
    ]
    key = {
        "category": _category,
        "month": lambda tx: _tx_date(tx).strftime("%Y-%m"),
        "merchant": lambda tx: tx["merchant_name"] or _category(tx),
    }[group_by]

    by_currency = defaultdict(lambda: defaultdict(lambda: [Decimal("0"), 0]))
    for tx in rows:
        bucket = by_currency[tx["currency"]][key(tx)]
        bucket[0] += Decimal(tx["amount"])
        bucket[1] += 1

    totals = {}
    for currency, groups in by_currency.items():
        ordered = sorted(groups.items(), key=lambda item: item[1][0], reverse=True)
        totals[currency] = {
            "total": str(sum(total for total, _ in groups.values())),
            "count": sum(count for _, count in groups.values()),
            "groups": [{group_by: name, "total": str(total), "count": count} for name, (total, count) in ordered],
        }
    return {"period": _period_info(start, end), "by_currency": totals}


@tool
def declined_transactions(
    start_date: str | None = None,
    end_date: str | None = None,
    *,
    config: RunnableConfig,
) -> dict:
    """The customer's declined transactions, newest first, each with the decline reason.

    Use for "why was my (last) transaction declined?". Dates are ISO
    (YYYY-MM-DD) and inclusive; when start_date is omitted the whole history
    is searched, so the most recent decline is found even if it is old.
    """
    start, end = _period(start_date, end_date, default_start=settings.HISTORY_START)
    rows = _transactions_in(config, start, end, transaction_status="Declined")
    rows.sort(key=lambda tx: tx["transaction_date"], reverse=True)
    return {
        "period": _period_info(start, end),
        "declined": [{**_brief(tx), "reason": _decline_reason(tx)} for tx in rows],
    }


@tool
def get_my_accounts(*, config: RunnableConfig) -> dict:
    """The customer's products (accounts, cards, loans, investments) with balance and limits.

    Use for "what is my balance?" or "what is my credit card limit?".
    """
    products = _api(config).get_all("/products/")
    return {
        "products": [
            {
                "type": p["product_type"],
                "number_last4": p["product_number"][-4:],
                "status": p["product_status"],
                "currency": p["currency"],
                "current_balance": p["current_balance"],
                "credit_limit": p["credit_limit"],
                "interest_rate": p["interest_rate"],
                "days_past_due": p["days_past_due"],
            }
            for p in products
        ]
    }


TOOLS = [list_transactions, spending_summary, declined_transactions, get_my_accounts]
