# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0025_auto_20170717_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordpropertygreek',
            old_name='logeion_link',
            new_name='logeion_url',
        ),
        migrations.RenameField(
            model_name='wordpropertylatin',
            old_name='logeion_link',
            new_name='logeion_url',
        ),
        migrations.AddField(
            model_name='wordpropertygreek',
            name='corpus_rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordpropertylatin',
            name='corpus_rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
