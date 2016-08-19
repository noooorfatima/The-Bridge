# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_bridge', '0010_auto_20160809_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordpropertygreek',
            old_name='reg_adject_adv_form',
            new_name='reg_adj_adv',
        ),
    ]
