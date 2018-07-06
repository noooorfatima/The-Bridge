
"""
TODO:
Make "What are you reading" and "Include/exclude" the same. √
This will allow users the option to read multiple texts, and make input for dijoint subsections more user friendly.
Make input be through autocomplete fields. √
Once "selection" is chosen, give a prompt for the subsections based on the text's subsectioning. It is fine for gallic wars, not so fine for poems, text books, or lists.
Fix importer
Fix/update autoLemma.py
Redo slideout panel filters to allow total #apps, apps in section, and corpus_rank side by side. (sort of done, needs better styling)


"""
#from new_bridge.models import 'insert class/model names here'
from django.views import generic
import unicodedata
import new_bridge.models
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
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


	def create(self, text):
		return text

	def get_list(self):
		result_list = [model.name_for_humans for model in models.TextMetadata.objects.filter(language='latin')]
		if self.q:
			data = models.TextMetadata.objects.all().filter(name_for_humans__icontains=self.q, language='latin')
			result_list = [model.name_for_humans for model in data]
		return result_list

class TextMetadataLookUp_greek(autocomplete.Select2ListView):


	def create(self, text):
		return text

	def get_list(self):
		result_list = [model.name_for_humans for model in models.TextMetadata.objects.filter(language='greek')]
		if self.q:
			data = models.TextMetadata.objects.all().filter(name_for_humans__icontains=self.q, language='greek')
			result_list = [model.name_for_humans for model in data]
		return result_list


def IndexView(request):

	latin_books_form = forms.TextMetadataAutoForm_latin()
	print(latin_books_form)
	greek_books_form = forms.TextMetadataAutoForm_greek()
	context = {"latin_books_form" : latin_books_form, "greek_books_form" : greek_books_form}
	#print("calling on index.html")
	return render(request,
	'index.html', context)

#^^^ pre-autocomplete index view
# Below code is modified from the GAM




def AboutView(request):
	return render(request,'newabout.html')

#class HelpView(generic.ListView):
#	template_name = 'help.html'
#	model = BookTable

#class ContactView(generic.ListView):
#	template_name = 'contact.html'
#	model = BookTable

# This function takes all of the information submitted through the form and creates a unique url for that query
# this will allow the user to copy the url and come back to exactly the same place they were before
@require_http_methods(["POST"])
def words_page_redirect(request, language):
	print ("in words_page_redirect")
	print(request.POST)
	#print(request.POST.get('section', ''))
	# Need to make sure all of the values are there, otherwise save as none
	print(request.POST["readlist"])
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
		if text in takencare_of_texts:
			break
		else:
			takencare_of_texts.add(text)
		print( "TEXT: ", text)
		text=text.replace("$", "")
		text_from = request.POST.getlist(text + " from")
		text_to = request.POST.getlist(text + " to")
		if text_from == []:
			text_from = [""]
		if text_to ==[]:
			text_to =[""]
		print(text_from, 'from 0')

		if text_from == ['']:
			text_from = ['start']
		print(text_to, 'to 0')

		if text_to == ['']:
			text_to = ["end"]

		reading_from.extend(text_from)
		reading_to.extend(text_to)
		text_meta = models.TextMetadata.objects.get(name_for_humans=text)
		text_machine.append(text_meta.name_for_computers)
	print(reading_from, reading_to, "reading_from, reading_to")
	if ('readlist' in request.POST): #get sections for things to include/exclude. the if carries over from an old way of doing things, and readlist will always be in the post request now, but it is a lot of indents to delete, vs just one if at the end.
		print ('readlist in request.POST')
		print( "about to make bookslist")
		bookslist = request.POST.getlist("readlist")

		bookslist = bookslist[0].split(",")
		print(bookslist, "made bookslist")
		num_books = len(bookslist)
		#print( "num_books", num_books)
		loop_count = 0
		for i in bookslist:
			#print(i, "i")
			loop_count +=1

			try:
				#print(request.POST.getlist(i + " from"), "from")
				#print(request.POST.getlist(i + " to"), "to")
				#print(request.POST.getlist(i), "maybe the rest of from???")
				from_secs = request.POST.getlist(i + " from")
				to_secs = request.POST.getlist(i + " to")
				print(from_secs, 'from sex')
				print(to_secs, 'to_sex')
				assert(len(to_secs) == len(from_secs))
			except Exception as e:
				print("ERROR: " + str(e))
				print("exception as e conditional triggered.")
				assert(False)
			list_to_be_stringed = []
			for from_to in zip(from_secs, to_secs): #zip makes them a generator of tuples. I just set from_sec and to_sec because that was what we used when there was only one, and i did not want to rename all of them.
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

				list_to_be_stringed.append(add_to_booklist)

			bookslist_string = "".join(list_to_be_stringed)
			print(bookslist_string)
			if not bookslist_string: # "" is falsey
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
	text_machine = "_".join(text_machine)
	print(language, text_machine, new_bookslist_string, text_from, text_to, add_remove)
	url = '/words_page/'+language+'/'+text_machine+'/'+new_bookslist_string+'/'+text_from+'/'+text_to+'/'+add_remove+'/'
	return HttpResponseRedirect(url)


