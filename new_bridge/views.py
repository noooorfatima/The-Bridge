
"""
eventually: see if I can do anything about intial load time, since it has been kind of slow since switching to autocompletes
"""
#from new_bridge.models import 'insert class/model names here'
from django.views import generic
import unicodedata
import new_bridge.models
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
#from django.urls import reverse
from django.core import serializers
from django.core import management
import json
#import pdb
from dal import autocomplete
from io import StringIO
import ast
from new_bridge import forms

models = new_bridge.models  #after switching to python3/django2.0, models wants to be explicitly referenced everytime we use it. this makes it easier. When next updating, see if you can remove it

class TextMetadataLookUp_latin(autocomplete.Select2ListView):

	#def create(self, text):
	#	return text

	def get_list(self):
		result_list = [model.name_for_humans for model in models.TextMetadata.objects.filter(language='latin')]
		result_list.sort()
		if self.q:
			data = models.TextMetadata.objects.all().filter(name_for_humans__icontains=self.q, language='latin')
			result_list = [model.name_for_humans for model in data]
			result_list.sort()
		return result_list

class TextMetadataLookUp_greek(autocomplete.Select2ListView):

	#def create(self, text):
	#	return text
	def get_list(self):
		result_list = [model.name_for_humans for model in models.TextMetadata.objects.filter(language='greek')]
		result_list.sort()
		if self.q:
			data = models.TextMetadata.objects.all().filter(name_for_humans__icontains=self.q, language='greek')
			result_list = [model.name_for_humans for model in data]
			result_list.sort()
		return result_list


def IndexView(request):

	latin_books_form = forms.TextMetadataAutoForm_latin()
	greek_books_form = forms.TextMetadataAutoForm_greek()
	subsection_data = {}
	for model in models.TextStructureGlossary.objects.all():
		s = model.subsection_level
		ns = ""
		for i in range(1, s+1):
			if i != s:
				ns = ns + str(1) + "."
			else:
				ns = ns + str(1)


		subsection_data[model.text_name] = ns
	name_for_humans_to_name_for_computers = {}
	for model in models.TextMetadata.objects.all():
		name_for_humans_to_name_for_computers[model.name_for_humans] = model.name_for_computers
	context = {"latin_books_form" : latin_books_form, "greek_books_form" : greek_books_form, "subsection_data" : subsection_data, "name_for_humans_to_name_for_computers" : name_for_humans_to_name_for_computers}
	#print("calling on index.html")
	return render(request,
	'index.html', context)

#^^^ pre-autocomplete index view
# Below code is modified from the GAM

def Tools(request):
	return render(request,'tools.html')
def Oracle(request):
	return render(request,'oracle.html')

def AboutView(request):
	return render(request,'newabout.html')


