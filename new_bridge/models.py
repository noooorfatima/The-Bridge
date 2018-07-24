
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = True` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.


from django.db import models
from treebeard.mp_tree import MP_Node

class TextStructureNode(MP_Node):
    text_name = models.CharField(max_length=100, blank=True)
    subsection_level = models.SmallIntegerField(blank=False)
    subsection_id = models.CharField(max_length=6, blank=False)
    least_mindiv = models.IntegerField(blank=False)
    path =  models.CharField(max_length = 300, blank = False)
    node_order_by = ['least_mindiv']
    def __unicode__(self):
        #Climb tree to find parent location information:
        loc_string = ""
        parent = self
        while not parent.is_root():
            loc_string =str(parent.subsection_id) + '.' + loc_string
            print((loc_string, 'loc string'))
            parent = parent.get_parent()
        text_name = parent.text_name
        #Descend tree to find child location information:
        child = self
        while not child.is_leaf():
            child = child.get_last_child()
            loc_string += '.'+'x'
        return text_name + '\t' + loc_string

class TextStructureGlossary(models.Model):
    text_name = models.CharField(max_length=100, blank=False)
    subsection_level = models.SmallIntegerField(blank=False)
    subsection_name = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += ' SUBSECTION LVL:\t'+str(self.subsection_level)
        s += ' SUBSECTION NAME:\t'+self.subsection_name
        return s

class WordAppearencesLatin(models.Model):
    text_name = models.CharField(max_length=100, blank=False)
    text_name_for_computers = models.CharField(max_length=100, blank=True, null=True)
    word = models.ForeignKey('WordPropertyLatin', blank=False,null=True, on_delete=models.CASCADE, related_name = "field3")
    mindiv = models.SmallIntegerField(blank=False)
    appearance = models.CharField(max_length=52, blank=False,null=True)
    local_def = models.CharField(max_length=1168, blank=True,null=True)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+ str(self.word_id)
        s += '\nLOCATION:\t'+str(self.mindiv)
        s += ' WORD: ' + self.word.title
        return s
    def __str__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+str(self.word_id)
        s += '\nLOCATION:\t'+str(self.mindiv)
        s += '\nLOCAL DEF:\t' + str(self.local_def)
        return s

class WordAppearencesGreek(models.Model):
    text_name = models.CharField(max_length=100, blank=False)
    text_name_for_computers = models.CharField(max_length=100, blank=True, null=True)
    word = models.ForeignKey('WordPropertyGreek', blank=False,null=True, on_delete=models.CASCADE, related_name = "field3")
    mindiv = models.SmallIntegerField(blank=False)
    appearance = models.CharField(max_length=100, blank=False,null=True)
    local_def = models.CharField(max_length=1168, blank=True,null=True)
    def __unicode__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+str(self.word_id)
        s += '\nLOCATION:\t'+str(self.mindiv)
        s += '\nLOCAL DEF:\t' + str(self.local_def)
        return s
    def __str__(self):
        s = 'TEXT:\t'+self.text_name
        s += '\nWORD ID:\t'+str(self.word_id)
        s += '\nLOCATION:\t'+str(self.mindiv)
        s += '\nLOCAL DEF:\t' + str(self.local_def)
        return s

class TextMetadata(models.Model):
    name_for_humans = models.CharField(max_length=100, blank=False)
    name_for_computers = models.CharField(max_length=100, blank=False)
    language = models.CharField(max_length=10, blank=False)
    local_def = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name_for_humans

class WordPropertyLatin(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, blank=True)
    display_lemma = models.CharField(max_length=84, blank=True)
    display_lemma_macronless = models.CharField(max_length=83, blank=True)
    english_core = models.CharField(max_length=155, blank=True)
    english_extended = models.CharField(max_length=500, blank=True)
    lnm_definition = models.CharField(max_length=74, blank=True)
    aeneid_definition = models.CharField(max_length=1168, blank=True)
    catullus_definition = models.CharField(max_length=245, blank=True)
    decl = models.CharField(db_column='decl', max_length=10, blank=True)
    conj = models.CharField(db_column='conj', max_length=10, blank=True)
    reg_adj_adv = models.CharField(max_length=1, blank=True)
    proper = models.CharField(max_length=1, blank=True)
    part_of_speech = models.CharField(max_length=24, blank=True)
    dcc_frequency_group = models.CharField(max_length=2, blank=True)
    dcc_semantic_group = models.CharField(max_length=34, blank=True)
    logeion_url = models.URLField(max_length=200, blank=True, null=True)
    corpus_rank = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

#I changed all the integer fields to text fields because it doesn't like importing blank integer fields
#Note exlude is still int because the spreadsheet doesn't have it
class WordPropertyGreek(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    accented_lemma = models.CharField(max_length=500, blank=True, null=True)
    logeion_lemma = models.CharField(max_length=500, blank=True, null=True)
    search_lemma = models.CharField(max_length=500, blank=True, null=True)
    display_lemma = models.CharField(max_length=500, blank=True, null=True)
    english_definition = models.CharField(max_length=500, blank=True, null=True)
    logeion_def = models.CharField(max_length=500, blank=True, null=True)
    #questions = models.IntegerField(blank=True, null=True)
    questions = models.CharField(max_length=500, blank=True, null=True)
    decl = models.CharField(max_length=4, blank=True, null=True)
    #idiom = models.IntegerField(blank=True, null=True)
    idiom = models.CharField(max_length=1, blank=True, null=True)
    #reg_adject_adv_form = models.IntegerField(blank=True, null=True)
    reg_adj_adv = models.CharField(max_length=1, blank=True, null=True)
    #proper = models.IntegerField(blank=True, null=True)
    proper = models.CharField(max_length=1, blank=True, null=True)
    part_of_speech = models.CharField(max_length=500, blank=True, null=True)
    exclude_1_0 = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    dcc_semantic_group = models.CharField(max_length=500, blank=True, null=True)
    logeion_url = models.URLField(max_length=200, blank=True, null=True)
    corpus_rank = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return self.title
    def __str__(self): #for greek it probably should use unicode, since it does not use the latin alphabet, but this is a django 1 to 2 thing.
        return self.title

class BookTitlesGreek(models.Model):
    #book type for sorting on home page
    #Note that the are valued such that they will be in the appropriate order when sorted alphabetacally
    title_of_book = models.TextField(db_column='Title of Book')
    LIST = 'LI'
    TEXT = 'TE'
    TEXTBOOK = 'TK'
    BOOK_TYPE_CHOICES= (
        (LIST,'List'),
        (TEXT,"Text"),
        (TEXTBOOK,'Textbook')
    )
    book_type = models.CharField(max_length=2,choices=BOOK_TYPE_CHOICES,null=True)
    def __unicode__(self):
        return self.title_of_book
    class Meta:
        managed = True
        db_table = 'book_titles_greek'

#Old thing that we might still be able to use at some point (ie, if we abandon name for humans all together, we could search based on this)
#Shouldn't use plurals
class BookTitles(models.Model):
    title_of_book = models.TextField(db_column='Title of Book')
    #book type for sorting on home page
    #Note that the are valued such that they will be in the appropriate order when sorted alphabetacally
    LIST = 'LI'
    TEXT = 'TE'
    TEXTBOOK = 'TK'
    BOOK_TYPE_CHOICES= (
        (LIST,'List'),
        (TEXT,"Text"),
        (TEXTBOOK,'Textbook')
    )
    book_type = models.CharField(max_length=2,choices=BOOK_TYPE_CHOICES,null=True)
    def __unicode__(self):
        return self.title_of_book
    class Meta:
        managed = True
        db_table = 'book_titles'
