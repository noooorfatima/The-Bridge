# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0022_auto_20170717_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordappearencesgreek',
            name='ldef',
        ),
        migrations.RemoveField(
            model_name='wordappearenceslatin',
            name='ldef',
        ),
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='logeion_link',
            field=models.CharField(max_length=1168, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='logeion_link',
            field=models.CharField(max_length=1168, null=True, blank=True),
            preserve_default=True,
        ),
    ]
