# Generated by Django 5.0.2 on 2024-05-08 04:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchstore', '0005_alter_producttype_options_product_owner_and_more'),
        ('user_management', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to='user_management.profile'),
        ),
    ]
