# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0012_auto_20160818_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='english_extended',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
