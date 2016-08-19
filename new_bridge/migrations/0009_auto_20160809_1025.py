# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0008_auto_20160713_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='booktitles',
            name='book_type',
            field=models.CharField(max_length=2, null=True, choices=[('LI', 'List'), ('TE', 'Text'), ('TK', 'Textbook')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booktitlesgreek',
            name='book_type',
            field=models.CharField(max_length=2, null=True, choices=[('LI', 'List'), ('TE', 'Text'), ('TK', 'Textbook')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordpropertygreek',
            name='logeion_definition',
            field=models.CharField(max_length=240, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordpropertygreek',
            name='logeion_lemma',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
