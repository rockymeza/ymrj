# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-28 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
        ),
    ]