# This function takes all of the information submitted through the form and creates a unique url for that query
# this will allow the user to copy the url and come back to exactly the same place they were before
@require_http_methods(["POST"])
def words_page_redirect(request, language):
	print ("in words_page_redirect")
	#print(request.POST)
	#print(request.POST.get('section', ''))
	# Need to make sure all of the values are there, otherwise save as none
	#print(request.POST["readlist"], "readlist")
	text = "none"
	bookslist = []
	text_from = "start"
	text_to = "end"
	bookslist_string = ""
	from_sec = ""
	to_sec = ""
	add_remove = "Remove"
	# This makes sure it does not mess up the url
	if not request.POST["textlist"] == "":
		#print("in if")
		texts = request.POST.getlist("textlist")[0].split("$,")
		#I know, this looks messy, but html only has strings. html5 has lists, but they basically only work in chrome, and maybe firefox. At #least the texts are always seperated on commas, because it comes from a javascript array. However, it makes text names with commas in #them weird, so we now add $ to the end when we add things to textlist, just to make this split nice.
	#print text,"identifying text in conditional" # delete
	text_machine =[]
	reading_from = []
	reading_to = []
	add_remove = request.POST["add_remove_selector"]
	takencare_of_texts = set()
	for text in texts:
		text=text.replace("$", "")
		text= text.strip()
		print(text)
		if text in takencare_of_texts:
			pass
		else:
			takencare_of_texts.add(text)

			#print( "TEXT: ", text)
			text_from = []
			text_to = []
			text_from.extend(request.POST.getlist(text + " reading from") )
			text_to.extend(request.POST.getlist(text + " reading to"))
			if text_from == [] or text_to == []: #something went wrong with removing
				assert(False)
			if text_from == ['']:
				text_from = ["start"]
			if text_to ==['']:
				text_to =["end"]
			text_to.append("$")
			text_from.append("$")

			for i in range(len(text_from)):
				if not text_from[i]:
					text_from[i] = "start"
				#print(text_from, 'from 0')

			for i in range(len(text_to)):
				if not text_to[i]:
					text_to[i] = "start"
				#print(text_to, 'to 0')
			reading_from.extend(text_from)
			reading_to.extend(text_to)
			text_machine.append(models.TextMetadata.objects.get(name_for_humans=text).name_for_computers+"$")
	print(reading_from, reading_to, "reading_from, reading_to")
	if ('readlist' in request.POST): #get sections for things to include/exclude. the if carries over from an old way of doing things, and readlist will always be in the post request now, but it is a lot of indents to delete, vs just one if at the end.
		#print ('readlist in request.POST')
		#print( "about to make bookslist")
		bookslist = request.POST.getlist("readlist")
		#print(bookslist)
		if bookslist.count("$") == 1: #i.e, there is one book
			bookslist = bookslist[0].split("$")
		else:
			bookslist = bookslist[0].split("$,")
			bookslist[-1]= bookslist[-1][:-1]
		print(bookslist, "made bookslist")
		num_books = len(bookslist)
		#print( "num_books", num_books)
		loop_count = 0
		list_to_be_stringed = []
		read_seen = set()
		for i in bookslist:
			#print(i, "i")
			if i == "":
				break
			loop_count +=1
			if not (i in read_seen):
				try:
					from_secs = request.POST.getlist(i + " from")
					to_secs = request.POST.getlist(i + " to")
					#print(from_secs, 'from sex')
					#print(to_secs, 'to_sex')
					assert(len(to_secs) == len(from_secs))
				except Exception as e:
					print("ERROR: " + str(e))
					print("exception as e conditional triggered.")
					assert(False)

				for from_to in zip(from_secs, to_secs): #zip makes them a generator of tuples. I just set from_sec and to_sec because that was 	what we used when there was only one, and i did not want to rename all of them.
					#print("in that important for loop")
					from_sec = from_to[0]
					to_sec = from_to[1]
					if from_sec != '' and to_sec != "":
						#print("in case 1")
						add_to_booklist = i + "$_" + from_sec + "_" + to_sec + str("+")
						#print(add_to_booklist)
					elif from_sec != '' and to_sec == "":
						#print("in case 2")
						add_to_booklist = i + "$_" + from_sec + "_" + "end" + str("+")
						#print(add_to_booklist)
					elif from_sec == '' and to_sec != "":
						#print("in case 3")
						add_to_booklist = i + "$_" + "start" + "_" + to_sec + str("+")
						#print(add_to_booklist)
					elif from_sec == '' and to_sec == "":
						#print("in case 4")
						add_to_booklist = i + "$_" + "start" + "_" + "end" + str("+")
						#print(add_to_booklist)
					#print(add_to_booklist, "add to booklist")
					list_to_be_stringed.append(add_to_booklist)
				read_seen.add(i)
			else:
				pass



		bookslist_string = "".join(list_to_be_stringed)
		print(bookslist_string, 'bookslist_string')


		if bookslist_string == "":
			bookslist_string = "none"

		print (bookslist_string, "bookslist_string")
	if bookslist_string !="none":
		new_bookslist_string = []
		for book in bookslist_string.split('+'):
			if book == '': # this is only necessary if things with loop count break. We should only need one of them
				print("book is empty!")
				break
			try:
				marker = book.index('$')
			except ValueError:
				marker = len(book)
			book2=book[:marker]
			new_bookslist_string.append(models.TextMetadata.objects.get(name_for_humans=book2).name_for_computers+book[marker:])

		new_bookslist_string = "+".join(new_bookslist_string)
		#print(new_bookslist_string)
	else:
		new_bookslist_string = 'none'


	text_from = "_".join(reading_from)
	text_to = "_".join(reading_to)
	if text_from == "_":
		text_from = "start"
	if text_to == "_":
		text_to = "end"
	text_machine = "_".join(text_machine)
	#print(language, text_machine, new_bookslist_string, text_from, text_to, add_remove)
	url = '/words_page/'+language+'/'+text_machine+'/'+new_bookslist_string+'/'+text_from+'/'+text_to+'/'+add_remove+'/'
	return HttpResponseRedirect(url)


