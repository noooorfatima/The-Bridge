# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0004_auto_20160615_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='proper',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='reg_adject_adv_form',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
    ]
