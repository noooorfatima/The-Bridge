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
from io import StringIO
import ast
models = new_bridge.models  #after switching to python 3, models wants to be explicitly referenced everytime we use it. this makes it easier.
def IndexView(request):
	sorted_latin_books=sorted(models.BookTitles.objects.all(),key=lambda book: (book.book_type,book.title_of_book))

	booklist_latin= [(book.title_of_book, book.book_type) for book in sorted_latin_books]

	sorted_greek_books=sorted(models.BookTitlesGreek.objects.all(),key=lambda book: (book.book_type,book.title_of_book))

	booklist_greek= [(book.title_of_book, book.book_type) for book in sorted_greek_books]
	booklist_latin_TE = []
	booklist_latin_TK = []
	booklist_latin_LI = []
	booklist_greek_TE = []
	booklist_greek_TK = []
	booklist_greek_LI = []
	for book in sorted_latin_books:
		if (book.book_type == "TE"):
			booklist_latin_TE.append(book.title_of_book)
		elif (book.book_type == "TK"):
			booklist_latin_TK.append(book.title_of_book)
		elif (book.book_type == "LI"):
			booklist_latin_LI.append(book.title_of_book)
	for book in sorted_greek_books:
		if (book.book_type == "TE"):
			booklist_greek_TE.append(book.title_of_book)
		elif (book.book_type == "TK"):
			booklist_greek_TK.append(book.title_of_book)
		elif (book.book_type == "LI"):
			booklist_greek_LI.append(book.title_of_book)
	print("calling on index.html")
	return render(request,
	'index.html',{"booklist_latin":booklist_latin,"booklist_greek":booklist_greek,"booklist_latin_TE":booklist_latin_TE,"booklist_latin_TK":booklist_latin_TK,"booklist_latin_LI":booklist_latin_LI,"booklist_greek_TE":booklist_greek_TE,"booklist_greek_TK":booklist_greek_TK,"booklist_greek_LI":booklist_greek_LI})

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
	print(request.POST, "request.POST")
	print(request.GET, 'request.GET')
	print(request.POST.get('section', ''))
	# Need to make sure all of the values are there, otherwise save as none
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
		print("in if")
		text = request.POST["textlist"]
	#print text,"identifying text in conditional" # delete
	print( "TEXT: ", text)
	text_from = request.POST["text_from"]
	text_to = request.POST["text_to"]
	add_remove = request.POST["add_remove_selector"]
	if text_to == '':
		text_to = 'end'
		text_from = 'start'

	text_meta = models.TextMetadata.objects.get(name_for_humans=text)
	text_machine = text_meta.name_for_computers
	if ('book' in request.POST):
		print ('boon in request.POST')
		print( "about to make bookslist")
		bookslist = request.POST.getlist("book")
		print(bookslist, "made bookslist")
		#assert(False)
		#bookslist = list_of_lists(bookslist)
		num_books = len(bookslist)
		print( "num_books", num_books)
		loop_count = 0
		for i in bookslist:
			print(i, "i")
			loop_count +=1

			try:
				print(request.POST.getlist(i + " from"), "from")
				print(request.POST.getlist(i + " to"), "to")
				print(request.POST.getlist(i), "maybe the rest of from???")
				from_secs = request.POST.getlist(i + " from")
				to_secs = request.POST.getlist(i + " to")
				print(from_secs, 'from sex')
				print(to_secs, 'to_sex')
				assert(len(to_secs) == len(from_secs))
			except Exception as e:
				print("ERROR: " + str(e))
				print("exception as e conditional triggered.")
				assert(False)
				
			for from_to in zip(from_secs, to_secs):
				from_sec = from_to[0]
				to_sec = from_to[1]
				if from_sec != '' and to_sec != "":
					print("in case 1")
					add_to_booklist = i + "$_" + from_sec + "_" + to_sec
					print(add_to_booklist)
				elif from_sec != '' and to_sec == "":
					print("in case 2")
					add_to_booklist = i + "$_" + from_sec + "_" + "end"
					print(add_to_booklist)
				elif from_sec == '' and to_sec != "":
					print("in case 3")
					add_to_booklist = i + "$_" + "start" + "_" + to_sec
					print(add_to_booklist)
				elif from_sec == '' and to_sec == "":
					print("in case 4")
					add_to_booklist = i + "$_" + "start" + "_" + "end"
					print(add_to_booklist)

				add_to_booklist = add_to_booklist + str("+")
				bookslist_string = bookslist_string + add_to_booklist #but we always need to add to the bookslist string
			print(bookslist_string, "bookslist_string")

	else:
		bookslist_string = "none"
	#print request.POST["textlist"]

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
		print(new_bookslist_string)
	else:
		new_bookslist_string = 'none'
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
	print(bookslist, "original bookslist for words_page")
	if bookslist != 'none': #this just changes the booklist to use human names instead of machine names. Irony noted Dylan.
		for book in bookslist.split('+'):
			try:
				marker = book.index('$')
				print(marker, 'marker')
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

	if text_from == "start" and text_to == "end":
		text_from_formatted = "all"
		text_to_formatted = ""
	else:
		text_from_formatted = "from "+text_from
		text_to_formatted = "to "+text_to

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
			print(new_bookslist_string, "new_bookslist_string")
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
			word_ids = generateWords(models.WordAppearencesLatin, language, text, text_from, text_to, bookslist, add_remove)
			word_property_table = models.WordPropertyLatin
		#print("\nword_property_table for Latin: " + word_property_table)
		else:
			word_ids = generateWords(models.WordAppearencesGreek, language, text,
			text_from, text_to,bookslist, add_remove)
			word_property_table = models.WordPropertyGreek
	except Exception as e:
		print("get words error 0")
		print(e)

	# take word ids and find the correct data for these words in correct table (word table)
	words_list = []
	#print "length of word ids: " + str(len(word_ids))
	#print type(word_ids)
	#accu1=0
	#print "NEW PRINT STATEMENT"
	#accu1
	try:
		#print "INSIDE TRY STATEMENT"
		for each in word_ids:
	#accu1+=1
	#print "WORD LOOP", accu1
		#if language == "latin":
			#count = models.WordAppearencesLatin.objects.filter(word__exact=each).count()
		#else:
			#count = models.WordAppearencesGreek.objects.filter(word__exact=each).count()
			#print "DEBUG IS THIS CAUSING PROBLEMS"
			#word = word_property_table.objects.filter(id__exact=each)[0]
			#word.corpus_rank = 9617 - count
			#word.save()
			words_list.append(word_property_table.objects.filter(id__exact=each)[0])
	#if accu1 < 5:
	   #print "debug: words_list add on " + accu1
	   #print words_list
	except Exception as e:
		print("get words error 1")
		print(e)
	from_mindiv = loc_to_mindiv(text,text_from)
	to_mindiv = loc_to_mindiv(text,text_to) #we need these to get the number of times a word appears in the user's selection

	json_words = serializers.serialize("json",words_list)
	#D#print type(json_words)
	json_words2 = json.loads(json_words)
	final_list = []
	test_for_in_final = {}
	#I might make this a seperate function, just because it has had so many problems.
	#print len(json_words2), "length of json words before adding appearances"
	for item in json_words2: #the final list is sent to words_page.html
	#print(item, "item")
		if item['pk'] not in list(test_for_in_final.keys()):
			if language != 'greek':
				word_app = models.WordAppearencesLatin.objects.filter(word=item['pk'],text_name=text)
	#print (word_app.local_def, "here is the word_apps local def")
	#print( word_app, "WORD APPEARENCE")
	#print "^^^^^^^^^^^ that is a word_app"
			else:
				print("looking at a greek word appearence")
				word_app = models.WordAppearencesGreek.objects.filter(word=item['pk'],text_name=text)
			#print(from_mindiv, "from mindiv")
			#print(to_mindiv , "to_mindv")
			total_count = len(word_app) #the total number of times the word appears in this text
			#print("Total count", total_count, word_app[0].word.title)
			useful_appearance_data = [word_apperance for word_apperance in word_app if from_mindiv <= word_apperance.mindiv <= to_mindiv] #this is all the times the word appears
			#in thet user selection. The length is  how many times the word appears in the section, and the first item is the first appearance of the word in  the section
			#print (useful_appearance_data, 'all appearances')

			item['fields']['count'] = len(useful_appearance_data)
			item['fields']['total_count'] = total_count
			word_app = useful_appearance_data[0] # now word_app is the first appearance of the word in the user's subsection
			item['fields']['position']=word_app.appearance
			if (word_app.local_def) and word_app.local_def !="":
				item['fields']['local_def']=word_app.local_def
			else:
				item['fields']['local_def']="None"
			test_for_in_final[item['pk']] = item

	#make the appearance list sorted and then just take the first one
	json_words = json.dumps(list(test_for_in_final.values()))

	#I do not know why it gets so big at this time
	#It's ok, json_words just has all of the information about the word.
	print(len(json_words),"length aftering adding appearances")
	return HttpResponse(json_words, content_type="application/json")

