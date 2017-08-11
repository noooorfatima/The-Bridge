# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0017_auto_20170726_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordpropertygreek',
            name='corpus_rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordpropertylatin',
            name='corpus_rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
