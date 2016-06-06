# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpcenter', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, help_text='The parent category for the article.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='helpcenter.Category', verbose_name='Article Category'),
        ),
    ]
