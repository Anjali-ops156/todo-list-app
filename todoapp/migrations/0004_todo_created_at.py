# Generated by Django 5.2.4 on 2025-08-01 17:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0003_todo_delete_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
