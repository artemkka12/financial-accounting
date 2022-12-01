# python manage.py load_categories --user_id=instance.id
from django.core.management import BaseCommand

from apps.attachments.models import Attachment
from apps.expenses.models import Category


class Command(BaseCommand):
    help = "Command to load default categories"

    def add_arguments(self, parser):
        parser.add_argument("--user_id", type=int, help="User id", required=True)

    def handle(self, **kwargs):
        user_id = kwargs.get("user_id")

        images = {
            "Food": Attachment.objects.get_or_create(file="default_categories/food.jpeg")[0],
            "Transport": Attachment.objects.get_or_create(file="default_categories/transport.jpeg")[0],
            "Clothes": Attachment.objects.get_or_create(file="default_categories/clothes.jpeg")[0],
            "House": Attachment.objects.get_or_create(file="default_categories/house.jpg")[0],
            "Other": Attachment.objects.get_or_create(file="default_categories/other.png")[0],
            "Sport": Attachment.objects.get_or_create(file="default_categories/sport.png")[0],
        }

        categories = [
            Category(name="Food", user_id=user_id, image=images.get("Food")),
            Category(name="Transport", user_id=user_id, image=images.get("Transport")),
            Category(name="Clothes", user_id=user_id, image=images.get("Clothes")),
            Category(name="House", user_id=user_id, image=images.get("House")),
            Category(name="Other", user_id=user_id, image=images.get("Other")),
            Category(name="Sport", user_id=user_id, image=images.get("Sport")),
        ]

        Category.objects.bulk_create(categories)

        self.stdout.write(self.style.SUCCESS("\nSuccessfully loaded default categories\n"))
