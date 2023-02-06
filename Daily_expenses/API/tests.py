from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import CustomUser


class ExpensesViewSetTests(APITestCase):
    expenses_url = 'http://127.0.0.1:8000/expenses/'
    # expenses_url = reverse('expenses-list')
    expenses_delete_url = 'http://127.0.0.1:8000/expenses/1/'
    # expenses_delete_url = reverse('expenses-list', args=[1])
    categories_url = 'http://127.0.0.1:8000/categories/'
    # categories_url = reverse('categories:categories-list')

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='alexmihai@gmail.com', password='pinguin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        data = {
            "name": "jalapane",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 1,
            "amount": 20,
            "date": 1674477483
        }

        category_payload = {
            "name": "animal se",
            "user": 1
        }

        self.client.post(
            self.categories_url, category_payload, format='json')
        self.client.post(
            self.expenses_url, data, format='json')

    def test_get_expenses_autheticated(self):
        expected_response = {
            "id": 1,
            "name": "jalapane",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 1,
            "amount": 20,
            'date': '2023-01-23',
            'user': 1
        }

        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(dict(response.data['expenses'][0]), expected_response)

    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, 401)

    def test_delete_customer_authenticated(self):
        response = self.client.delete(self.expenses_delete_url)
        self.assertIn(response.status_code, {status.HTTP_204_NO_CONTENT, status.HTTP_301_MOVED_PERMANENTLY})
