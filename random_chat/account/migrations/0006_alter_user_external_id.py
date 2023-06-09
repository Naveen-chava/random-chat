# Generated by Django 4.1.1 on 2023-04-04 05:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_alter_user_external_id_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="external_id",
            field=models.UUIDField(
                default=uuid.UUID("78a9169e-6a95-4a6f-a23d-39f49f2c04f1"), unique=True
            ),
        ),
    ]
