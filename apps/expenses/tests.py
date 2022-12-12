from django.urls import reverse
from faker import Faker
from rest_framework import status

from apps.common.models import Currency
from apps.common.tests import CustomAPITestCase
from apps.expenses.models import Category

fake = Faker()


class ExpensesTestCase(CustomAPITestCase):
    def test_expenses(self):
        self.auth()

        data = {
            "currency": Currency.MDL.value,
            "amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "description": fake.text(),
            "user": self.user.id,
            "category": Category.objects.filter(user=self.user).first().id,
        }
        response = self.client.post(reverse("expenses-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expense_id = response.data.get("id")

        response = self.client.get(reverse("expenses-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse("expenses-detail", kwargs={"pk": expense_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "currency": Currency.EUR.value,
            "amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "description": fake.text(),
            "user": self.user.id,
            "category": Category.objects.filter(user=self.user).last().id,
        }
        response = self.client.put(reverse("expenses-detail", kwargs={"pk": expense_id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True)}
        response = self.client.patch(reverse("expenses-detail", kwargs={"pk": expense_id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse("expenses-detail", kwargs={"pk": expense_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("expenses-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
