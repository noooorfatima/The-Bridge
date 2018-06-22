# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0003_auto_20180529_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default=b'VIII - VIII = ', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default=b'I + I = II', max_length=15),
        ),
    ]
