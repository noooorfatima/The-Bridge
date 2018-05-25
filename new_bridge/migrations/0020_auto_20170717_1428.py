# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0019_auto_20170717_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordappearencesgreek',
            name='logeion_link',
        ),
        migrations.RemoveField(
            model_name='wordappearenceslatin',
            name='logeion_link',
        ),
        migrations.AddField(
            model_name='wordpropertygreek',
            name='logeion_link',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordpropertylatin',
            name='logeion_link',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
