# Generated by Django 4.1.1 on 2023-03-22 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_address_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address_user", name="pin", field=models.PositiveIntegerField(),
        ),
    ]
