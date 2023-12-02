# Generated by Django 4.2.7 on 2023-11-25 17:08

from django.db import migrations, models
import helpers.media_upload


class Migration(migrations.Migration):
    dependencies = [
        ("pizza", "0002_pizza_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Burger",
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
                ("burger_name", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
                ("rate", models.FloatField(default=0)),
                ("prepare_time", models.FloatField(blank=True, null=True)),
                ("calories", models.FloatField(blank=True)),
                ("price", models.FloatField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=helpers.media_upload.upload_burger_image,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]