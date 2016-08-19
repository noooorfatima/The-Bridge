# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0011_auto_20160809_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='text_name_for_computers',
            field=models.CharField(max_length=52, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='text_name_for_computers',
            field=models.CharField(max_length=52, null=True, blank=True),
            preserve_default=True,
        ),
    ]
