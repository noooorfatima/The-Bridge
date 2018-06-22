# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0002_auto_20180529_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default=b'I + I = II', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default=b'V - I = ', max_length=15),
        ),
    ]
