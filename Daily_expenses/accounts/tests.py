from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import CustomUser


class AccountsFunctionalityTests(APITestCase):
    register_url = 'http://127.0.0.1:8000/register/'
    # register_url = reverse('register')
    login_url = 'http://127.0.0.1:8000/login/'
    # login_url = reverse('login')
    logout_url = 'http://127.0.0.1:8000/logout/'
    # logout_url = reverse('logout')

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='silviu',
            email='silviu@gmail.com', password='pinguin12340')
        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register(self):
        payload = {
            "first_name": "bob",
            "last_name": "mihai",
            "username": "bob",
            "email": "bob@gmail.com",
            "password": "pinguin12340"
        }

        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        payload = {
            "username": "silviu@gmail.com",
            "password": "pinguin12340"
        }
        response = self.client.post(reverse("login"), payload)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="silviu")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
