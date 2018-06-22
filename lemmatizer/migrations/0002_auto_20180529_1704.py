# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default=b'VI + V = ', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default=b'IX + I = ', max_length=15),
        ),
    ]