def generateWords(word_appearences, lang, text, text_from, text_to, read_texts, add_remove):
	#Create a database filter for the texts+ranges in read_texts:
	#print(text_from)
	#print(text_to)
	#print(lang)
	#print(text)
	#print(read_texts)
	#print(add_remove)
 # Get WordAppearence objects for words appearing in main text:
	try:
		from_mindiv = loc_to_mindiv(text,text_from)
		to_mindiv = loc_to_mindiv(text,text_to)
		#print("find me", text_from, text_to)
		print(from_mindiv,to_mindiv)
		print("HEY THIS IS THE RANGE OF MINDIVS WE NEED TO CARE ABOUT")
		if text_from == text_to:
			to_node = loc_to_node(text,text_to)
			child = to_node
			#working around python variable storage
			while not child.is_leaf():
				child = child.get_last_child()
			to_mindiv = child.least_mindiv
			print( from_mindiv,to_mindiv)
		vocab = word_appearences.objects.filter(text_name__exact=text, mindiv__range=(from_mindiv, to_mindiv))
	#print len(vocab), "words"
	#loc_list = []
	#for vcab in vocab:
	#loc_list.append(vcab.mindiv)
	except Exception as e:
		print("try 2 error: ")
		print(e)

	# makes a list of dictionaries that contain the id num of all of the words in vocab variable
	# looks like: [{'word': 1001}, {'word': 2030'}, ...} etc.


	list_of_dict_of_words = vocab.values('word')
	#print len(list_of_dict_of_words), 'list_of_dict_of_words'
	# makes a list of these id numbers
	list_word_ids = []
	for each in list_of_dict_of_words:
		list_word_ids.append(each['word'])
	print(len(list_word_ids))

	if len(read_texts)==0:
		print (len(list(set(list_word_ids))),"Word IDS without duplicates, about to return cause we made it through generate words and now we are free") #yes this was written while listening to the soundtrack of Gladiator
		return list(set(list_word_ids))
	else:
		try:
			# Get words which appear in main text and any of the read_texts:
			list_word_ids=list(set(list_word_ids))
			vocab_intersection =[]
			vocab_non_intersection =[]
			filtered_words= words_in_read_texts(word_appearences, read_texts)
			print(len(filtered_words), "length of read words")
			print(len(list_word_ids), 'words being studied')
			for item in filtered_words:
			# item.word.id might need to change
			# Make it whatever it needs to be to get the id that corresponds to the word
				if item.word.id in list_word_ids:
					vocab_intersection.append(item.word)
			print(len(vocab_intersection))
		except Exception as e:
			print("try 3 error: ")
			print(e)
			assert(False)

	# Remove or exclusively include words appearing in read_texts:
	#print vocab_intersection
	vocab_final = []

	#THIS IS NEEDED FOR PRODUCTION
	#PSYCHE, MAYBE NOT
	#vvvvvvvvvvvvvvvvvvv UNCOMMENT
	#vocab_intersection = vocab_intersection.values('word')
	#UNCOMMENT^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	#So far this has been working fine on the devserver, but this should be the first change if anything breaks in production
	vocab_intersection_ids = []
	for each in vocab_intersection:
		vocab_intersection_ids.append(each.id)
	print(len(vocab_intersection_ids))
	#pdb.set_trace()
	#print len(vocab_intersection_ids),"len of vocab_intersection"
	if len(read_texts) > 0:
		if add_remove == 'Add': # Add is a bit of a mis-nomer: all it is (and all we want it to be) is the intersection: the words in the new text that you have seen before.
			return list(set(vocab_intersection_ids))

		else: # If user wants words appearing ONLY in the main text
			vocab_final = [word for word in list_word_ids if word not in vocab_intersection_ids]
			print(len(vocab_final), "returning this many words")
			return vocab_final
	else:
	# don't need to modify list; nothing to add/remove
		return list(set(vocab_intersection_ids))

