# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookTitles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_of_book', models.TextField(db_column='Title of Book')),
            ],
            options={
                'db_table': 'book_titles',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookTitlesGreek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_of_book', models.TextField(db_column='Title of Book')),
            ],
            options={
                'db_table': 'book_titles_greek',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_for_humans', models.CharField(max_length=100)),
                ('name_for_computers', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextStructureGlossary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_name', models.CharField(max_length=52)),
                ('subsection_level', models.SmallIntegerField()),
                ('subsection_name', models.CharField(max_length=20, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextStructureNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('text_name', models.CharField(max_length=52, blank=True)),
                ('subsection_level', models.SmallIntegerField()),
                ('subsection_id', models.CharField(max_length=6)),
                ('least_mindiv', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordAppearencesGreek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_name', models.CharField(max_length=52)),
                ('mindiv', models.SmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordAppearencesLatin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_name', models.CharField(max_length=52)),
                ('mindiv', models.SmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordPropertyGreek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=43, null=True, blank=True)),
                ('accented_lemma', models.CharField(max_length=50, null=True, blank=True)),
                ('search_lemma', models.CharField(max_length=43, null=True, blank=True)),
                ('display_lemma', models.CharField(max_length=175, null=True, blank=True)),
                ('english_definition', models.CharField(max_length=135, null=True, blank=True)),
                ('questions', models.IntegerField(null=True, blank=True)),
                ('decl', models.CharField(max_length=4, null=True, blank=True)),
                ('idiom', models.IntegerField(null=True, blank=True)),
                ('reg_adject_adv_form', models.IntegerField(null=True, blank=True)),
                ('proper', models.IntegerField(null=True, blank=True)),
                ('part_of_speech', models.CharField(max_length=24, null=True, blank=True)),
                ('exclude_1_0', models.IntegerField(null=True, blank=True)),
                ('notes', models.CharField(max_length=34, null=True, blank=True)),
                ('dcc_semantic_group', models.CharField(max_length=34, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordPropertyLatin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, blank=True)),
                ('display_lemma', models.CharField(max_length=84, blank=True)),
                ('display_lemma_macronless', models.CharField(max_length=83, blank=True)),
                ('english_core', models.CharField(max_length=155, blank=True)),
                ('english_extended', models.CharField(max_length=247, blank=True)),
                ('lnm_definition', models.CharField(max_length=74, blank=True)),
                ('aeneid_definition', models.CharField(max_length=1168, blank=True)),
                ('catullus_definition', models.CharField(max_length=245, blank=True)),
                ('decl', models.CharField(max_length=1, db_column='decl', blank=True)),
                ('conj', models.CharField(max_length=1, db_column='conj', blank=True)),
                ('reg_adj_adv', models.CharField(max_length=1, blank=True)),
                ('proper', models.CharField(max_length=1, blank=True)),
                ('part_of_speech', models.CharField(max_length=24, blank=True)),
                ('dcc_frequency_group', models.CharField(max_length=2, blank=True)),
                ('dcc_semantic_group', models.CharField(max_length=34, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='wordappearenceslatin',
            name='word',
            field=models.ForeignKey(to='new_bridge.WordPropertyLatin', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wordappearencesgreek',
            name='word',
            field=models.ForeignKey(to='new_bridge.WordPropertyGreek', null=True),
            preserve_default=True,
        ),
    ]
