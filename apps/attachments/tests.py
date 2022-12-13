from django.urls import reverse
from rest_framework import status

from ..common.tests import CustomAPITestCase


class AttachmentTestCase(CustomAPITestCase):

    def test_attachment(self):
        self.auth()

        files = {"file": open("media/default_categories/food.jpeg", "rb")}
        data = {"user": self.user.id}
        response = self.client.post(reverse("attachments-list"), data=data, files=files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attachment_id = response.data.get("id")

        response = self.client.get(reverse("attachments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)  # 6 default + 1 created

        response = self.client.get(reverse("attachments-detail", kwargs={"pk": attachment_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse("attachments-detail", kwargs={"pk": attachment_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("attachments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)  # 6 default
