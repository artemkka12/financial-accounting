from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from apps.users.models import User

fake = Faker()


class CustomAPITestCase(APITestCase):
    def auth(self):
        username = fake.user_name()
        password = fake.password()
        self.user = User.objects.create_user(username, username + "@gmail.com", password)
        jwt_fetch_data = {"username": username, "password": password}
        response = self.client.post(reverse("token_obtain_pair"), jwt_fetch_data, "json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