# We go here after the one above
def words_page(request, language, text, bookslist, text_from, text_to, add_remove):
	#change back to the human name because a bunch of stuff depends on it
	#if you try to change it to, add to the number of people who went down this rabit hole: 2
	#Note that it is ironic that the machine strictly uses the name_for_humans as opposed the the name_for_computers that was made for it
	print(text, "TEXT")
	#print(text_from, 'text_from')
	text = text[:-1]
	name_for_computers = []
	name_for_humans = []
	loc_def = []
	text = text.split("$_")
	#print(text, 'split text')
	for t in text:
		print(t, 't')
		name_for_computers.append(models.TextMetadata.objects.get(name_for_computers=t).name_for_computers)
		name_for_humans.append(models.TextMetadata.objects.get(name_for_computers=t).name_for_humans)
		loc_def.append(models.TextMetadata.objects.get(name_for_computers=t).local_def)
	name_for_computers = "$_".join(name_for_computers)
	name_for_humans = " and  ".join(name_for_humans)
	#print(name_for_humans)
	new_bookslist_string = []
	bookslist_comp = bookslist
	#print(bookslist, "original bookslist for words_page")
	if bookslist != 'none': #this just changes the booklist to use human names instead of machine names. Irony noted Dylan.
		for book in bookslist.split('+'):
			try:
				marker = book.index('$')
				#print(marker, 'marker')
			except:
				marker = len(book)
			book2=book[:marker]
			new_bookslist_string.append(models.TextMetadata.objects.get(name_for_computers=book2).name_for_humans+book[marker+1:])
			#print(new_bookslist_string, "new bookslist_string")
		bookslist = "+".join(new_bookslist_string)
		print(bookslist, 'new bookslist for words page')
	#print(bookslist, "bookslist")
	# Do some formatting to make vocab metadata more human-readable:
	add_remove_formatted = "excluding"
	if add_remove == "Add":
		add_remove_formatted = "also appearing in"
	#print(text_from, "text_from")
	if text_from == "" and text_to == "":
		text_from_formatted = "all"
		text_to_formatted = ""
	elif text_from.count("_") == 0:
		text_from_formatted = "from "+ text_from
		text_to_formatted = "to "+ text_to
	else:
		text_formating = name_for_humans.split(" and  ")
		#print(text_formating, "FORMATTING")
		formating_from = text_from.split("_$")
		#formating_from = [item.split("_") for item in formating_from if item !='']
		formating_to = text_to.split("_$")
		#formating_to = [item.split("_") for item in formating_to if item !='']
		formating_from = [item for item in formating_from if item !='']
		formating_to = [item for item in formating_to if item !='']
		#print(formating_from, "FORMATTING 1")
		triples = list(zip(text_formating, formating_from, formating_to))
		text_from_formatted = " "
		i =0
		for triple in triples:
			i += 1
			#print(triple)
			triple = list(triple) #tuples are immutable, and we are going to mutate this a lot
			triple[1] = triple[1].split("_")
			triple[2] = triple[2].split("_")
			triple[1] = [item for item in triple[1] if item !='']
			triple[2] = [item for item in triple[2] if item !='']
			#print(triple[1])
			#print(triple[2])
			if len(triple[1]) == 1: #if there is only one location for a text
				text_from_formatted = text_from_formatted + triple[0] + ": " + triple[1][0] + "-" + triple[2][0]
			else:
				count = 0
				print("in else")
				for item in list(zip(triple[1], triple[2])):
					print(item)
					if count == 0:
						text_from_formatted = text_from_formatted + triple[0] + ": " +  item[0] + "-" + item[1]
					else:
						text_from_formatted = text_from_formatted + " and " +  item[0] + "-" + item[1]
					count += 1

			if i != len(triples):
				text_from_formatted = text_from_formatted + "; "
			else:
				text_to_formatted = ""


	# Parse the user-selected books and their ranges, & format them for human:
	bookslist_formatted = "nothing"
	if bookslist != "none":
		temp_bookslist = bookslist.split("+")
		bookslist_formatted = ""
		for book in temp_bookslist:
			booksection = book.split('_')
			book = booksection[0]
			if len(booksection)==3:
				book += " from "+  booksection[1] + " to " + booksection[2]
			bookslist_formatted += book+ ", "
		bookslist_formatted = bookslist_formatted[:-2]

	loc_def = all(loc_def)

	try:
		return render(request,"words_page.html", {"language":language, "text":name_for_humans,
	"text_comp": name_for_computers,
	"bookslist_comp":bookslist_comp,
	"bookslist": bookslist, "bookslist_formatted": bookslist_formatted,
	"text_from": text_from, "text_from_formatted": text_from_formatted,
	"text_to": text_to, "text_to_formatted": text_to_formatted,
	"add_remove": add_remove, "add_remove_formatted": add_remove_formatted,"loc_def":loc_def})
	except Exception as e:
		print("WORDSPAGEERROR")
		print(e)

