# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0002_auto_20160531_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='idiom',
            field=models.CharField(max_length=1, blank=True,null=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='proper',
            field=models.CharField(max_length=1, blank=True,null=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='questions',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='reg_adject_adv_form',
            field=models.CharField(max_length=1, blank=True, null=True),
        ),
    ]
