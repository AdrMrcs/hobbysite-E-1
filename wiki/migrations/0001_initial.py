# Generated by Django 5.0.2 on 2024-05-08 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user_management", "0002_alter_profile_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArticleCategory",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Article",
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
                ("title", models.CharField(max_length=255)),
                ("entry", models.TextField()),
                ("headerImage", models.ImageField(null=True, upload_to="images/")),
                ("createdOn", models.DateTimeField(auto_now_add=True)),
                ("updatedOn", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="articleauthor",
                        to="user_management.profile",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="articlecategory",
                        to="wiki.articlecategory",
                    ),
                ),
            ],
            options={
                "ordering": ["-createdOn"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("entry", models.TextField()),
                ("createdOn", models.DateTimeField(auto_now_add=True)),
                ("updatedOn", models.DateTimeField(auto_now=True)),
                (
                    "article",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commentarticle",
                        to="wiki.article",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        default=1,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="commentauthor",
                        to="user_management.profile",
                    ),
                ),
            ],
            options={
                "ordering": ["createdOn"],
            },
        ),
    ]
