# Generated by Django 5.0.4 on 2024-05-05 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0002_alter_comment_commission'),
        ('user_management', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='people_required',
        ),
        migrations.AddField(
            model_name='commission',
            name='status',
            field=models.CharField(choices=[('OP', 'Open'), ('FU', 'Full'), ('CO', 'Completed'), ('DI', 'Discontinued')], default='OP', max_length=25),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('manpower_required', models.IntegerField()),
                ('status', models.CharField(choices=[('OP', 'Open'), ('FU', 'Full')], default='OP', max_length=25)),
                ('commission', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='commissions.commission')),
            ],
            options={
                'ordering': ['-status', '-manpower_required', 'role'],
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('RE', 'Rejected')], default='PE', max_length=25)),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.profile')),
                ('job', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='job_apps', to='commissions.job')),
            ],
            options={
                'ordering': ['status', '-applied_on'],
            },
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