# Generates vocab list and returns as JSON string:
def get_words(request, language, text, bookslist, text_from,text_to, add_remove):
#change back to the human name because a bunch of stuff depenends on it
	#Note that it is ironic that the machine strictly uses the name_for_humans as opposed the the name_for_computers that was made for it
	#Also note that there was an issue with the fact and the apostrophe appearing in a title.
	#I think I switched to machine names in the spot the error was occuring, but I was considering switching it everywhere.
	# I still might do that because it will be REALLY inconvinient to switch once all of the data is uploaded.
	#leaving it for now, because the list of titles is just never going to be that big
	#To summerize: when this function is called, text = name_for_computers from words_page. However, many later things use name for humans (generateWords, loc_to_mindiv/loc_to_node, et c.)
	debuggingthingy = False
	if debuggingthingy:
		print( "\nAll paremeters for get words\n")
		print( request)
		print( language)
		print( text)
		print(text_from)
		print(text_to)
		print(bookslist)
		print( add_remove)
		print( '\n')

	new_text = []

	for t in text.split("$_"):
		new_text.append(models.TextMetadata.objects.get(name_for_computers=t).name_for_humans)
	#print(new_text, 'NEW TEXT')
	text_from = text_from.split("_$")
	text_to = text_to.split("_$")
	#print(text_from, "starts")
	#print(text_to, 'ends')
	text_list =[]
	for i in range(len(new_text)):

		if type(text_from[i]) == type("string"):
			if text_from[i][0] == '_':
				text_from[i] = text_from[i][1:]
			text_from[i] = text_from[i].split("_")

		if type(text_to[i]) == type("string"):
			if text_to[i][0] == '_':
				text_to[i] = text_to[i][1:]
			text_to[i] = text_to[i].split("_")
		book_with_many_sections = new_text[i][:] #[:] shallow copy
		for j in range(len(text_from[i])):
			text_list.append([book_with_many_sections, text_from[i][j], text_to[i][j]])
	print(text_list, "text_list")




	print(text_from, text_to)
	if bookslist != 'none':
		print (bookslist, "bookslist in if")
		new_bookslist_string = []
		bookslist_comp = bookslist
		#convert to human name
		for book in bookslist.split('+'):
			try:
				marker = book.index('$')
			except:
				marker = len(book)
			book2=book[:marker]
			new_bookslist_string.append(models.TextMetadata.objects.get(name_for_computers=book2).name_for_humans+book[marker+1:])
			#print(new_bookslist_string, "new_bookslist_string")
			bookslist = "+".join(new_bookslist_string)
	# Split read_texts into a list of lists of the form
	#[ [text_name, text_from, text_to], etc.]:
		bookslist = bookslist.split("+") #Split string
		for i in range(len(bookslist)): #Split each substring
			bookslist[i] = bookslist[i].split("_")
	else:
		bookslist = []

	# If no start/end loc was given, set to start/end of text:
	if text_from == 'none':
		text_from = 'start'

	if text_to == 'none':
		text_to = 'end'

	# Get words from database based on specified texts and ranges:
	word_ids = None
	word_property_table = None

	try:
	#print models.WordAppearencesLatin,language,text,text_from,text_to,bookslist,add_remove
		assert(type(bookslist) == type([]))
		if language == "latin":
			#pdb.set_trace()
		#print models.WordAppearencesLatin,language,text,text_from,text_to,bookslist,add_remove
			print(bookslist, "BOOKSLIST THAT GOES INTO GENERATE WORDS")
			word_ids = generateWords(models.WordAppearencesLatin, language, text_list, text_from, text_to, bookslist, add_remove)
			word_property_table = models.WordPropertyLatin
		#print("\nword_property_table for Latin: " + word_property_table)
		else:
			word_ids = generateWords(models.WordAppearencesGreek, language, text_list, text_from, text_to, bookslist, add_remove)
			word_property_table = models.WordPropertyGreek
		print("generated words")
	except Exception as e:
		print("get words error 0")
		print(e)

	# take word ids and find the correct data for these words in correct table (word table)
	words_list =[]
	try:
		#print "INSIDE TRY STATEMENT"

		print(len(word_ids), "getting word data for this many ids")
		[words_list.append(word_property_table.objects.get(id__exact=id)) for id in word_ids]
		print("got them!!")
		print(len(words_list))
		#print(words_list, 'here it is')
	#if accu1 < 5:
	   #print "debug: words_list add on " + accu1
	   #print words_list
	except Exception as e:
		print("get words error 1")
		print(e)
		assert(False)
	#appends mindivs to texts for useful_appearance_data
	for text in text_list:
		print(text)
		book = text[0]
		text_from = text[1]
		text_to = text[2]
		from_mindiv = loc_to_mindiv(book, text_from)
		to_mindiv = loc_to_mindiv(book, text_to)
		if True:
		#print("a text_to is the same as as text_from")
		#print(text_to)
			to_node = loc_to_node(book,text_to)
			child = to_node
		#working around python variable storage
			while not child.is_leaf():
			#print("NOT A LEAF")
				child = child.get_last_child()
				to_mindiv = child.least_mindiv
		text.extend([from_mindiv, to_mindiv])
	print(text_list)
		#print(to_mindiv, "new to")
	json_words = serializers.serialize("json", words_list)
	print(len(json_words))

	json_words2 = json.loads(json_words)
	test_for_in_final = {}
	print(len(json_words2))
	#I might make this a seperate function, just because it has had so many problems.
	#print len(json_words2), "length of json words before adding appearances"
	print('last step')
	final_keys = set()
	for text in text_list:
		for item in json_words2: #the final list is sent to words_page.html
			#print(final_keys)
			if True:
				from_mindiv = text[3]
				to_mindiv = text[4]
				if language != 'greek':
					#print(item['pk'])
					#item['pk'] = word ID
					word_app = models.WordAppearencesLatin.objects.filter(word=item['pk'],text_name=text[0])
					useful_appearance_data = models.WordAppearencesLatin.objects.filter(text_name=text[0], word=item['pk'], mindiv__range=(from_mindiv,  to_mindiv))
					#print(item)
					#print( len(word_app), "WORD APPEARENCE")
					#print(word_app.exists())
					#print( "^^^^^^^^^^^ that is a word_app")
				else:
					word_app = models.WordAppearencesGreek.objects.filter(word=item['pk'],text_name=text[0])
					useful_appearance_data = models.WordAppearencesGreek.objects.filter(text_name=text[0], word=item['pk'], mindiv__range=(from_mindiv,  to_mindiv))
				if word_app.exists(): #not guarrenteed that this word exists in both texts.
					total_count = len(word_app) #the total number of times the word appears in this text
					#print(len(useful_appearance_data))
					#print("Total count", total_count, word_app[0].word.title)
					#print('got total count')
					if len(useful_appearance_data) > 0:
						#print('word appears')
						item['fields']['count'] = len(useful_appearance_data)
						#print('set fields count')
						item['fields']['total_count'] = total_count
						#print('set fields total_count')
						item['fields']['source_text'] = str(text[0]) + ": " + "-".join(text[1:3])


						#print('set fields source_text')
						#print(useful_appearance_data)
						word_app = useful_appearance_data[0] # now word_app is the first appearance of the word in the user's subsection
						#print('reset word_app')
						item['fields']['position']=word_app.appearance

						if (word_app.local_def):
							item['fields']['local_def']= word_app.local_def
						else:
							item['fields']['local_def']= 'No Text-Specific Definition'


						test_for_in_final[item['pk']] = item
						final_keys.add(item['pk'])
					else:
						pass #this is a wierd case where the user has selected two texts, and a word appears in both texts over all, but not in either of the subsections they selected
						#print(word_app[0])
						#print(, 'this exists but not in either section')
				else:
					#print(item, 'MADE IT TO THE EXCPETION')
					pass #word appears in the selection, but not in this text

	json_words = json.dumps(list(test_for_in_final.values()))
	print('last return in views.py!')
	return HttpResponse(json_words, content_type="application/json")

