from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser


class StatsViewSetTests(APITestCase):
    stats_url = reverse('statistics-list')
    expenses_url = 'http://127.0.0.1:8000/expenses/'
    categories_url = 'http://127.0.0.1:8000/categories/'

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='alexmihai@gmail.com', password='pinguin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        data_1 = {
            "name": "jalapane",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 1,
            "amount": 20,
            "date": 1674477483
        }

        data_2 = {
            "name": "miare",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 3,
            "amount": 20,
            "date": 1674841558
        }

        data_3 = {
            "name": "portocale",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 3,
            "amount": 20,
            "date": 1641059158
        }

        data_4 = {
            "name": "banane",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 2,
            "amount": 20,
            "date": 1672595158
        }

        data_5 = {
            "name": "fier",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 3,
            "amount": 20,
            "date": 1673459158
        }

        data_6 = {
            "name": "bomboane",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 3,
            "amount": 20,
            "date": 1642614358
        }

        data_7 = {
            "name": "sarmale",
            "price": 3323232323.0,
            "currency": "ron",
            "category": 2,
            "amount": 20,
            "date": 1642268758
        }

        category_payload_1 = {
            "name": "animale",
            "user": 1
        }

        category_payload_2 = {
            "name": "pasari",
            "user": 1
        }

        category_payload_3 = {
            "name": "mancare",
            "user": 1
        }

        self.client.post(
            self.categories_url, category_payload_1, format='json')
        self.client.post(
            self.categories_url, category_payload_2, format='json')
        self.client.post(
            self.categories_url, category_payload_3, format='json')

        self.client.post(
            self.expenses_url, data_1, format='json')
        self.client.post(
            self.expenses_url, data_2, format='json')
        self.client.post(
            self.expenses_url, data_3, format='json')
        self.client.post(
            self.expenses_url, data_4, format='json')
        self.client.post(
            self.expenses_url, data_5, format='json')
        self.client.post(
            self.expenses_url, data_6, format='json')
        self.client.post(
            self.expenses_url, data_7, format='json')

    def test_get_stats_autheticated(self):
        expected_response = {
            "user_statistics": {
                "balance_sheet": {
                    "last_1_day": {
                        "price__sum": 3323232323.0
                    },
                    "last_7_days": {
                        "price__sum": 6646464646.0
                    },
                    "last_30_days": {
                        "price__sum": 13292929292.0
                    }
                },
                "most_popular_category": "mancare",
                "invested_the_most_in": "mancare"
            },
            "status": 200
        }

        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, expected_response)
