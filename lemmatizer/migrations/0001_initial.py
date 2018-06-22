# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='formatlemmatizedtext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/tmp/format_temp_file.txt'), upload_to=b'', blank=True)),
                ('in_format', models.CharField(default=b'Excel', max_length=5, choices=[(b'csv', b'csv'), (b'Excel', b'Excel')])),
                ('out_format', models.CharField(default=b'csv', max_length=5, choices=[(b'csv', b'csv'), (b'Excel', b'Excel')])),
                ('question', models.CharField(default=b'I + III = ', max_length=17)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='lemmmatizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(default=b'latin', max_length=5, choices=[(b'latin', b'Latin'), (b'greek', b'Greek')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/tmp/lematizer_temp_file.txt'), upload_to=b'', blank=True)),
                ('text', models.TextField(default=b'', blank=True)),
                ('lem_format', models.CharField(default=b'bridge', max_length=8, choices=[(b'bridge', b'Bridge'), (b'morpheus', b'Morpheus')])),
                ('lem_level', models.CharField(default=b'Ambiguous', max_length=11, choices=[(b'Ambiguous', b'Ambiguous'), (b'Unambiguous', b'Unambiguous')])),
                ('out_format', models.CharField(default=b'Excel', max_length=5, choices=[(b'csv', b'csv'), (b'Excel', b'Excel')])),
                ('question', models.CharField(default=b'VII - IV = ', max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
