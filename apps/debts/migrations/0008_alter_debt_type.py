# Generated by Django 4.1.3 on 2022-12-26 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debts", "0007_remove_debt_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debt",
            name="type",
            field=models.CharField(
                blank=True, choices=[("BORROW", "BORROW"), ("LEND", "LEND")], max_length=32, null=True
            ),
        ),
    ]
