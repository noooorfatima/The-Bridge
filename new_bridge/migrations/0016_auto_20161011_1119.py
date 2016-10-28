# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0015_auto_20160928_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textstructureglossary',
            name='text_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='textstructurenode',
            name='text_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='wordappearencesgreek',
            name='appearance',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='wordappearencesgreek',
            name='text_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='wordappearencesgreek',
            name='text_name_for_computers',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordappearenceslatin',
            name='text_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='wordappearenceslatin',
            name='text_name_for_computers',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='title',
            field=models.CharField(max_length=60, blank=True),
        ),
    ]
