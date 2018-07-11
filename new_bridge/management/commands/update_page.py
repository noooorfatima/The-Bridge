#import argparse
import sys
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/')
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/new_bridge/management/commands')
from .get_data import *
from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import WordPropertyLatin,WordPropertyGreek, TextStructureGlossary,TextMetadata
from . import text_import
#Might need to add argument specifying which sort it is (greek|latin)
'''
Adds a manage.py command that does ALL of the heavy lifting
that used to be involved in updating the database.
Basically this part of the script formats the csv and then calls Jack's script, text_import.py

NOTE** I made this flexible for when the update to SHORTDEF and LONGDEF occurs
BUT IT IS NOT GENERALLY FLEXIBLE
'''
class Command(BaseCommand):
	help = "Imports/updates the database"
	def add_arguments(self,parser):
		parser.add_argument("inputCSVFile",nargs=1, type=str, help="Name of file to import (include .csv)")
		parser.add_argument("language",nargs=1, type=str, help="The language we are importing for (Greek or Latin)")

	def handle(self, *args, **options):
		print(args, 'args')
		headers = get_headers(args[0])

		lang=args[1]
		print(lang)
		data_dict2 = get_data_list_of_dicts(args[0])
		index = 0
		name = headers[1]
		try:
			TextMetadata.objects.get(name_for_humans=name)
		except Exception as e:
			print( "Got an error, text name does not match any text metadata")
			print ("Current text is:", name)
			error =  {'name_error' : name}
			return str(error)
		if "LOCALDEF" in headers:
			tmd = TextMetadata.objects.get(name_for_humans=name)
			tmd.local_def=True
			tmd.save()
		for item in data_dict2: #would love to make this a list comprehension
			the_title = data_dict2[index]['TITLE']
			locations = item[name].split(",")

			for loc in locations:
				try:
					if loc.count(".") > 0:
						raise ValueError
				except ValueError:
					print( "Got a ValueError, are there . instead of _?")
					print ("Loction with a problem is:", loc)
					error =  {'dots_error' : loc}
					return str(error)

			if lang == "Latin":
				try:
					#print("the_title in update_page Latin", the_title)
					word_id=WordPropertyLatin.objects.get(title=the_title).id
				except:
					print("exception: %s" % the_title)
					error = {"dots_error" : the_title}
					return str(error)
					pass

			elif lang == "Greek":
				try:
					#print(index)
					#print(the_title)
					#print(WordPropertyGreek.objects.filter(title=the_title))
					#print("")
					word_id=WordPropertyGreek.objects.get(title=the_title).id
				except:
					print("exception: %s" % the_title)
					error = {"dots_error" : the_title}
					return str(error)
					pass
			try:
				data_dict2[index]['word_id']=word_id
				index = index + 1
			except UnboundLocalError:
				print( "Got a UnboundLocalError, likely picked wrong language")
				print ("Current language is:", lang)
				error =  {'lang_error' : lang}
				return str(error)




		headers.insert(0, 'word_id') #edits the existing list, we don't need it in its old form so we don't need to create a new list
		write_data_dicts('temp_output.csv', headers, data_dict2)
		error = text_import.main('temp_output.csv',lang)
		if error != None:
			return str(error)
