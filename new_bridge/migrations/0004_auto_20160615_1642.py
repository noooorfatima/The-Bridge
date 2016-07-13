# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0003_auto_20160615_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='idiom',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
    ]
