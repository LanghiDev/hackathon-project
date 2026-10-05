"""Thin HTTP client for the backend API, always acting as one logged-in customer."""

import httpx

import config


class LoginError(Exception):
    pass


def login(document_number, date_of_birth):
    """Exchange document + birth date for a session ({access, customer_id, first_name})."""
    response = httpx.post(
        f"{config.API_URL}/auth/login/",
        json={"document_number": document_number, "date_of_birth": date_of_birth},
        timeout=30,
    )
    if response.status_code in (400, 401):
        raise LoginError("Invalid document number or date of birth.")
    response.raise_for_status()
    return response.json()


class BankAPI:
    """Calls the API with the customer's JWT; the backend scopes every query to them."""

    def __init__(self, token):
        self._client = httpx.Client(
            base_url=config.API_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )

    def get_all(self, path, **params):
        """Return every row of a list endpoint, following pagination."""
        rows = []
        response = self._client.get(path, params={**params, "page_size": 100})
        while True:
            response.raise_for_status()
            page = response.json()
            rows.extend(page["results"])
            if not page["next"]:
                return rows
            response = self._client.get(page["next"])
