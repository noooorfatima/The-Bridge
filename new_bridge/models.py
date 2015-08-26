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
from treebeard.mp_tree import MP_Node

class TextStructureNode(MP_Node):
    text_name = models.CharField(max_length=52, blank=True)
    subsection_level = models.SmallIntegerField(blank=False)
    subsection_number = models.IntegerField(blank=False)
    least_mindiv = models.IntegerField(blank=False)

    node_order_by = ['subsection_number']
    def __unicode__(self):
        #Climb tree to find parent location information:
        loc_string = ""
        parent = self      
        while not parent.is_root():
            loc_string =unicode(parent.subsection_number) + '.' + loc_string
            parent = parent.get_parent()
        #Descend tree to find child location information:
        child = self
        while not child.is_leaf():
            child = child.get_last_child()
            loc_string += '.'+'x'
        return self.text_name + '\t' + loc_string

class TextStructureGlossary(models.Model):
    text_name = models.CharField(max_length=52, blank=False)
    subsection_level = models.SmallIntegerField(blank=False)
    subsection_name = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nSUBSECTION LVL:\t'+self.subsection_level
        s += '\nSUBSECTION NAME:\t'+self.subsection_name
        return s

class WordAppearences(models.Model):
    text_name = models.CharField(max_length=52, blank=False)
    word_id = models.IntegerField(blank=False)
    mindiv = models.SmallIntegerField(blank=False)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+self.word_id
        s += '\nLOCATION:\t'+self.mindiv
        return s

#class TextMetadata(models.Model):
#   human-readable text name
#   other meta-data?
#class WordProperties(models.Model):


class BookTable(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=30, blank=True) 
    appearences = models.CharField(db_column='Appearences', max_length=17360, blank=True) 
    field_book_text = models.CharField(db_column='BookText', max_length=52, blank=True) 
    def __unicode__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'book_table'

class WordTable(models.Model):
    title = models.CharField(db_column='title', max_length=30, blank=True) 
    display_lemma = models.CharField(db_column='display_lemma', max_length=84, blank=True) 
    display_lemma_macronless = models.CharField(db_column='display_lemma_macronless', max_length=83, blank=True) 
    english_core = models.CharField(db_column='english_core', max_length=155, blank=True) 
    english_extended = models.CharField(db_column='english_extended', max_length=247, blank=True) 
    lnm_definition = models.CharField(db_column='lnm_definition', max_length=74, blank=True) 
    aeneid_definition = models.CharField(db_column='aeneid_definition', max_length=1168, blank=True) 
    catullus_definition = models.CharField(db_column='catullus_definition', max_length=245, blank=True) 
    decl = models.CharField(db_column='decl', max_length=1, blank=True) 
    conj = models.CharField(db_column='conj', max_length=1, blank=True) 
    reg_adj_adv = models.CharField(db_column='reg_adj_adv', max_length=1, blank=True) 
    proper = models.CharField(db_column='proper', max_length=1, blank=True) 
    part_of_speech = models.CharField(db_column='part_of_speech', max_length=24, blank=True) 
    dcc_frequency_rank = models.CharField(db_column='dcc_frequency_rank', max_length=5, blank=True) 
    dcc_frequency_group = models.CharField(db_column='dcc_frenquency_group', max_length=2, blank=True) 
    dcc_semantic_group = models.CharField(db_column='dcc_semantic_group', max_length=34, blank=True) 
    def __unicode__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'word_table'


class BookTitles(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') 
    def __unicode__(self):
        return self.title_of_book
    class Meta:
        managed = True
        db_table = 'book_titles'

class BookTableGreek(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(db_column='Title', max_length=43, blank=True) 
    appearences = models.CharField(db_column='Appearences', max_length=8, blank=True) 
    field_book_text = models.CharField(db_column=' Book/Text', max_length=44, blank=True) 
    def __unicode__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'book_table_greek'

class WordTableGreek(models.Model):
    title = models.CharField(db_column='TITLE', max_length=43, blank=True, null=True) 
    accented_lemma = models.CharField(db_column='accented lemma', max_length=50, blank=True, null=True) 
    search_lemma = models.CharField(db_column='SEARCH LEMMA', max_length=43, blank=True, null=True) 
    display_lemma = models.CharField(db_column='DISPLAY LEMMA', max_length=175, blank=True, null=True) 
    english_definition = models.CharField(db_column='English Definition', max_length=135, blank=True, null=True) 
    questions = models.IntegerField(db_column='Questions', blank=True, null=True) 
    decl = models.CharField(db_column='Decl', max_length=4, blank=True, null=True) 
    idiom = models.IntegerField(db_column='Idiom', blank=True, null=True) 
    reg_adject_adv_form = models.IntegerField(db_column='Reg Adject/Adv/Form', blank=True, null=True) 
    proper = models.IntegerField(db_column='Proper', blank=True, null=True) 
    part_of_speech = models.CharField(db_column='Part Of Speech', max_length=24, blank=True, null=True) 
    exclude_1_0 = models.IntegerField(db_column='Exclude 1/0', blank=True, null=True) 
    notes = models.CharField(db_column='Notes', max_length=34, blank=True, null=True) 
    dcc_semantic_group = models.CharField(db_column='DCC SEMANTIC GROUP', max_length=34, blank=True, null=True) 
    dcc_core_frequency = models.CharField(db_column='DCC Core Frequency', max_length=4, blank=True, null=True) 
    herodotus_1_frequency_rank = models.IntegerField(db_column='Herodotus 1 frequency rank', blank=True, null=True) 
    def __unicode__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'word_table_greek'

class BookTitlesGreek(models.Model):
    title_of_book = models.TextField(db_column='Title of Book') 
    def __unicode__(self):
        return self.title_of_book
    class Meta:
        managed = True
        db_table = 'book_titles_greek'