def generateWords(word_appearences, lang, text, text_from, text_to, read_texts, add_remove):
	#Create a database filter for the texts+ranges in read_texts:
	print("GENERATE WORDS")
	print()
	print(text_from)
	print(text_to)
	print(lang)
	print(text)
	#print(read_texts)
	print(add_remove)

 # Get WordAppearence objects for words appearing in main texts:

	try:
		list_word_ids = words_in_read_texts(word_appearences, text)
		print("we got ", len(list_word_ids), " words")
	#loc_list = []
	#for vcab in vocab:
	#loc_list.append(vcab.mindiv)
	except Exception as e:
		print("try 2 error: ")
		print(e)
		assert(False)

	#if len(read_texts)==0:
	#	print (len(list_word_ids),"Word IDS without duplicates, about to return cause we made it through generate words and now we are free") #yes this was written while listening to the soundtrack of Gladiator
	#	return list(set(list_word_ids))
	try:
		# Get words which appear in main text and any of the read_texts:
		filtered_words= words_in_read_texts(word_appearences, read_texts)
		print(len(filtered_words), "length of read words")
		print(len(list_word_ids), 'words being studied')
		print(type(filtered_words), type(list_word_ids))
		vocab_intersection_ids = filtered_words & list_word_ids
	except Exception as e:
		print("try 3 error: ")
		print(e)


	# Remove or exclusively include words appearing in read_texts:
	#print vocab_intersection
	vocab_final = []
	#converting to a list may or may not be necessary, but it returned a list before. I think the javascript expects a list
	#if we avoid it though, we do not want to convert to a list unnecessarily.
	print(len(vocab_intersection_ids),"len of vocab_intersection")
	if add_remove == 'Add': # Add is a bit of a mis-nomer: all it is (and all we want it to be) is the intersection: the words in the new text that you have seen before.
		return list(vocab_intersection_ids)

	else: # If user wants words appearing ONLY in the main text(s)
		vocab_final = list_word_ids - vocab_intersection_ids
		print(len(vocab_final), "returning this many words")
		return list(vocab_final)

