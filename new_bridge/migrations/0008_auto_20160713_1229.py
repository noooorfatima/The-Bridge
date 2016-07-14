# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0007_textmetadata_local_def'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='local_def',
            field=models.CharField(max_length=1168, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='local_def',
            field=models.CharField(max_length=1168, null=True, blank=True),
            preserve_default=True,
        ),
    ]
