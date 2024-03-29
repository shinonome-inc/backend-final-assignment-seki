# Generated by Django 4.1 on 2022-09-09 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="誕生日"),
                ),
                (
                    "self_introduction",
                    models.TextField(
                        blank=True,
                        default="未設定",
                        max_length=160,
                        null=True,
                        verbose_name="自己紹介",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