#THIS FUNCTION IS FAR MORE VERSITILE THAN IT SOUNDS, could be the basis of bridge giving you suggestions of what to read.
def words_in_read_texts(word_appearences, read_texts, has_mindivs=False): #read_texts just needs to a list of texts, not necessarially ones that have been read.
#has_mindivs lets read_texts be a list with [text, from_mindiv, to_mindiv]
	print("read_texts", read_texts)
	r = set()
	for text_range in read_texts: #text range is meant to be a list where [0] is the book title, [1] is the start, and [2] is the end.
		#print(text_range, 'text_range')
		book = text_range[0]
		if not has_mindivs:
			if len(text_range) > 1:
				start = text_range[1]
				end = text_range[2]
			else:
				start = "start"
				end = "end"
			print("vocaturus from_mindiv and to_mindiv with these inputs" , 'book=', book, 'start = ', start, 'end = ', end)
			from_mindiv = loc_to_mindiv(book, start)
			print(from_mindiv)
			to_mindiv = loc_to_mindiv(book, end)
			if True:
				print("Ooh corner case")
				to_node = loc_to_node(book,  end)
				child = to_node
				while not child.is_leaf():
					child = child.get_last_child()
					to_mindiv = child.least_mindiv
				print(to_mindiv)
		else:
			from_mindiv = text_range[1]
			to_mindiv = text_range[2]
		print("For read text, from, " , from_mindiv, "to, ",  to_mindiv)
				#print("For read text,  from,  to",  from_mindiv,  to_mindiv)
				#print("book",  book)
		print (text_range, 'text range')
		#was crashing when returning large requests, so I swithed from a list to a set. set membership checks are faster, and there will not be duplicates, which is important when we iterate over this later.
		new_vocab = word_appearences.objects.filter(text_name=book, mindiv__range=(from_mindiv, to_mindiv))
		list_of_dicts = new_vocab.values('word')
		print(len(list_of_dicts))
		ids = set()
		[ids.add(dict['word']) for dict in list_of_dicts] #adds all the word ids to the set 'ids'

		# this will get us words appearing in any of the texts. to make it only get words that appear in all texts, we want to take intersection (&) instead
		#we probably need to add another button like the include/exclude one, and make that pass along a boolean to be an input for this function
		#so this will be more like:
		#if any_all = any:
			#r = r|ids
		#else:
			#r = r&ids
		r = r|ids # this makes r the union of r and ids

		print(len(r), "len(r)")

	return r
