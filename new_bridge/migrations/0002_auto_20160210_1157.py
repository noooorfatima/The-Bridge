# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='aeneid_definition',
            field=models.CharField(max_length=1168, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='catullus_definition',
            field=models.CharField(max_length=245, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='conj',
            field=models.CharField(max_length=1, null=True, db_column='conj', blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='dcc_frequency_group',
            field=models.CharField(max_length=2, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='dcc_semantic_group',
            field=models.CharField(max_length=34, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='decl',
            field=models.CharField(max_length=1, null=True, db_column='decl', blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='display_lemma',
            field=models.CharField(max_length=84, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='display_lemma_macronless',
            field=models.CharField(max_length=83, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='english_core',
            field=models.CharField(max_length=155, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='english_extended',
            field=models.CharField(max_length=247, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='lnm_definition',
            field=models.CharField(max_length=74, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='part_of_speech',
            field=models.CharField(max_length=24, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='proper',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='reg_adj_adv',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='title',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
