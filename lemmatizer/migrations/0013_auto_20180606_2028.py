# Generated by Django 2.0.6 on 2018-06-06 20:28

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0012_auto_20180531_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='file',
            field=models.FileField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='/tmp/format_temp_file.txt'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='in_format',
            field=models.CharField(choices=[('csv', 'csv'), ('Excel', 'Excel')], default='Excel', max_length=5),
        ),
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='out_format',
            field=models.CharField(choices=[('csv', 'csv'), ('Excel', 'Excel')], default='csv', max_length=5),
        ),
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default='V - IV = ', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='file',
            field=models.FileField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='/tmp/lematizer_temp_file.txt'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='language',
            field=models.CharField(choices=[('latin', 'Latin'), ('greek', 'Greek')], default='latin', max_length=5),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='lem_format',
            field=models.CharField(choices=[('bridge', 'Bridge'), ('morpheus', 'Morpheus')], default='bridge', max_length=8),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='lem_level',
            field=models.CharField(choices=[('Ambiguous', 'Ambiguous'), ('Unambiguous', 'Unambiguous')], default='Ambiguous', max_length=11),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='out_format',
            field=models.CharField(choices=[('csv', 'csv'), ('Excel', 'Excel')], default='Excel', max_length=5),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default='I - I = ', max_length=15),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
