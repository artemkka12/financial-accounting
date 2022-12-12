from django.urls import reverse
from faker import Faker
from rest_framework import status

from apps.common.models import Currency
from apps.common.tests import CustomAPITestCase

from .models import Debt, DebtType

fake = Faker()


class DebtsTestCase(CustomAPITestCase):
    def test_debts(self):
        self.auth()
        data = {
            "amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "currency": Currency.MDL.value,
            "description": fake.text(),
            "second_person": fake.name(),
            "type": DebtType.BORROW.value,
            "deadline": fake.date(),
        }
        response = self.client.post(reverse("debts-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        debt = Debt.objects.last()

        response = self.client.get(reverse("debts-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse("debts-detail", kwargs={"pk": debt.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "amount": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "currency": Currency.EUR.value,
            "description": fake.text(),
            "second_person": fake.name(),
            "type": DebtType.BORROW.value,
            "deadline": fake.date(),
        }
        response = self.client.put(reverse("debts-detail", kwargs={"pk": debt.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"amount": debt.amount - debt.amount / 2}
        response = self.client.patch(reverse("debts-partial-pay", kwargs={"pk": debt.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(reverse("debts-mark-as-paid", kwargs={"pk": debt.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("debts-overdue"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse("debts-detail", kwargs={"pk": debt.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("debts-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