#THIS FUNCTION IS FAR MORE VERSITILE THAN IT SOUNDS
def words_in_read_texts(word_appearences, read_texts): #returns a list of words in read_texts. read_texts just needs to a list of texts, not necessarially ones that have been read.
	print("read_texts", read_texts)
	r=[]
	for text_range in read_texts: #text range is meant to be a list where [0] is the book title, [1] is the start, and [2] is the end.
		print(text_range, 'text_range')
		book = text_range[0]
		if len(text_range) > 1:
			start = text_range[1]
			end = text_range[2]
		else:
			start = "start"
			end = "end"
		#print("vocaturus from_mindiv and to_mindiv with these inputs" , 'book=', book, 'start = ', start, 'end = ', end)
		from_mindiv = loc_to_mindiv(book, start)
		to_mindiv = loc_to_mindiv(book, end)
		#print("For read text, from, " , from_mindiv, "to, ",  to_mindiv)
		if start == end:
			print("Ooh corner case")
			to_node = loc_to_node(book,  end)
			child = to_node
			while not child.is_leaf():
				child = child.get_last_child()
				to_mindiv = child.least_mindiv
		#print("For read text,  from,  to",  from_mindiv,  to_mindiv)
		#print("book",  book)
		#print (text_range, 'text range')
		r.extend(list(word_appearences.objects.filter(text_name=book,mindiv__range=(from_mindiv, to_mindiv))))
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
	#print "in loc_to_node"
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

"""
def texts_with_most_overlap(request, read_texts, texts, language):
	unreads = [text for text in texts if text not in read_texts] #make sure each item is the the familiar format: text[0] = book title, [1]=start section, [2]=end section
	important = [] #this will be a list of lists of json strings of words appearing in unread texts
	for text in unreads:
	   important.append(get_words(request, language, text[0], bookslist, text[1], text_to[2], "Remove")) #note that we must use append, not extend, becasue extend will give us a flat list
	important.sort(key =len) #sorts important by length
	return render(request, "texts with most overlap.html ")
"""
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
		print('wrote the binary file')
		#this is capturing the output of management.call_command, which can only be a string
		out = StringIO()
		print(out, 'haha printout')
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
