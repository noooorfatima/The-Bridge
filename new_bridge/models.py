# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = True` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class BookTable(models.Model):
    title = models.CharField(db_column='Title', max_length=25, blank=True) # Made lowercase.
    appearences = models.CharField(db_column='Appearences', max_length=17360, blank=True) # Made lowercase.
    field_book_text = models.CharField(db_column=' Book/Text', max_length=52, blank=True) # Made lowercase. Unusitable char.s removed. Field renamed because it started with '_'.
    class Meta:
        managed = True
        db_table = 'book_table'

class WordTable(models.Model):
    title = models.CharField(db_column='TITLE', max_length=25, blank=True) # Made lowercase.
    display_lemma = models.CharField(db_column='DISPLAY LEMMA', max_length=90, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    english_core = models.CharField(db_column='ENGLISH-CORE', max_length=130, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    english_extended = models.CharField(db_column='ENGLISH-EXTENDED', max_length=246, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    lasla_morph_1 = models.CharField(db_column='LASLA MORPH 1', max_length=2, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    lasla_morph_2 = models.CharField(db_column='LASLA MORPH 2', max_length=1, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    lasla_combined = models.CharField(db_column='LASLA Combined', max_length=3, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    decl = models.IntegerField(db_column='Decl', blank=True, null=True) # Made lowercase.
    conj = models.IntegerField(db_column='Conj', blank=True, null=True) # Made lowercase.
    idiom = models.IntegerField(db_column='Idiom', blank=True, null=True) # Made lowercase.
    reg_adj_adv = models.IntegerField(db_column='Reg Adj/Adv', blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    number = models.IntegerField(db_column='Number', blank=True, null=True) # Made lowercase.
    proper = models.CharField(db_column='Proper', max_length=9, blank=True, null=True) # Made lowercase.
    part_of_speech = models.CharField(db_column='Part Of Speech', max_length=12, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    dcc_frequency_rank = models.IntegerField(db_column='DCC FREQUENCY RANK', blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    dcc_frequency_group = models.IntegerField(db_column='DCC FREQUENCY GROUP', blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    dcc_semantic_group = models.CharField(db_column='DCC SEMANTIC GROUP', max_length=34, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    class Meta:
        managed = True
        db_table = 'word_table'


class BookTitles(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') # Made lowercase. Unusitable char.s removed.
    class Meta:
        managed = True
        db_table = 'book_titles'

    
class BookTableGreek(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=43, blank=True) # Made lowercase.
    appearences = models.CharField(db_column='Appearences', max_length=8, blank=True) # Made lowercase.
    field_book_text = models.CharField(db_column=' Book/Text', max_length=44, blank=True) # Made lowercase. Unusitable char.s removed. Field renamed because it started with '_'.
    class Meta:
        managed = True
        db_table = 'book_table_greek'

class WordTableGreek(models.Model):
    title = models.CharField(db_column='TITLE', max_length=43, 
            blank=True, null=True) # Made lowercase.
    accented_lemma = models.CharField(db_column='accented lemma', max_length=50, blank=True, null=True) # Unusitable char.s removed.
    search_lemma = models.CharField(db_column='SEARCH LEMMA', max_length=43, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    display_lemma = models.CharField(db_column='DISPLAY LEMMA', max_length=175, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    english_definition = models.CharField(db_column='English Definition', max_length=135, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    questions = models.IntegerField(db_column='Questions', blank=True, null=True) # Made lowercase.
    decl = models.CharField(db_column='Decl', max_length=4, blank=True, null=True) # Made lowercase.
    idiom = models.IntegerField(db_column='Idiom', blank=True, null=True) # Made lowercase.
    reg_adject_adv_form = models.IntegerField(db_column='Reg Adject/Adv/Form', blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    proper = models.IntegerField(db_column='Proper', blank=True, null=True) # Made lowercase.
    part_of_speech = models.CharField(db_column='Part Of Speech', max_length=24, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    exclude_1_0 = models.IntegerField(db_column='Exclude 1/0', blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    notes = models.CharField(db_column='Notes', max_length=34, blank=True, null=True) # Made lowercase.
    dcc_semantic_group = models.CharField(db_column='DCC SEMANTIC GROUP', max_length=34, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    dcc_core_frequency = models.CharField(db_column='DCC Core Frequency', max_length=4, blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    herodotus_1_frequency_rank = models.IntegerField(db_column='Herodotus 1 frequency rank', blank=True, null=True) # Made lowercase. Unusitable char.s removed.
    class Meta:
        managed = True
        db_table = 'word_table_greek'

class BookTitlesGreek(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') # Made lowercase. Unusitable char.s removed.
    class Meta:
        managed = True
        db_table = 'book_titles_greek'

