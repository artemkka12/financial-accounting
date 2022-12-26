from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from ..users.models import User

fake = Faker()


class CustomAPITestCase(APITestCase):
    def auth(self):
        username = fake.email()
        password = fake.password()
        self.user = User.objects.create_user(username=username, email=username, password=password)
        jwt_fetch_data = {"username": username, "password": password}
        response = self.client.post(reverse("token_obtain_pair"), jwt_fetch_data, "json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
