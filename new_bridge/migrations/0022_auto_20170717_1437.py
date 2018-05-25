# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0021_auto_20170717_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='ldef',
            field=models.CharField(max_length=1168, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='ldef',
            field=models.CharField(max_length=1168, null=True, blank=True),
            preserve_default=True,
        ),
    ]
