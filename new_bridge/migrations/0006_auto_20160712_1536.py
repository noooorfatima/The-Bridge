# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0005_auto_20160615_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='appearance',
            field=models.CharField(max_length=52, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='appearance',
            field=models.CharField(max_length=52, null=True),
            preserve_default=True,
        ),
    ]
