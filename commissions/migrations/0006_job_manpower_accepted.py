# Generated by Django 5.0.2 on 2024-05-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commissions", "0005_commission_created_by_alter_job_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="manpower_accepted",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
