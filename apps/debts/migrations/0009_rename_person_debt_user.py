# Generated by Django 4.1.3 on 2022-12-26 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("debts", "0008_alter_debt_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="debt",
            old_name="person",
            new_name="user",
        ),
    ]
