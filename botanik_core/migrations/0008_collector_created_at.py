# Generated by Django 5.2.3 on 2025-07-06 18:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botanik_core', '0007_tablepermissionarea_usergroup_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collector',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
