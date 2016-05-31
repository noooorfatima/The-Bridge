# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpropertygreek',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='wordpropertylatin',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
