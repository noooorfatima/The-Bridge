# Generated by Django 2.0.6 on 2018-06-07 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0014_auto_20180607_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default='VI - III = ', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default='IV + II = ', max_length=15),
        ),
    ]
