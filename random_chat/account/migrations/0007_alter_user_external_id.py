# Generated by Django 4.1.1 on 2023-04-04 05:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_alter_user_external_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="external_id",
            field=models.UUIDField(
                default=uuid.UUID("fab25f0c-334b-4ce8-bdc9-0750ff12d101"), unique=True
            ),
        ),
    ]