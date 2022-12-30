from django.urls import reverse
from faker import Faker
from rest_framework import status

from ..common.tests import CustomAPITestCase

fake = Faker()


class IncomesTestCase(CustomAPITestCase):
    def test_incomes(self):
        self.auth()

        data = {
            "amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "description": fake.text(),
            "user": self.user.id,
        }
        response = self.client.post(reverse("incomes-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        income_id = response.data.get("id")

        response = self.client.get(reverse("incomes-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse("incomes-detail", kwargs={"pk": income_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "description": fake.text(),
            "user": self.user.id,
        }
        response = self.client.put(reverse("incomes-detail", kwargs={"pk": income_id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True)}
        response = self.client.patch(reverse("incomes-detail", kwargs={"pk": income_id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse("incomes-detail", kwargs={"pk": income_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("incomes-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
