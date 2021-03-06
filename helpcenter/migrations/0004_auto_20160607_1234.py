# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpcenter', '0003_article_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(db_index=True, help_text='An article title is restricted to 200 characters.', max_length=200, verbose_name='Article Title'),
        ),
    ]