# We go here after the one above
def words_page(request, language, text, bookslist, text_from, text_to, add_remove):
	#change back to the human name because a bunch of stuff depends on it
	#if you try to change it to, add to the number of people who went down this rabit hole: 2
	#Note that it is ironic that the machine strictly uses the name_for_humans as opposed the the name_for_computers that was made for it
	text_meta = models.TextMetadata.objects.get(name_for_computers=text)
	text = text_meta.name_for_humans
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
	#print(bookslist, "bookslist")
	# Do some formatting to make vocab metadata more human-readable:
	add_remove_formatted = "excluding"
	if add_remove == "Add":
		add_remove_formatted = "also appearing in"
	print(text_from, "text_from")
	if text_from == "" and text_to == "":
		text_from_formatted = "all"
		text_to_formatted = ""
	elif text_from.count("_") == 0:
		text_from_formatted = "from "+ text_from
		text_to_formatted = "to "+ text_to
	else:
		formating_from = text_from.split("_")
		formating_to = text_to.split("_")
		pairs = list(zip(formating_from, formating_to))
		text_from_formatted = " "
		for pair in pairs:
			text_from_formatted = text_from_formatted + " from "+ pair[0] + " to " + pair[1]
			if pair != pairs[-1]: #this format can be rather humorously be broken by including terms multiple times... but it does not affect the words displayed.
				text_from_formatted = text_from_formatted + " and "
			else:
				text_to_formatted = " "

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

	loc_def =  models.TextMetadata.objects.get(name_for_humans=text).local_def
	try:
		return render(request,"words_page.html", {"language":language, "text":text,
	"text_comp":text_meta.name_for_computers,
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
	debuggingthingy = True
	if debuggingthingy:
		print( "\nAll paremeters for get words\n")
		print( request)
		print( language)
		print( text)
		print(bookslist)
		print( add_remove)
		print( '\n')

	text_meta = models.TextMetadata.objects.get(name_for_computers=text)
	text = text_meta.name_for_humans
	if bookslist != 'none':
		print (bookslist, "bookslist in if")
		new_bookslist_string = []
		bookslist_comp = bookslist
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
			#print(bookslist, "BOOKSLIST THAT GOES INTO GENERATE WORDS")
			word_ids = generateWords(models.WordAppearencesLatin, language, text, text_from, text_to, bookslist, add_remove)
			word_property_table = models.WordPropertyLatin
		#print("\nword_property_table for Latin: " + word_property_table)
		else:
			word_ids = generateWords(models.WordAppearencesGreek, language, text,
			text_from, text_to, bookslist, add_remove)
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
		[words_list.append(word_property_table.objects.filter(id__exact=id)[0]) for id in word_ids]
		print("got them!!")
		#print(words_list, 'here it is')
	#if accu1 < 5:
	   #print "debug: words_list add on " + accu1
	   #print words_list
	except Exception as e:
		print("get words error 1")
		print(e)
		assert(False)
	from_mindivs = []
	to_mindivs = []




	text_from = text_from.split("_")
	text_to = text_to.split("_")
	print(text_from)
	print(text_to)
	for each in zip(text_from, text_to):
		print (each)
		if each[0] != "_" or each[1] != "_": #making sure we are only using locations
			text_from = each[0]
			text_to = each[1]
			from_mindivs.append(loc_to_mindiv(text, text_from)) #THIS LINE IS WHY THIS AND THE VERY SIMILAR CODE ABOVE CANNOT BE ONE FUNCTION
			to_mindiv = loc_to_mindiv(text, text_to) #while seems like it would be nicer to have this in an else, sometimes even when the if triggers the while loop does not, and then to_mindiv is undefined.
			if text_from == text_to:
				print("a text_to is the same as as text_from")
				to_node = loc_to_node(text,text_to)
				child = to_node
				#working around python variable storage
				while not child.is_leaf():
					print("NOT A LEAF")
					child = child.get_last_child()
					to_mindiv = child.least_mindiv
				print(to_mindiv, "new to")
			to_mindivs.append(to_mindiv) #we need these to get the number of times a word appears in the user's selection

	mindivs = list(zip(from_mindivs, to_mindivs))
	print (mindivs, "mindivs")

	json_words = serializers.serialize("json", words_list)
	#D#print type(json_words)
	json_words2 = json.loads(json_words)
	test_for_in_final = {}
	#I might make this a seperate function, just because it has had so many problems.
	#print len(json_words2), "length of json words before adding appearances"
	print('last step')
	final_keys = set()
	for item in json_words2: #the final list is sent to words_page.html
		if item['pk'] not in final_keys:
			if language != 'greek':
				#print(item['pk'])
				word_app = models.WordAppearencesLatin.objects.filter(word=item['pk'],text_name=text)
				#print( word_app, "WORD APPEARENCE")
				#print( "^^^^^^^^^^^ that is a word_app")
			else:
				word_app = models.WordAppearencesGreek.objects.filter(word=item['pk'],text_name=text)
			#print(from_mindiv, "from mindiv")
			#print(to_mindiv , "to_mindv")
			total_count = len(word_app) #the total number of times the word appears in this text
			#print("Total count", total_count, word_app[0].word.title)
			#print('got total count')
			#try: #this takes a long time, so if the user is studying the whole text, we don't want to do it
			if len(mindivs) >= 1: #ie, we have some mindivs
				useful_appearance_data = []
				for word_apperance in word_app:
					#print("in top loop")
					for each in mindivs:
						from_mindiv = each[0]
						to_mindiv = each[1]

						if from_mindiv <= word_apperance.mindiv <= to_mindiv: #this is all the times the word appears in the selection
							#print("adding word app")
							useful_appearance_data.append(word_apperance)
				if useful_appearance_data == []:
					print (word_app[0].word_id, "OFFENDING WORD_ID")
					print(mindivs, "MINDIV RANGE")
					print("ERROR: that word id (number two above this) does not appear in any of the ranges (directly above this)")
					assert(False)

			#except:
				#print("just start to end")
				#useful_appearance_data = [word_app] #still need to define it because we call it later
				#pass

			#in the user selection. The length is  how many times the word appears in the section, and the first item is the first appearance of the word in  the section
			#print (len(useful_appearance_data), 'all appearances in section')

			item['fields']['count'] = len(useful_appearance_data)
			item['fields']['total_count'] = total_count
			#print(useful_appearance_data)
			word_app = useful_appearance_data[0] # now word_app is the first appearance of the word in the user's subsection
			item['fields']['position']=word_app.appearance
			if (word_app.local_def) and word_app.local_def !="":
				item['fields']['local_def']=word_app.local_def
			else:
				item['fields']['local_def']="None"
			test_for_in_final[item['pk']] = item
			final_keys.add(item['pk'])

	#make the appearance list sorted and then just take the first one
	json_words = json.dumps(list(test_for_in_final.values()))

	#I do not know why it gets so big at this time
	#It's ok, json_words just has all of the information about the word.
	print('last return in views.py!')
	return HttpResponse(json_words, content_type="application/json")

def generateWords(word_appearences, lang, text, text_from, text_to, read_texts, add_remove):
	#Create a database filter for the texts+ranges in read_texts:
	print(text_from)
	print(text_to)
	print(lang)
	print(text)
	print(read_texts)
	print(add_remove)
 # Get WordAppearence objects for words appearing in main text:
	try:
		vocab = word_appearences.objects.none() #creates an empty django queryset.
		text_from = text_from.split("_")
		text_to = text_to.split("_")
		for each in zip(text_from, text_to):
			text_from = each[0]
			text_to = each[1]
			from_mindiv = loc_to_mindiv(text, text_from)
			to_mindiv = loc_to_mindiv(text, text_to)
			print("find me", text_from, text_to)
			print(from_mindiv, to_mindiv)
			print("HEY THIS IS THE RANGE OF MINDIVS WE NEED TO CARE ABOUT")
			if text_from == text_to:
				to_node = loc_to_node(text,text_to)
				child = to_node
				#working around python variable storage
				while not child.is_leaf():
					child = child.get_last_child()
					to_mindiv = child.least_mindiv
				print( from_mindiv,to_mindiv)
			vocab= vocab.union(word_appearences.objects.filter(text_name__exact=text, mindiv__range=(from_mindiv, to_mindiv)))

		print("we got ", len(vocab), " words")
	#loc_list = []
	#for vcab in vocab:
	#loc_list.append(vcab.mindiv)
	except Exception as e:
		print("try 2 error: ")
		print(e)

	print("about to make the list of word ids")
	# makes a set of the id numbers
	list_of_dicts= vocab.values('word')

	list_word_ids = set()
	for dict in list_of_dicts:
		list_word_ids.add(dict['word'])

	if len(read_texts)==0:
		print (len(list_word_ids),"Word IDS without duplicates, about to return cause we made it through generate words and now we are free") #yes this was written while listening to the soundtrack of Gladiator
		return list(set(list_word_ids))
	else:
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
	if len(read_texts) > 0:
		if add_remove == 'Add': # Add is a bit of a mis-nomer: all it is (and all we want it to be) is the intersection: the words in the new text that you have seen before.
			return list(vocab_intersection_ids)

		else: # If user wants words appearing ONLY in the main text
			vocab_final = list_word_ids - vocab_intersection_ids
			print(len(vocab_final), "returning this many words")
			return list(vocab_final)
	else:
	# don't need to modify list; nothing to add/remove
		return list(vocab_intersection_ids)

#THIS FUNCTION IS FAR MORE VERSITILE THAN IT SOUNDS, could be the basis of bridge giving you suggestions of what to read.
def words_in_read_texts(word_appearences, read_texts): #read_texts just needs to a list of texts, not necessarially ones that have been read.
	#print("read_texts", read_texts)
	r = set()
	for text_range in read_texts: #text range is meant to be a list where [0] is the book title, [1] is the start, and [2] is the end.
		#print(text_range, 'text_range')
		book = text_range[0]
		if len(text_range) > 1:
			start = text_range[1]
			end = text_range[2]
		else:
			start = "start"
			end = "end"
		print("vocaturus from_mindiv and to_mindiv with these inputs" , 'book=', book, 'start = ', start, 'end = ', end)
		from_mindiv = loc_to_mindiv(book, start)
		to_mindiv = loc_to_mindiv(book, end)
		print("For read text, from, " , from_mindiv, "to, ",  to_mindiv)
		if start == end:
			print("Ooh corner case")
			to_node = loc_to_node(book,  end)
			child = to_node
			while not child.is_leaf():
				child = child.get_last_child()
				to_mindiv = child.least_mindiv
		#print("For read text,  from,  to",  from_mindiv,  to_mindiv)
		#print("book",  book)
		print (text_range, 'text range')
		#was crashing when returning large requests, so I swithed from a list to a set. set membership checks are faster, and there will not be duplicates, which is important when we iterate over this later.
		new_vocab = word_appearences.objects.filter(text_name=book, mindiv__range=(from_mindiv, to_mindiv))
		list_of_dicts = new_vocab.values('word')
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


# Traverses the text's text structure tree to find the appropriate mindiv.
# location (str) must be a specific, bottom-level location in the text.
#   e.g., if text is structured chapter.verse, must specifiy chapter AND verse.
#   location can alternatively be "start" or "end".
# Returns the appropriate mindiv (integer).
def loc_to_mindiv(text,location):
	#print text
	#print TextStructureNode.objects.filter(text_name=text)
	node = models.TextStructureNode.objects.filter(text_name=text)[0]
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
	node = models.TextStructureNode.objects.filter(text_name=text)[0]
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



def admin(request):
	return render(request,'admin.html')

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
		#print('wrote the binary file')
		#this is capturing the output of management.call_command, which can only be a string
		out = StringIO()
		#print(out, 'haha printout')
	#print('IN for call_command: ', 'update_master','temp_csv_for_importing.csv',lang, stdout=out)
		management.call_command('update_master','temp_csv_for_importing.csv',lang,stdout=out)
		error = out.getvalue().strip()
		print(error)
		if error != str():
			error = ast.literal_eval(error)
	#text_name_error no longer relevant
		if "text_name_error" in error:
			return render(request, 'admin/myimport.html',{'query_results' : query_results,'text_name_error' : True, 'text_name' : error['text_name_error'],'text_name_results' : text_name_results })
		elif "lang_error" in error:
			return render(request, 'admin/myimport.html',{'query_results' : query_results,'lang_error' : True,'text_name_results' : text_name_results })
		return render(request, 'admin/myimport.html',{"success" : True, 'query_results' : query_results,'text_name_results' : text_name_results})
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
		print("Successfully updated page!")
		print("Now cleaning up all TextStructureNodes") #If there are two text structures for a text, removes all the older ones (not just for this updated text)
		management.call_command('sqlite_delete',"TextStructureNodeCLEAN")
		error = out.getvalue().strip()
		print(error)
		if error != str():
			error = ast.literal_eval(error)
		if "text_name_error" in error:
			return render(request, 'admin/myimport.html',{'query_results' : query_results,'text_name_error' : True, 'text_name' : error['text_name_error'],'text_name_results' : text_name_results })
		elif "lang_error" in error:
			return render(request, 'admin/myimport.html',{'query_results' : query_results,'lang_error' : True,'text_name_results' : text_name_results })
		return render(request, 'admin/myimport.html',{"success" : True, 'query_results' : query_results,'text_name_results' : text_name_results})
	else:
		return render(request, 'admin/myimport.html', {'query_results' : query_results,'text_name_results' : text_name_results})

def handler404(request):
	response = render('404.html', {}, context_instance=RequestContext(request))
	response.status_code = 404
	return response
