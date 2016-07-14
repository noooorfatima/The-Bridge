# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0006_auto_20160712_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='textmetadata',
            name='local_def',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
