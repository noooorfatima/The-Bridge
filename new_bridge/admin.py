from django.contrib import admin
from models import WordPropertyLatin,TextStructureGlossary,TextMetadata,WordPropertyGreek
import os
#This creates a txt file that full_import than uses to decide which field names to use
#Didn't use anything flexible here, but am shooting for everything else to be quite flexible (in terms of working from different directories
os.chdir('new_bridge/management/commands/')
with open('WordPropertyLatin_field_names.txt', 'w') as f:
	for field in WordPropertyLatin._meta.get_all_field_names():
		f.write(field+',')
os.chdir('../../../')

admin.site.register(WordPropertyLatin)
admin.site.register(TextStructureGlossary)
admin.site.register(TextMetadata)
admin.site.register(WordPropertyGreek)

