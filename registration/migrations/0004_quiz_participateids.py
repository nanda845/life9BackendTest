# Generated by Django 2.1 on 2019-03-02 10:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20190302_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='participateIds',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), default=list, size=None),
        ),
    ]