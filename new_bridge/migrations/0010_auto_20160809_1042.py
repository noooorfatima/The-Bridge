# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0009_auto_20160809_1025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordpropertygreek',
            old_name='logeion_definition',
            new_name='logeion_def',
        ),
    ]
