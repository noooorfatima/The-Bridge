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
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=30, blank=True) # Field name made lowercase.
    appearences = models.CharField(db_column='Appearences', max_length=17360, blank=True) # Field name made lowercase.
    field_book_text = models.CharField(db_column=' Book/Text', max_length=52, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    class Meta:
        managed = False
        db_table = 'book_table'


class WordTable(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='TITLE', max_length=17, blank=True) # Field name made lowercase.
    display_lemma = models.CharField(db_column='DISPLAY LEMMA', max_length=84, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    #display_lemma_macronless = models.CharField(db_column='DISPLAY LEMMA MACRONLESS', max_length=78, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    #display_lemma_macron_field = models.CharField(db_column='DISPLAY LEMMA MACRON#', max_length=84, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    english_core = models.CharField(db_column='ENGLISH-CORE', max_length=126, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    english_extended = models.CharField(db_column='ENGLISH-EXTENDED', max_length=247, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    #aeneid_definition = models.CharField(db_column='AENEID-DEFINITION', max_length=696, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    #catullus_definition = models.CharField(db_column='CATULLUS-DEFINITION', max_length=154, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    lasla_morph_1 = models.CharField(db_column='LASLA MORPH 1', max_length=43, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    lasla_morph_2 = models.CharField(db_column='LASLA MORPH 2', max_length=42, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    lasla_combined = models.CharField(db_column='LASLA Combined', max_length=3, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    decl = models.CharField(db_column='Decl', max_length=1, blank=True) # Field name made lowercase.
    conj = models.CharField(db_column='Conj', max_length=2, blank=True) # Field name made lowercase.
    idiom = models.CharField(db_column='Idiom', max_length=1, blank=True) # Field name made lowercase.
    reg_adj_adv = models.CharField(db_column='Reg Adj/Adv', max_length=2, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    number = models.CharField(db_column='Number', max_length=1, blank=True) # Field name made lowercase.
    proper = models.CharField(db_column='Proper', max_length=1, blank=True) # Field name made lowercase.
    part_of_speech = models.CharField(db_column='Part Of Speech', max_length=12, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    #exclude_1_0 = models.CharField(db_column='Exclude 1/0', max_length=1, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    #notes = models.CharField(db_column='NOTES', max_length=123, blank=True) # Field name made lowercase.
    dcc_frequency_rank = models.CharField(db_column='DCC FREQUENCY RANK', max_length=12, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcc_frequency_group = models.CharField(db_column='DCC FREQUENCY GROUP', max_length=4, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcc_semantic_group = models.CharField(db_column='DCC SEMANTIC GROUP', max_length=34, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        managed = False
        db_table = 'word_table'


class BookTitles(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        managed = True
        db_table = 'book_titles'

    
class BookTableGreek(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=43, blank=True) # Field name made lowercase.
    appearences = models.CharField(db_column='Appearences', max_length=8, blank=True) # Field name made lowercase.
    field_book_text = models.CharField(db_column=' Book/Text', max_length=44, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    class Meta:
        managed = True
        db_table = 'book_table_greek'

class WordTableGreek(models.Model):
    title = models.CharField(db_column='TITLE', max_length=43, blank=True, null=True) # Field name made lowercase.
    accented_lemma = models.CharField(db_column='accented lemma', max_length=50, blank=True, null=True) # Field renamed to remove unsuitable characters.
    search_lemma = models.CharField(db_column='SEARCH LEMMA', max_length=43, blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_lemma = models.CharField(db_column='DISPLAY LEMMA', max_length=175, blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    english_definition = models.CharField(db_column='English Definition', max_length=135, blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    questions = models.IntegerField(db_column='Questions', blank=True, null=True) # Field name made lowercase.
    decl = models.CharField(db_column='Decl', max_length=4, blank=True, null=True) # Field name made lowercase.
    idiom = models.IntegerField(db_column='Idiom', blank=True, null=True) # Field name made lowercase.
    reg_adject_adv_form = models.IntegerField(db_column='Reg Adject/Adv/Form', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    proper = models.IntegerField(db_column='Proper', blank=True, null=True) # Field name made lowercase.
    part_of_speech = models.CharField(db_column='Part Of Speech', max_length=24, blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    exclude_1_0 = models.IntegerField(db_column='Exclude 1/0', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    notes = models.CharField(db_column='Notes', max_length=34, blank=True, null=True) # Field name made lowercase.
    dcc_semantic_group = models.CharField(db_column='DCC SEMANTIC GROUP', max_length=34, blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcc_core_frequency = models.CharField(db_column='DCC Core Frequency', max_length=4, blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    herodotus_1_frequency_rank = models.IntegerField(db_column='Herodotus 1 frequency rank', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        managed = True
        db_table = 'word_table_greek'

class BookTitlesGreek(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        managed = True
        db_table = 'book_titles_greek'