'''
#Not fully implemented yet: will give users sections based on what they know
#needs a form that will have inputs for language, known texts, target_text, subsection size, and subsection_depth. the whole template for that needs to be written, but it should be able to be pretty similar to textlist.html (hopefully).
#also needs a url added to urls.py
#this is just the outline of the alogrithm, a lot still needs to be filled in.
def bridge_discover(request):

	lang = request.POST['lang']
	known_texts = request.POST.getlist('known_texts') #ideally texts will be submitted from this hypothetical form as [text, start, end], or they will be easy to get in this form.
	target_text = request.POST[target_text] # a single text
	size_of_section = request.POST[section_size] # how much the user wants to see
	subsection_depth = request.POST[subsection_depth]
	#somewhere disallow subsection depth greater than depth of text (ie, no depth 3 searches of the aenied)

	if lang == 'latin':
		word_appearences = models.WordAppearencesLatin.objects.all()
		word_property_table = models.WordPropertyLatin
	elif lang == 'greek': #all ifs should be re-written to this form at some point, so that adding new languages to views is a matter of adding another elif lang == lang, get info for lang
		word_appearences = models.WordAppearencesGreek.objects.all()
		word_property_table = models.WordPropertyGreek
	else:
		return render() # some template we don't have, "some error about how we don't have that language yet"

	known_words = words_in_read_texts(word_appearences, known_texts) #at this point known words should be a set of known word ids.
	#generate sections in target_text this should be a list of tuples of mindivs:
	while not node.is_leaf(): # Go to rightmost node until end of tree.
		#print node,node.least_mindiv
		node = node.get_last_child()
	end = node.least_mindiv - size of section #might be off by one, but this is the general idea
	sections_to_return =[]
	for i in range(end):
		section = [target_text, i, size_of_section + i]
		these_words= words_in_read_texts(word_appearences, section)
		try:
			diff = len(known_words - these_words)
		except Exception as e:
			print(e)
			print(len(known_words), 'this is how many known words their are')
			print(len(these_words),'this is how many these_words there are')
		sections_to_return.append(diff, these_words) #should add a new tuple in the form int(), set(), where each set is a set of word ids

	sections_to_return.sort() #do any other fancy thing that needs to be done to make it sort by the first item
		try:
			[id = (word_property_table.objects.get(id__exact=id)) diff_section[1] for in sections_to_return for id in diff_section[1]]
			#diff_section[1] = the set of word ids
			#id gets converted to a word_property object of the right language
			print("got the ids them!!")
		except Exception as e:
			print(e)
			assert(False)
	#probably needs to do some thing where it converted to json like wordspage.
	context ={"sections_to_return" : sections_to_return }
	return render(template, context)
'''






# Traverses the text's text structure tree to find the appropriate mindiv.
# location (str) must be a specific, bottom-level location in the text.
#   e.g., if text is structured chapter.verse, must specifiy chapter AND verse.
#   location can alternatively be "start" or "end".
# Returns the appropriate mindiv (integer).
def loc_to_mindiv(text,location):
	print(text, 'text in loc_to_mindiv')
	#print TextStructureNode.objects.filter(text_name=text)
	node = models.TextStructureNode.objects.get(text_name=text)
	#print node, "Nodles"
	if location == 'start':
		#print "location = start"
		return node.least_mindiv
		pass # don't change nodes!  Root.least_mindiv is start of text.
	elif location == 'end':
		while not node.is_leaf(): # Go to rightmost node until end of tree.
			#print node,node.least_mindiv
			node = node.get_last_child()
	else: # traverse tree according to given location.
		#print location,"location" #currently broken for things with one level of sectioning
		#print type(location),"location type"
		loc = location.split('.')
		#print text, 'text'
		#print loc,"loc"
		for subsection in loc:
			print(subsection,"subsection")
			node = node.get_children().get(subsection_id__exact=subsection)
			#print node, node.least_mindiv
	return node.least_mindiv

def loc_to_node(text,location):
	node = models.TextStructureNode.objects.get(text_name=text)
	if location == 'start':
		pass # don't change nodes!  Root.least_mindiv is start of text.
	elif location == 'end':
		while not node.is_leaf(): # Go to rightmost node until end of tree.
			node = node.get_last_child()
	else: # traverse tree according to given location.
		loc = location.split('.')
		for subsection in loc:
			node = node.get_children().get(subsection_id__exact=subsection)
	return node
