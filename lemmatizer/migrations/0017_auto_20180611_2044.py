# Generated by Django 2.0.6 on 2018-06-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0016_auto_20180607_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default='I + I = II', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default='IV - IV = ', max_length=15),
        ),
    ]
