# Generated by Django 4.1.3 on 2022-12-01 15:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("expenses", "0003_alter_category_image"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="category",
            unique_together={("name", "user")},
        ),
    ]