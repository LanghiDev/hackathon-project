from datetime import date, datetime, timezone
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from . import models


def make_customer(customer_id, document_number, date_of_birth):
    return models.Customer.objects.create(
        customer_id=customer_id,
        document_number=document_number,
        document_type='CC',
        first_name='Test',
        last_name=customer_id,
        date_of_birth=date_of_birth,
        city='Bogotá',
        state='Cundinamarca',
        country='Colombia',
        segment='Mass',
        registration_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        customer_status='Active',
    )


def make_transaction(transaction_id, customer, product):
    return models.Transaction.objects.create(
        transaction_id=transaction_id,
        transaction_date=datetime(2026, 6, 1, tzinfo=timezone.utc),
        process_date=date(2026, 6, 1),
        product=product,
        customer=customer,
        transaction_type='Purchase',
        amount=Decimal('10.00'),
        currency='USD',
        channel='App',
        transaction_country='Colombia',
        transaction_status='Approved',
    )


def make_product(product_id, customer):
    return models.Product.objects.create(
        product_id=product_id,
        customer=customer,
        product_type='Debit Card',
        product_number=f'N-{product_id}',
        currency='USD',
        current_balance=Decimal('100.00'),
        opening_date=date(2024, 1, 1),
        product_status='Active',
        opening_channel='App',
    )


class CustomerAuthTests(APITestCase):
    def setUp(self):
        self.alice = make_customer('CUS-ALICE', '111', date(1990, 5, 17))
        self.bob = make_customer('CUS-BOB', '222', date(1985, 1, 2))
        alice_product = make_product('PRD-ALICE', self.alice)
        bob_product = make_product('PRD-BOB', self.bob)
        make_transaction('TX-ALICE', self.alice, alice_product)
        make_transaction('TX-BOB', self.bob, bob_product)

    def login(self, document_number='111', date_of_birth='1990-05-17'):
        return self.client.post(
            '/api/auth/login/',
            {'document_number': document_number, 'date_of_birth': date_of_birth},
            format='json',
        )

    def authenticate_as_alice(self):
        token = self.login().data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_login_returns_token_for_matching_birth_date(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer_id'], 'CUS-ALICE')
        self.assertIn('access', response.data)

    def test_login_rejects_wrong_birth_date(self):
        response = self.login(date_of_birth='1990-05-18')
        self.assertEqual(response.status_code, 401)

    def test_api_requires_authentication(self):
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer not-a-token')
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, 401)

    def test_customer_only_sees_own_rows(self):
        self.authenticate_as_alice()
        response = self.client.get('/api/transactions/')
        ids = [row['transaction_id'] for row in response.data['results']]
        self.assertEqual(ids, ['TX-ALICE'])

    def test_filtering_by_another_customer_returns_nothing(self):
        self.authenticate_as_alice()
        response = self.client.get('/api/transactions/', {'customer': 'CUS-BOB'})
        self.assertEqual(response.data['results'], [])

    def test_another_customers_row_is_not_found(self):
        self.authenticate_as_alice()
        self.assertEqual(self.client.get('/api/transactions/TX-BOB/').status_code, 404)
        self.assertEqual(self.client.get('/api/customers/CUS-BOB/').status_code, 404)

    def test_api_is_read_only(self):
        self.authenticate_as_alice()
        self.assertEqual(self.client.delete('/api/transactions/TX-ALICE/').status_code, 405)
        self.assertEqual(self.client.post('/api/transactions/', {}, format='json').status_code, 405)

    def test_internal_tables_are_staff_only(self):
        self.authenticate_as_alice()
        self.assertEqual(self.client.get('/api/agents/').status_code, 403)
        self.assertEqual(self.client.get('/api/campaigns/').status_code, 403)

    def test_staff_session_sees_all_rows(self):
        staff = User.objects.create_user('samuel', password='pw', is_staff=True)
        self.client.force_authenticate(staff)
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.data['count'], 2)
