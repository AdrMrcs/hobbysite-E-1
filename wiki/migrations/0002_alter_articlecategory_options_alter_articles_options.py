# Generated by Django 5.0.3 on 2024-03-19 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='articles',
            options={'ordering': ['createdOn']},
        ),
    ]
