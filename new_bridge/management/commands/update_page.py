#import argparse
import sys
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/')
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/new_bridge/management/commands')
from get_data import *
from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import WordPropertyLatin,WordPropertyGreek, TextStructureGlossary,TextMetadata
import text_import
#Might need to add argument specifying which sort it is (greek|latin)
'''
Adds a manage.py command that does ALL of the heavy lifting 
that used to be involved in updating the database.

NOTE** I made this flexible for when the update to SHORTDEF and LONGDEF occurs
BUT IT IS NOT GENERALLY FLEXIBLE
'''
class Command(BaseCommand):
	help = "Imports/updates the database"
	def add_arguments(self,parser):
		parser.add_argument("inputCSVFile",nargs=1, type=str, help="Name of file to import (include .csv)")
		parser.add_argument("language",nargs=1, type=str, help="The language we are importing for (Greek or Latin)")

	def handle(self, *args, **options):
		headers = get_headers(args[0])
		lang=args[1]
		print lang
		data_dict2 = get_data_list_of_dicts(args[0])
		index = 0
		name = headers[1]
		if "LOCALDEF" in headers:
			print "Local def exists for", name
			tmd = TextMetadata.objects.get(name_for_humans=name)
			tmd.local_def=True
			tmd.save()
		for item in data_dict2:
			the_title = data_dict2[index]['TITLE']
			if lang == "Latin":
				word_id=WordPropertyLatin.objects.get(title=the_title).id
			elif lang == "Greek":
				word_id=WordPropertyGreek.objects.get(title=the_title).id
			data_dict2[index]['word_id']=word_id
			index = index + 1
		new_headers2 = ['word_id'] + headers
		write_data_dicts('temp_output.csv', new_headers2, data_dict2)
		error = text_import.main('temp_output.csv',lang)
		if error != None:
			return str(error)