#An admin page for importing updated spreadsheets
def myimport(request):
	query_results = models.TextStructureGlossary.objects.all()
	text_name_results = models.TextMetadata.objects.all()
	print(request.method)
	if request.method == 'POST':
		update_option = request.POST['update_option']
		lang = request.POST['select_lang']
		if update_option == "update_master":
			print(update_option)
			print("please be 1", len(request.FILES.getlist('datafile')))
			try:
				if len(request.FILES.getlist('datafile')) != 1:
					return render(request, 'admin/myimport.html',{'multi_file' : True, 'query_results' : query_results,'text_name_results' : text_name_results})
				the_file = request.FILES['datafile']
			except:
				return render(request, 'admin/myimport.html',{'failed' : True, 'query_results' : query_results,'text_name_results' : text_name_results})

			if the_file.content_type != 'text/csv':
				return render(request, 'admin/myimport.html',{'failed' : True, 'query_results' : query_results,'text_name_results' : text_name_results})
			fileName = the_file.name
			print(fileName)
			with open('temp_csv_for_importing.csv','wb') as f:
				f.write(the_file.read())
			#TODO add this line after June 28th, 2019
			# os.chown('temp_csv_for_importing.csv', 'www-data', 'www-data')
			#print('wrote the binary file')
			#this is capturing the output of management.call_command, which can only be a string
			out = StringIO()
			#print(out, 'haha printout')
			print('IN for call_command: ', 'update_master','temp_csv_for_importing.csv',lang, out)
			management.call_command('update_master','temp_csv_for_importing.csv',lang,stdout=out)
			error = out.getvalue().strip()
			if error:
				print(error, 'ERROR')
			if error != str():
				error = ast.literal_eval(error)
			if "lang_error" in error:
				return render(request, 'admin/myimport.html',{'query_results' : query_results,'lang_error' : True, 'title_bool': True, 'title_error': error['title_error'], 'text_name_results' : text_name_results })
			return render(request, 'admin/myimport.html',{"success" : True, 'query_results' : query_results, 'text_name_results' : text_name_results})

		elif update_option == "update_page":
			texts = request.FILES.getlist('datafile')
			if len(texts) == 0:
				return render(request, 'admin/myimport.html',{'failed' : True, 'query_results' : query_results,'text_name_results' : text_name_results})
			for fileName in texts:
				if fileName.content_type != 'text/csv':
					return render(request, 'admin/myimport.html',{'failed' : True, 'query_results' : query_results,'text_name_results' : text_name_results})
				with open('temp_csv_for_importing.csv','wb') as f:
					f.write(fileName.read())
			out = StringIO()
			management.call_command('update_page','temp_csv_for_importing.csv',lang,stdout=out)
			error = out.getvalue().strip()
			if error:
				print(error, "ERROR")
			if error != str():
				error = ast.literal_eval(error)
			if "lang_error" in error:
				return render(request, 'admin/myimport.html',{'query_results' : query_results,'lang_error' : True,'text_name_results' : text_name_results })
			if "name_error" in error:
				return render(request, 'admin/myimport.html',{'query_results' : query_results,'text_name_error' : True, 'text_name' : error['name_error'],'text_name_results' : text_name_results })
			if "dots_error" in error:
				return render(request, 'admin/myimport.html',{'query_results' : query_results,'dots_error' : True, 'location' : error['dots_error'],'text_name_results' : text_name_results })
			if "structure_error" in error:
				return render(request, 'admin/myimport.html',{'query_results' : query_results,'structure_error' : True, 'location' : error['structure_error'],'text_name_results' : text_name_results })
			if "local_def_error" in error:
				return render(request, 'admin/myimport.html',{'query_results' : query_results,'local_def_error' : True, 'location' : error['local_def_error'],'text_name_results' : text_name_results })

			print("Successfully updated page!")

			print("Now cleaning up all TextStructureNodes") #If there are two text structures for a text, removes all the older ones (not just for this updated text)
			management.call_command('sqlite_delete',"TextStructureNodeCLEAN")
			error = out.getvalue().strip()
			print(error, "ERROR")
			if error != str():
				error = ast.literal_eval(error)
			print(lang)
			#print("cleaned, now updating corpus_rank")
			#management.call_command('update_corpusrank', lang)
			return render(request, 'admin/myimport.html',{"success" : True, 'query_results' : query_results,'text_name_results' : text_name_results})
	else:
		return render(request, 'admin/myimport.html', {'query_results' : query_results,'text_name_results' : text_name_results})

def handler404(request):
	response = render('404.html', {}, context_instance=RequestContext(request))
	response.status_code = 404
	return response
