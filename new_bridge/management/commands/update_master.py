#import argparse
import sys
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/')
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/new_bridge/management/commands')
from get_data import *
from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import WordPropertyLatin,WordPropertyGreek, TextStructureGlossary
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
		print args[0]
		data_dict = get_data_list_of_dicts(args[0])
		print data_dict[1]
		headers = get_headers(args[0])
		print "Headers:", headers
		lang=args[1]
		print lang
		updated1=True
		updated2=True
		#print data_dict[0:5]
		#now finding the headers we wnat to deal with here
		wanted_list=[] #The indices of them will be here (indices as they appear in headers)
		#print  WordPropertyLatin._meta.get_all_field_names()
		fields = []
		if lang == 'Latin':
			for name in WordPropertyLatin._meta.get_all_field_names():
				fields = fields + [name.upper().replace('_',' ').replace('-',' ')]
			#print fields, "FIELDS"
		elif lang == 'Greek':
			print WordPropertyGreek._meta.get_all_field_names()
			for name in WordPropertyGreek._meta.get_all_field_names():
				fields = fields + [name.upper().replace('_',' ').replace('-',' ')]
		else:
			print "Got an unexpected language",lang
			return '{language_error : lang}'
		nohypen=[] # I'd like to think I did this as a joke because ticha had hypen instead of hyphen for a lot of the document
		for item in headers:
			nohypen=nohypen + [item.upper().replace('-',' ').replace('/', ' ')]
		#print nohypen, "NO HY"
		index = 0
		print "No Hypen", nohypen
		print "fields", fields
		for item in nohypen:
			print item, "ITEM"
			if item in fields:
				wanted_list=wanted_list+[index]
			elif item == 'LNM DEFENITION': #you see this shit? That's not how you spell definition
				wanted_list=wanted_list+[index]
			#Spreadsheet will eventually change without change to models, hardcoding for changes
			elif item == 'SHORTDEF':
				wanted_list=wanted_list+[index]
				updated1=True
			elif item == 'LONGDEF':
				wanted_list=wanted_list+[index]
				updated2=True
			elif item == 'LOGEIONDEF':
				wanted_list = wanted_list + [index]
			index = index + 1
		#print wanted_list


		new_headers = []
		unwanted = []
		index = 0
		for header in headers:
			if index in wanted_list:
				new_headers = new_headers + [headers[index]]
			else:
				unwanted = unwanted + [header]
			index = index + 1
		#print new_headers, "new_headers"

		index = 0
		for item in data_dict:
			data_dict[index]['id']=index+1
			for junk in unwanted:
				del data_dict[index][junk]
			#item['id'] = index
			index = index + 1
		#print data_dict[0]['id']
		new_headers = ['id'] + new_headers
		#print "#######################################"
		#print TextStructureGlossary.objects.all()
		#print WordPropertyLatin.objects.all()
		#print data_dict[0].keys()
		
		print "This takes a little while..."
		if lang=='Latin':
			#Hard coded for the spreadsheet update
			if updated1:
				english_core = 'SHORTDEF'
			else:
				english_core = 'ENGLISH-CORE'
			if updated2:
				english_extended = 'LONGDEF'
			else:
				english_extended = 'ENGLISH-EXTENDED'
			index = 0
			for item in data_dict:
				print index
				try:
					WordPropertyLatin.objects.update_or_create(
					title = item['TITLE'],
					defaults={
					#'id' : item['id'],
					'display_lemma' : item['DISPLAY LEMMA'],
					'display_lemma_macronless' : item['DISPLAY LEMMA MACRONLESS'],
					'english_core' : item[english_core],
					'english_extended' : item[english_extended],
				    'decl' : item['Decl'],
				    'conj' : item['Conj'],
				    'reg_adj_adv' : item['Reg Adj/Adv'] ,
				    'proper' : item['Proper'],
				    'part_of_speech' : item['Part Of Speech'] ,
			    	}
			    	 )
				except KeyError:
					print "Got a key error, likely picked wrong language"
					print "Current language is:", lang
					error =  {'lang_error' : lang}
					return str(error)
				index += 1
			print "Imported WordPropertyLatin"
		elif lang=='Greek':
			#questions is in model but doesn't seem to be in the spreadsheet
			#Anyways, just add this in if it needs to be 
			#'questions' : item['questions'],
			#Same for exclude_1_0 and notes
			for item in data_dict:
                                #print item, "item for greek"
				#try:
				WordPropertyGreek.objects.update_or_create(
				title = item['TITLE'],
				# id = item['id'],
				defaults={
				#'id' : item['id'],
				#'title' : item['TITLE'],
				# 'accented_lemma' : item['accented lemma'],
				'logeion_lemma' : item['LOGEION LEMMA'],
				'search_lemma' : item['SEARCH LEMMA'],
				'display_lemma' : item['DISPLAY LEMMA'],
				'english_definition' : item['SHORTDEF'],
				'logeion_def' : item['LOGEIONDEF'],
				'decl' : item['DECL'],
				'idiom' : item['IDIOM'],
				'reg_adj_adv' : item['REG ADJ/ADV'],
				'proper' : item['PROPER'],
				'part_of_speech' : item['PART-OF-SPEECH'],
				}
				)
				#except KeyError:
				#	print "Got a key error, likely picked wrong language"
				#	print "Current row is:",item
				#	print "Current language is:", lang
				#	error =  {'lang_error' : lang}
				#	return str(error)
				#print "Imported WordPropertyGreek"
