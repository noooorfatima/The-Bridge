# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0016_auto_20161011_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='logeion_link',
            field=models.CharField(max_length=700, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='logeion_link',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
