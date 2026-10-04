"""Customer authentication for the backend.core API.

Bank customers are not Django ``User`` rows, so they authenticate with their
``document_number`` + ``date_of_birth`` and receive a JWT carrying a
``customer_id`` claim. Every authenticated request resolves to a
``CustomerPrincipal`` that viewsets use to scope querysets to that customer.

This module is loaded by DRF settings, so it must not import DRF views (the
login view lives in ``views.py``).
"""

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

CUSTOMER_CLAIM = 'customer_id'


class CustomerPrincipal:
    """Minimal ``request.user`` for a customer authenticated by JWT."""

    is_authenticated = True
    is_anonymous = False
    is_staff = False

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def __str__(self):
        return self.customer_id


def issue_customer_token(customer):
    token = AccessToken()
    token[CUSTOMER_CLAIM] = customer.customer_id
    return str(token)


class CustomerJWTAuthentication(BaseAuthentication):
    """Authenticate ``Authorization: Bearer <jwt>`` as a ``CustomerPrincipal``."""

    keyword = b'bearer'

    def authenticate(self, request):
        header = get_authorization_header(request).split()
        if not header or header[0].lower() != self.keyword:
            return None
        if len(header) != 2:
            raise AuthenticationFailed('Invalid Authorization header.')
        try:
            token = AccessToken(header[1].decode())
        except TokenError as exc:
            raise AuthenticationFailed(str(exc))
        customer_id = token.get(CUSTOMER_CLAIM)
        if not customer_id:
            raise AuthenticationFailed('Token has no customer.')
        return CustomerPrincipal(customer_id), token

    def authenticate_header(self, request):
        return 'Bearer'
