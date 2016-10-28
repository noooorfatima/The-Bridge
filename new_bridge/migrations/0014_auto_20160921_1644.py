# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0013_auto_20160819_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='accented_lemma',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='dcc_semantic_group',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='display_lemma',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='english_definition',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='logeion_def',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='logeion_lemma',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='notes',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='part_of_speech',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='questions',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='search_lemma',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='title',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
