# Generated by Django 4.1.3 on 2022-12-15 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("debts", "0006_alter_debt_partial_paid_amount"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="debt",
            name="currency",
        ),
    ]