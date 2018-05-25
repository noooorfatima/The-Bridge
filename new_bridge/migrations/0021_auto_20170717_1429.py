# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0020_auto_20170717_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordpropertygreek',
            name='logeion_link',
        ),
        migrations.RemoveField(
            model_name='wordpropertylatin',
            name='logeion_link',
        ),
    ]
