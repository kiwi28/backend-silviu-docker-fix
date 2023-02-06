
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import CustomUser
import json


class CategoriesViewSetTests(APITestCase):
    categories_one_url = reverse('categories-list', args=[1])
    categories_delete_url = reverse('categories-list', args=[1])
    categories_url = reverse('categories-list')

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='alexmihai@gmail.com', password='pinguin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        category_payload_1 = {
            "name": "animale",
            "user": 1
        }

        category_payload_2 = {
            "name": "masini",
            "user": 1
        }

        category_payload_3 = {
            "name": "case",
            "user": 1
        }

        self.client.post(
            self.categories_url, category_payload_1, format='json')
        self.client.post(
            self.categories_url, category_payload_2, format='json')
        self.client.post(
            self.categories_url, category_payload_3, format='json')

    def test_get_categories_all_autheticated(self):
        expected_response = [
            {
                "id": 1,
                "name": "animale",
                "user": 1
            },
            {
                "id": 3,
                "name": "case",
                "user": 1
            },
            {
                "id": 2,
                "name": "masini",
                "user": 1
            },
        ]

        response = self.client.get(self.categories_url)
        formatted_response = [dict(ordered_dict) for ordered_dict in response.data]
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(formatted_response), json.dumps(expected_response))

    def test_get_category_autheticated(self):
        expected_response = {
            "id": 1,
            "name": "animale",
            "user": 1
        }

        response = self.client.get(self.categories_one_url, secure=True)
        print(response)
        self.assertIn(response.status_code, {status.HTTP_200_OK, status.HTTP_301_MOVED_PERMANENTLY})
        self.assertDictEqual(response.data, expected_response)

    def test_delete_category_authenticated(self):
        response = self.client.delete(self.categories_one_url)
        self.assertIn(response.status_code, {status.HTTP_204_NO_CONTENT, status.HTTP_301_MOVED_PERMANENTLY})
