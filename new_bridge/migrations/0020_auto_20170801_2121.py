# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0019_auto_20170731_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordpropertygreek',
            name='word_frequency',
        ),
        migrations.RemoveField(
            model_name='wordpropertylatin',
            name='word_frequency',
        ),
    ]
