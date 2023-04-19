# Generated by Django 4.1.1 on 2023-04-03 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_alter_user_external_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="external_id",
            field=models.UUIDField(
                default=uuid.UUID("fd184cf2-3e2a-4dcd-a539-ae7608c61542"), unique=True
            ),
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "ONLINE"),
                            (2, "OFFLINE"),
                            (3, "AVAILABLE"),
                            (4, "BUSY"),
                        ],
                        default=2,
                    ),
                ),
                (
                    "gender",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "MALE"),
                            (2, "FEMALE"),
                            (3, "OTHER"),
                            (99, "DO_NOT_WANT_TO_DISCOLSE"),
                        ],
                        default=99,
                    ),
                ),
                ("age", models.IntegerField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]