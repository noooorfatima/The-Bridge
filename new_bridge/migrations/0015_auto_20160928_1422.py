# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0014_auto_20160921_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
