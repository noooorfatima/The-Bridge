# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0017_auto_20170717_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordappearencesgreek',
            name='logeion_link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='wordappearenceslatin',
            name='logeion_link',
            field=models.URLField(),
        ),
    ]
