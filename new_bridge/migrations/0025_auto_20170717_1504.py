# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0024_auto_20170717_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordpropertygreek',
            name='logeion_link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordpropertylatin',
            name='logeion_link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
