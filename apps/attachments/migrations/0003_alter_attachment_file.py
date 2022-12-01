# Generated by Django 4.1.3 on 2022-12-01 15:01

import apps.attachments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attachments", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to=apps.attachments.models.upload_to_user_id),
        ),
    ]