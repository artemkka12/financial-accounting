from django.urls import reverse
from faker import Faker
from rest_framework import status

from ..common.tests import CustomAPITestCase

fake = Faker()


class UserTestCase(CustomAPITestCase):
    def test_user(self):
        self.auth()

        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"username": fake.user_name()}
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.user.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse("users-detail", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
