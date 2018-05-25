# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0023_auto_20170717_1438'),
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
    ]
