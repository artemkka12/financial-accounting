from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..users.models import User

fake = Faker()


class CustomAPITestCase(APITestCase):
    def auth(self):
        username = fake.email()
        data = {
            "email": username,
            "username": username,
            "password": fake.password(),
        }

        response = self.client.post(reverse("users-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse("token_obtain_pair"), data, "json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.user = User.objects.get(username=username)
