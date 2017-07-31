#from new_bridge.models import 'insert class/model names here' 
from django.views import generic
import unicodedata
from new_bridge.models import *
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.core import serializers
from django.core import management
import json
import pdb
from StringIO import StringIO
import ast
import mysql.connector

def IndexView(request):
        sorted_latin_books=sorted(BookTitles.objects.all(),key=lambda book: (book.book_type,book.title_of_book))
        booklist_latin= [(book.title_of_book, book.book_type) 
                for book in sorted_latin_books]
        sorted_greek_books=sorted(BookTitlesGreek.objects.all(),key=lambda book: (book.book_type,book.title_of_book))        
        booklist_greek= [(book.title_of_book, book.book_type) 
                for book in sorted_greek_books]
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
	return render(request, 'index.html', 
                {"booklist_latin":booklist_latin,"booklist_greek":booklist_greek,"booklist_latin_TE":booklist_latin_TE,"booklist_latin_TK":booklist_latin_TK,"booklist_latin_LI":booklist_latin_LI,"booklist_greek_TE":booklist_greek_TE,"booklist_greek_TK":booklist_greek_TK,"booklist_greek_LI":booklist_greek_LI})
	
	
def AboutView(request):
     return render(request,'newabout2.html')

#class HelpView(generic.ListView):
#	template_name = 'help.html'
#	model = BookTable

#class ContactView(generic.ListView):
#	template_name = 'contact.html'
#	model = BookTable

# This function takes all of the information submitted through the form and creates a unique url for that query
# this will allow the user to copy the url and come back to exactly the same place they were before
@require_http_methods(["POST"])
def words_page_redirect(request,language):
    # Need to make sure all of the values are there, otherwise save as none
    text = "none"
    bookslist = []
    text_from = "start"
    text_to = "end"
    bookslist_string = ""
    from_sec = ""
    to_sec = ""
    
    # This makes sure it does not mess up the url
    if not request.POST["textlist"] == "":
	text = request.POST["textlist"]
	#print text,"identifying text in conditional" # delete
    #print request.POST["textlist"],"what happens when request.POST[textlist]"
    #print request.POST,"hello world request post"
    #print request.POST["textlist"]
    text_meta = TextMetadata.objects.get(name_for_humans=text)
    text_machine = text_meta.name_for_computers
    if ('book' in request.POST) == True:
	bookslist = request.POST.getlist("book")
	#bookslist = ",".join(bookslist)
	#bookslist = list_of_lists(bookslist)
	num_books = len(bookslist)
	loop_count = 0
	for i in bookslist:
		loop_count +=1
	
                try:
		    from_sec = request.POST[i + " from"]
		    to_sec = request.POST[i + " to"]
		except Exception as e:
		    print "ERROR: " + str(e)
                    print "exception as e conditional triggered." 

		if from_sec != "" and to_sec != "":
                    i = i + "$_" + from_sec + "_" + to_sec
		    #bookslist_string = bookslist_string + "_" + from_sec + "_" + to_sec
                elif from_sec != "" and to_sec == "":
                    i = i + "$_" + from_sec + "_" + "end"
                elif from_sec == "" and to_sec != "":
                    i = i + "$_" + "start" + "_" + to_sec

		if loop_count != num_books:
		    i = i + str("+")

		bookslist_string = bookslist_string + i
    else:
        bookslist_string = "none"

    if request.POST['text_from'] != "":
	text_from = request.POST["text_from"]

    if request.POST['text_to'] != "":
	text_to = request.POST["text_to"]
    add_remove = request.POST["add_remove_selector"]
    if bookslist_string !="none":
       new_bookslist_string = []
       for book in bookslist_string.split('+'):
	   try:
	      marker = book.index('$')
	   except ValueError:
	      marker = len(book)
		
           book2=book[:marker]
	   new_bookslist_string.append(TextMetadata.objects.get(name_for_humans=book2).name_for_computers+book[marker:])
       new_bookslist_string = "+".join(new_bookslist_string)
    else:
	new_bookslist_string = 'none'
    url = '/words_page/'+language+'/'+text_machine+'/'+new_bookslist_string+'/'+text_from+'/'+text_to+'/'+add_remove+'/'

    return HttpResponseRedirect(url)


# This function is now redirected to once the new url is constructed
def words_page(request,language,text,bookslist,text_from,text_to,add_remove):
    #change back to the human name because a bunch of stuff depends on it
    #Note that it is ironic that the machine strictly uses the name_for_humans as opposed the the name_for_computers that was made for it
    text_meta = TextMetadata.objects.get(name_for_computers=text)
    text = text_meta.name_for_humans
    new_bookslist_string = []
    bookslist_comp = bookslist
    if bookslist != 'none':
       for book in bookslist.split('+'):
 	   try:
              marker = book.index('$')
           except:
              marker = len(book)
           book2=book[:marker]
	   new_bookslist_string.append(TextMetadata.objects.get(name_for_computers=book2).name_for_humans+book[marker+1:])
       bookslist = "+".join(new_bookslist_string)	
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
        loop_counter = 1
        for book in temp_bookslist:
            booksection = book.split('_')
            book = booksection[0]
	    if len(booksection)==3:
		book += " from "+  booksection[1] + " to " + booksection[2]
            bookslist_formatted += book+ ", "
        bookslist_formatted = bookslist_formatted[:-2]
    if TextMetadata.objects.get(name_for_humans=text).local_def:
        loc_def = True
    else:
        loc_def = False
    try:
        return render(request,"words_page.html", {"language":language, "text":text,
        "text_comp":text_meta.name_for_computers, "bookslist_comp":bookslist_comp,
        "bookslist": bookslist, "bookslist_formatted": bookslist_formatted, 
        "text_from": text_from, "text_from_formatted": text_from_formatted, 
        "text_to": text_to, "text_to_formatted": text_to_formatted,
        "add_remove": add_remove, "add_remove_formatted": add_remove_formatted,"loc_def":loc_def})
    except Exception, e:
        print e

# Generates vocab list and returns as JSON string:
def get_words(request,language,text,bookslist,text_from,text_to,add_remove):
#change back to the human name because a bunch of stuff depenends on it
    #Note that it is ironic that the machine strictly uses the name_for_humans as opposed the the name_for_computers that was made for it
    #Also note that there was an issue with the fact and the apostrophe appearing in a title.
    #I think I switched to machine names in the spot the error was occuring, but I was considering switching it everywhere.
    # I still might do that because it will be REALLY inconvinient to switch once all of the data is uploaded.
    #debuggingthingy = true
    #if debuggingthingy:
       #print "\nAll paremeters for get words\n"
       ##rint request
       #print language
       #print text
       #print add_remove
       #print '\n'
    text_meta = TextMetadata.objects.get(name_for_computers=text)
    text = text_meta.name_for_humans
    if bookslist != 'none': 
       for book in bookslist:
          new_bookslist_string = []
          bookslist_comp = bookslist
          for book in bookslist.split('+'):
              try:
                 marker = book.index('$')
              except:
                 marker = len(book)
              book2=book[:marker]
              new_bookslist_string.append(TextMetadata.objects.get(name_for_computers=book2).name_for_humans+book[marker+1:])
       bookslist = "+".join(new_bookslist_string)
   

    # Parse string specifying names+ranges of read texts:
    if bookslist == "none":
        bookslist = []
    else:
        # Split read_texts into a list of lists of the form
        #   [ [text_name, text_from, text_to], etc.]:
    	bookslist = bookslist.split("+") #Split string
        for i in range(len(bookslist)): #Split each substring
            bookslist[i] = bookslist[i].split("_")
        
    # If no start/end loc was given, set to start/end of text:
    if text_from == 'none':
        text_from = 'start'

    if text_to == 'none':
        text_to = 'end'

    # Get words from database based on specified texts and ranges:
    word_ids = None
    word_property_table = None

    try:
        #print WordAppearencesLatin,language,text,text_from,text_to,bookslist,add_remove
        if language == "latin":
	    #pdb.set_trace()
            #print WordAppearencesLatin,language,text,text_from,text_to,bookslist,add_remove
            word_ids = generateWords(WordAppearencesLatin,language,text,text_from,text_to,bookslist,add_remove)
            word_property_table = WordPropertyLatin
            #print("\nword_property_table for Latin: " + word_property_table)
        else:
            word_ids = generateWords(WordAppearencesGreek,language,text,
                text_from,text_to,bookslist,add_remove)
            word_property_table = WordPropertyGreek
    except Exception, e:
        print "get words error 0"
        print e
    
    # take word ids and find the correct data for these words in correct table (word table)
    words_list = []
    print "length of word ids: " + str(len(word_ids))
    #print type(word_ids)
    #accu1=0
    #print "NEW PRINT STATEMENT"
    #accu1
    try:
        #print "INSIDE TRY STATEMENT"
        for each in word_ids:
            #accu1+=1
            #print "WORD LOOP", accu1
            if language == "latin":
               count = WordAppearencesLatin.objects.filter(word__exact=each).count()
            else:
               count = WordAppearencesGreek.objects.filter(word__exact=each).count()
            print "DEBUG IS THIS CAUSING PROBLEMS"
            word = word_property_table.objects.filter(id__exact=each)[0]
            word.corpus_rank = 9617 - count
            word.save()
            words_list.append(word_property_table.objects.filter(id__exact=each)[0])
            #if accu1 < 5:
               #print "debug: words_list add on " + accu1
               #print words_list
    except Exception, e:
	print "get words error 1"
        print e 
    json_words = serializers.serialize("json",words_list)
    #D#print type(json_words)
    print "WORD PROPERTY  TABLE", word_property_table #debug:
    json_words2 = json.loads(json_words)
    final_list = [] 
    test_for_in_final = {}
    print len(json_words2), "length of json words before adding appearances"
    for item in json_words2:
        if item['pk'] not in test_for_in_final.keys():
            if language != 'greek':
                word_app = WordAppearencesLatin.objects.filter(word=item['pk'],text_name=text)
            else:
                word_app = WordAppearencesGreek.objects.filter(word=item['pk'],text_name=text)
            item['fields']['position']=[(word.appearance, word.appearance.split('.')) for word in word_app]
            item['fields']['count']=len(item['fields']['position'])
            word_app = word_app[0]
            if not(word_app.local_def==None or word_app.local_def==""):
                item['fields']['local_def']=word_app.local_def
            else:
                item['fields']['local_def']="None"
            test_for_in_final[item['pk']] = item

    #make the appearance list sorted and then just take the first one
    for item in test_for_in_final:
        #test_for_in_final[item]['fields']['position'].sort(key= lambda tup: tuple(float(tup[1][i]) for i in range(len(tup[1]))))
        #test_for_in_final[item]['fields']['position'].sort(key= lambda tup: (float(tup[1][0]),float(tup[1][1])))# each item is tuple with the second item a list split on the .
        test_for_in_final[item]['fields']['position']=test_for_in_final[item]['fields']['position'][0][0]
    json_words = json.dumps(test_for_in_final.values())
    print len(test_for_in_final.values())
    #I do not know why it gets so big at this time
    #print json_words
    print len(json_words),"length aftering adding appearances"
    return HttpResponse(json_words, content_type="application/json")

def generateWords(word_appearences,lang,text,
        text_from,text_to,read_texts,add_remove):
    #Create a database filter for the texts+ranges in read_texts:
    print text_from
    print text_to
    print lang
    print text
    print read_texts
    print add_remove
    read_texts_filter = Q()
    if len(read_texts) > 0:
        for text_range in read_texts:
            # Create a new filter for the specified range of the specified text:
            book = text_range[0]
            if len(text_range) > 1:
                start = text_range[1]
                end = text_range[2]
            else:
                start = "start"
                end = "end"
            new_filter = Q(text_name__exact = text, 
                mindiv__range=(loc_to_mindiv(book,start), loc_to_mindiv(book,end)))
            # Add it to the combined filter with an OR operation.
            read_texts_filter = read_texts_filter | new_filter
            print read_texts_filter, "READ_TEXTS_FILTER"
    # Get WordAppearence objects for words appearing in main text:
    try: 
        from_mindiv = loc_to_mindiv(text,text_from)
        to_mindiv = loc_to_mindiv(text,text_to)
        print from_mindiv,to_mindiv
        if text_from == text_to:
           to_node = loc_to_node(text,text_to)
           child = to_node
           while not child.is_leaf():
              child = child.get_last_child()
           to_mindiv = child.least_mindiv
        print from_mindiv,to_mindiv
        vocab = word_appearences.objects.filter(text_name__exact=text,
                mindiv__range=(from_mindiv, to_mindiv))
        print len(vocab), "BUUUUHHHHHH"
        #loc_list = []
        #for vcab in vocab:
        #    loc_list.append(vcab.mindiv)
    except Exception, e:
        print "try 2 error: "
        print e

    # makes a list of dictionaries that contain the id num of all of the words in vocab variable
    # looks like: [{'word': 1001}, {'word': 2030'}, ...} etc.
    list_of_dict_of_words = vocab.values('word')
    # makes a list of these id numbers
    list_word_ids = []
    for each in list_of_dict_of_words:
	list_word_ids.append(each['word'])
   
    if len(read_texts)==0:
        print len(list(set(list_word_ids))),"WEEEEEEEEEEE WOOOOOOO"
        return list(set(list_word_ids))
    else:
        try:
            # Get words which appear in main text and any of the read_texts:

            #COMMENT THIS OUT FOR PRODUCTION
            #COMMENT vvvvvvvvvvvvvvvvvvvvvv
            #index = 100
            vocab_intersection = []
            #CONSIDER NOT COMMENTINGvvvvvvvvvvvvvvvvvvvvvvvvvv
            #don't want dups
            list_word_ids=list(set(list_word_ids))
            #PROBABLY DON't COMMENT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            #while index<len(list_word_ids):
            #    vocab_intersection.extend(list(word_appearences.objects.filter(read_texts_filter,
            #            word__in=list_word_ids[index-100:index],text_name=text).values('word')))
            #    index += 100
            #vocab_intersection.extend(list(word_appearences.objects.filter(read_texts_filter,
            #        word__in=list_word_ids[index-100:index],text_name=text).values('word')))
            #COMMENT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            #ORIGINAL, DOES NOT WORK IN SQLITE3
            #UNCOMMENT vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            #This stuff doesn't work 
            filter_list = []
            for text in read_texts: # unsure of how read_texts looks when selecting multiple text
            # with just one text it is [[text_name]], hence text[0]
                book = text[0]
                if len(text_range) > 1:
                   start = text_range[1]
                   end = text_range[2]
                else:
                   start = "start"
                   end = "end"

                filter_list.extend(list(word_appearences.objects.filter(text_name=book,mindiv__range=(loc_to_mindiv(book,start), loc_to_mindiv(book,end)))))
            for item in filter_list:
                # item.word.id might need to change
                # Make it whatever it needs to be to get the id that corresponds to the word
                if item.word.id in list_word_ids:
                    vocab_intersection.append(item.word)
            print vocab_intersection
            print len(vocab_intersection)
           # vocab_intersection = word_appearences.objects.filter(read_texts_filter, word__in=list_word_ids)
            print len(vocab_intersection),"For this test, this should be at most 50"
            #UNCOMMENT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        except Exception, e:
            print "try 3 error: "
            print e

    # Remove or exclusively include words appearing in read_texts:
    #print vocab_intersection
    vocab_final = []

    #THIS IS NEEDED FOR PRODUCTION
    #PSYCHE, MAYBE NOT
    #vvvvvvvvvvvvvvvvvvv UNCOMMENT
    #vocab_intersection = vocab_intersection.values('word')
    #UNCOMMENT^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    print vocab_intersection
    #print vocab_intersection.values('word')
    vocab_intersection_ids = []
    for each in vocab_intersection:
        vocab_intersection_ids.append(each.id)
    #pdb.set_trace()
    vocab_intersection_ids = list(set(vocab_intersection_ids))
    print len(vocab_intersection_ids),"len of vocab_intersection"
    if len(read_texts) > 0:
        if add_remove == 'Add': # If user wants words appearing in ALL texts 
	    for word in list_word_ids:
            	if word in vocab_intersection_ids:
	  	    vocab_final.append(word)
        else: # If user wants words appearing ONLY in the main text
            for word in list_word_ids:
                if word not in vocab_intersection_ids:
                    vocab_final.append(word)
    else:
        # don't need to modify list; nothing to add/remove
        vocab_final = vocab_intersection_ids
    #OUTSIDE OF CONDITIONALS
    print "WHY DON'T YOU WORK WHY"
    return vocab_final


# Translates a human-readable text location into a machine-readable mindiv.
#
# Traverses the text's text structure tree to find the appropriate mindiv.
# location (str) must be a specific, bottom-level location in the text.
#   e.g., if text is structured chapter.verse, must specifiy chapter AND verse.
#   location can alternatively be "start" or "end".
# Returns the appropriate mindiv (integer).
def loc_to_mindiv(text,location):
    print text
    print TextStructureNode.objects.filter(text_name=text)
    node = TextStructureNode.objects.filter(text_name=text)[0]
    print node, "Nodles"
    if location == 'start':
        pass # don't change nodes!  Root.least_mindiv is start of text.
    elif location == 'end':
        while not node.is_leaf(): # Go to rightmost node until end of tree.
            print node,node.least_mindiv
            node = node.get_last_child()
    else: # traverse tree according to given location.
        print location,"location"
	print type(location),"location type"
        loc = location.split('.')
        print loc,"loc"
        for subsection in loc:
            print subsection,"subsection"
            node = node.get_children().get(subsection_id__exact=subsection)
    print node, node.least_mindiv
    return node.least_mindiv

def loc_to_node(text,location):
    node = TextStructureNode.objects.filter(text_name=text)[0]
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


def generateLatinWords(language,text,bookslist,
        text_from,text_to,add_remove):
    word_list = []
    word_list2 = []
    final_list = []
    wordcount = 0
    all_entries = BookTable.objects.all()
    word_table_entries = WordPropertyLatin.objects.all()

    # Replace the nones with empty strings
    if bookslist == "none":
        bookslist = []
    else:
        # bookslist is split into a list of lists here; index 0 is the book, 1 is "from_sec", 2 is "to_sec"
    	bookslist = bookslist.split("+")
	bookslist_temp = []
        for i in bookslist:
            i = i.split("_")
            bookslist_temp.append(i)
        print "bookslist after splitting:\t",bookslist_temp
	bookslist = bookslist_temp[:]

    if text_from == "none":
        text_from = ""

    if text_to == "none":
        text_to = ""

    for each in all_entries:
        if text_from == "" and text_to == "" and text == each.field_book_text:
            word_list.append(each.title)
        elif text == each.field_book_text:
            if each.field_book_text.strip() == "DCC Latin Core":
                word_in_core = each.title
                for j in word_table_entries:
                    if word_in_core == j.title:
                        core_helper( j,j.dcc_frequency_rank, word_list,text_from, text_to)
            else:
                appearances = each.appearences
                helper(appearances, each, word_list, text_from, text_to)

        for i in bookslist:
            if i[0] == each.field_book_text:
                appearances = each.appearences
		from_sec = ""
		to_sec = ""
                if i[0] != "DCC Latin Core":
		    if len(i) > 1:
                        from_sec = i[1]
                        to_sec = i[2]
                    if from_sec == "":
                        word_list2.append(each.title)
                    else:
                        helper(appearances, each, word_list2, from_sec, to_sec)
                else:
		    if len(i) > 1:
                        from_sec = i[1]
                        to_sec = i[2]
                    if from_sec == "":
                        word_list2.append(each.title)
                    else:
                        word_in_core2 = each.title
                        for k in word_table_entries:
                            if word_in_core2 == k.title:
                                core_helper( k, k.dcc_frequency_rank, word_list2, from_sec, to_sec)

    # user wants to KEEP words in both "reading" and "have read"
    if add_remove == "Add":         
        for i in word_list:
            if i in word_list2:
                final_list.append(i)
    else: # user wants to remove words in both "reading" and "have read"
        for i in word_list:
	    if i not in word_list2:
	        final_list.append(i)
    
    # sort the list alphabetically
    final_list.sort()
    
    # set the global variable to be the list of words generated (the list is of TITLES, not display lemmas)
    # number of words in the list
    wordcount = len(final_list)
    
    # list of actual display lemmas/dictionary entries
    actual_words = []

    # grab the display lemmas
    all_words = WordPropertyLatin.objects.all()
    for word in final_list:
        for each in all_words:
            if word == each.title:
                actual_words.append(each)

    return actual_words

def generateGreekWords(language,text,bookslist,text_from,text_to,add_remove):
    word_list = []
    word_list2 = []
    final_list = []
    wordcount = 0
    all_entries = BookTableGreek.objects.all()
    word_table_entries = WordPropertyGreek.objects.all()
    print "so far, so good!  Pulled from db."

    # Replace the nones with empty strings
    if bookslist == "none":
        bookslist = []
    else:
        bookslist = bookslist.split("+")
	bookslist_temp = []
	for i in bookslist:
	    i = i.split("_")
	    bookslist_temp.append(i)

	bookslist = bookslist_temp[:]

    if text_from == "none":
        text_from = ""
    if text_to == "none":
        text_to = ""

    print "processed bookslist!"

    for each in all_entries:
        if text_from == "" and text_to == "" and text == each.field_book_text:
            word_list.append(each.title)
        elif text == each.field_book_text:
            if each.field_book_text.strip() == "DCC Greek Core":
                word_in_core = each.title
                for j in word_table_entries:
                    if word_in_core == j.title:
                        greek_core_helper( j,j.dcc_core_frequency, word_list,text_from, text_to)
            elif each.field_book_text.strip() == "Herodotus Book 1 Core (412 words > 10 times)":
                word_in_core = each.title
                for j in word_table_entries:
                    if word_in_core == j.title:
                        greek_core_helper( j,j.herodotus_1_frequency_rank, word_list,text_from, text_to)    
            elif each.field_book_text.strip() == "Introduction to Ancient Greek (Luschnig)":
                appearances = each.appearences
                greek_helper(appearances, each, word_list, text_from, text_to)
            elif each.field_book_text.strip() == "Reading Greek (JACT)":
                appearances = each.appearences
                greek_helper(appearances, each, word_list, text_from, text_to)
            else:
                appearances = each.appearences
                helper(appearances, each, word_list, text_from, text_to)

        for i in bookslist:
            if i[0] == each.field_book_text:
                appearances = each.appearences
		from_sec = ""
		to_sec = ""

		#setting from_sec and to_sec if user specifies them
		if len(i) > 1:
		    from_sec = i[1]
		    to_sec = i[2]

		if i[0] == "Introduction to Ancient Greek (Luschnig)":
		    if from_sec == "":
		        word_list2.append(each.title)
	            else:
		        greek_helper(appearances, each, word_list2, from_sec, to_sec)

		elif i[0] == "Reading Greek (JACT)":
		    if from_sec == "":
		        word_list2.append(each.title)
		    else:
		        greek_helper(appearances, each, word_list2, from_sec, to_sec)

                elif i[0] == "DCC Greek Core":
                    if from_sec == "":
                        word_list2.append(each.title)
                    else:
                        word_in_core2 = each.title
                        for k in word_table_entries:
                            if word_in_core2 == k.title:
                                greek_core_helper( k, k.dcc_core_frequency, word_list2, from_sec, to_sec)

                elif i[0] == "Herodotus Book 1 Core (412 words > 10 times)":
                    if from_sec == "":
                        word_list2.append(each.title)
                    else:
                        word_in_core2 = each.title
                        for k in word_table_entries:
                            if word_in_core2 == k.title:
                                core_helper( k, k.herodotus_1_frequency_rank, word_list2, from_sec, to_sec)

		else: # any other text
		    if from_sec == "":
		        word_list2.append(each.title)
		    else:
		        helper(appearances, each, word_list2, from_sec, to_sec)

    print "got through the ginormous text-specific filter."

    if add_remove == "Add": # the user wants to keep only words in both "reading" and "have read"
        for i in word_list:
            if i in word_list2:
                final_list.append(i)
    else: # the user wants to remove words in both "reading" and "have read"
	for i in word_list:
	    if i not in word_list2:
	        final_list.append(i)

    # sort the list alphabetically
    final_list.sort()

    # number of words in the final list
    wordcount = len(final_list)

    # list of the actual display lemmas/dictionary entries
    actual_words = []

    # grab display lemmas
    all_words = WordPropertyGreek.objects.all()
    for word in final_list:
        for each in all_words:
            if word == each.title:
                actual_words.append(each)
    return actual_words


# This function turns the appearances into a list of lists, where each appearance is itself a list,
# and each value in the list represents a certain subdivision of a text, like chapter, line, etc. 
def list_of_lists(a):
	# splits individual appearances first by commas
        a = a.split(",")
        b = []
	# then by periods
        for i in a:
                b.append(i.split("."))
	return b

# This function decides whether or not a word should be displayed, 
# based on the words appearances in a text. 
def helper(a, b, c, beg, end):
    beg = beg.split(".")
    end = end.split(".")
    a = list_of_lists(a)
    for i in range(len(a)):
        if len(beg) == 1 and len(end) == 1: # 1 subdivision
            if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
                return c.append(b.title)
    
        elif len(beg) == 2 and len(end) == 2: # 2 subdivisions
            if a[i][0] != "" and int(beg[0]) <= int(a[i][0]):
                if int(end[0]) == int(beg[0]) and int(end[0]) >= int(a[i][0]):
                    if int(beg[1]) <= int(a[i][1]) and int(end[1]) >= int(a[i][1]):
                        return c.append(b.title)
                elif int(end[0]) > int(a[i][0]):
			return c.append(b.title)
		elif int(end[0]) == int(a[i][0]) and int(end[1]) >= int(a[i][1]):
                        return c.append(b.title)

        elif len(beg) == 3 and len(end) == 3: #3 subdivisions
            if a[i][0] != ""  and int(beg[0]) <= int(a[i][0]) and int(end[0]) >= int(a[i][0]):
                if int(beg[1]) <= int(a[i][1]):
                    if int(end[1]) == int(a[i][1]):
                        if int(beg[2]) <= int(a[i][2]) and int(end[2]) >= int(a[i][2]):
                            return c.append(b.title)
                    elif int(end[1]) > int(a[i][1]):
                            return c.append(b.title)

	elif len(beg) == 1 and len(end) == 2:
	    if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][1]) <= int(end[1]):
			return c.append(b.title)

	elif len(beg) == 1 and len(end) == 3:
	    if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(end[0]) > int(a[i][0]):
			return c.append(b.title)
		elif int(end[0]) == int(a[i][0]):
			if int(a[i][1]) < int(end[1]):
				return c.append(b.title)
			elif int(a[i][1]) == int(end[1]) and int(a[i][2]) <= int(end[2]):
				return c.append(b.title)

	elif len(beg) == 2 and len(end) == 1:
	   if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) > int(beg[0]):
			return c.append(b.title)
		elif int(a[i][0]) == int(beg[0]):
			if int(a[i][1]) >= int(beg[1]):
				return c.append(b.title)

	elif len(beg) == 2 and len(end) == 3:
	   if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) == int(beg[0]) and int(a[i][1]) >= int(beg[1]):
			if int(a[i][0]) == int(end[0]):
				if int(a[i][1]) == int(end[1]) and int(a[i][2]) <= int(end[2]):
					return c.append(b.title)
				elif int(a[i][1]) < int(end[1]):
					return c.append(b.title)	
			elif int(a[i][0]) < int(end[0]):
				return c.append(b.title)
		elif int(a[i][0]) > int(beg[0]):
			if int(a[i][0]) == int(end[0]):
                                if int(a[i][1]) == int(end[1]) and int(a[i][2]) <= int(end[2]):
                                        return c.append(b.title)
                                elif int(a[i][1]) < int(end[1]):
                                        return c.append(b.title)
                        elif int(a[i][0]) < int(end[0]):
                                return c.append(b.title)

	elif len(beg) == 3 and len(end) == 1:
           if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
                if int(a[i][0]) == int(beg[0]):
                        if int(a[i][1]) == int(beg[1]) and int(a[i][2]) > int(beg[2]):
                                return c.append(b.title)
                        elif int(a[i][1]) > int(beg[1]):
                                return c.append(b.title)
                elif int(a[i][0]) > int(beg[0]):
                        return c.append(b.title)


	elif len(beg) == 3 and len(end) == 2:
	   if a[i][0] != "" and int(a[i][0]) >= int(beg[0]) and int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) == int(end[0]) and int(a[i][1]) <= int(end[1]):
			if int(a[i][0]) == int(beg[0]):
				if int(a[i][1]) == int(beg[1]) and int(a[i][2]) >= int(beg[2]):
					return c.append(b.title)
				elif int(a[i][1]) > int(beg[1]):
					return c.append(b.title)
			elif int(a[i][0]) > int(beg[0]):
				return c.append(b.title)
		elif int(a[i][0]) < int(end[0]):
			if int(a[i][0]) == int(beg[0]):
                                if int(a[i][1]) == int(beg[1]) and int(a[i][2]) >= int(beg[2]):
                                        return c.append(b.title)
                                elif int(a[i][1]) > int(beg[1]):
                                        return c.append(b.title)
                        elif int(a[i][0]) > int(beg[0]):
                                return c.append(b.title)

	    
def core_helper(x, y, z, beg, end):
	if y is not None and y != "":
		if int(beg) <= int(y) and int(end) >= int(y):
			return z.append(x.title)

def greek_core_helper(x, y, z, beg, end):
	if y is not None and y != "" and y != "#N/A":
        	if int(beg) <= int(y) and int(end) >= int(y):
	               	return z.append(x.title)



def greek_helper(a, b, c, beg, end):
    beg = beg.split(".")
    end = end.split(".")
    a = list_of_lists(a)
    for i in range(len(a)):
        if len(beg) == 1 and len(end) == 1:
            if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
                return c.append(b.title)

	elif len(beg) == 1 and len(end) == 2 and len(a[i]) == 1:
	    if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
		return c.append(b.title)
	
	elif len(beg) == 1 and len(end) == 2 and len(a[i]) ==2:
	    if int(a[i][0]) >= int(beg[0]):
		if int(a[i][0]) == int(end[0]) and a[i][1] <= end[1]:
			return c.append(b.title)
		elif int(a[i][0]) < int(end[0]):
			return c.append(b.title)
	
	elif len(beg) == 2 and len(end) == 1 and len(a[i]) == 1:
	    if int(beg[0]) <= int(a[i][0]) <= int(end[0]):
		return c.append(b.title)

	elif len(beg) == 2 and len(end) == 1 and len(a[i]) == 2:
	    if int(end[0]) >= int(a[i][0]):
		if int(a[i][0]) == int(beg[0]) and a[i][1] >= beg[1]:
			return c.append(b.title)
		elif int(a[i][0]) > int(beg[0]):
			return c.append(b.title)

        elif len(beg) == 2 and len(end) ==2 and len(a[i]) == 2:
            if int(beg[0]) <= int(a[i][0]):
                if int(end[0]) == int(beg[0]) and int(end[0]) >= int(a[i][0]):
                    if beg[1] <= a[i][1] and end[1] >= a[i][1]:
                        return c.append(b.title)
                elif int(end[0]) > int(a[i][0]):
                        return c.append(b.title)
                elif int(end[0]) == int(a[i][0]) and end[1] >= a[i][1]:
                        return c.append(b.title)

	elif len(beg) == 2 and len(end) == 2 and len(a[i]) == 1:
	    if int(beg[0]) <= int(a[i][0]): 
		if int(a[i][0]) <= int(end[0]):
			return c.append(b.title) 
#An admin page for importing updated spreadsheets
def myimport(request):
    query_results = TextStructureGlossary.objects.all()
    text_name_results = TextMetadata.objects.all()
    if request.method == 'POST':
        update_option = request.POST['update_option']
        lang = request.POST['select_lang']
        if update_option == "update_master":
            try:
                if len(request.FILES.getlist('datafile')) != 1:
                    return render(request, 'admin/myimport.html',{'multi_file' : True, 'query_results' : query_results,'text_name_results' : text_name_results})
                the_file = request.FILES['datafile']
            except:
                return render(request, 'admin/myimport.html',{'failed' : True, 'query_results' : query_results,'text_name_results' : text_name_results})
            if the_file.content_type != 'text/csv':
                return render(request, 'admin/myimport.html',{'failed' : True, 'query_results' : query_results,'text_name_results' : text_name_results})

            fileName = the_file.name
            print fileName
            with open('temp_csv_for_importing.csv','w') as f:
                f.write(the_file.read())
            #this is capturing the output of management.call_command, which can only be a string
            out = StringIO() 
            management.call_command('update_master','temp_csv_for_importing.csv',lang,stdout=out)
            error = out.getvalue().strip()
            print error
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
            for fileName in texts:
                with open('temp_csv_for_importing.csv','w') as f:
                    f.write(fileName.read())
                out = StringIO() 
                management.call_command('update_page','temp_csv_for_importing.csv',lang,stdout=out)
                print "Successfully updated page!"
                print "Now cleaning up all TextStructureNodes" #If there are two text structures for a text, removes all the older ones (not just for this updated text)
                management.call_command('sqlite_delete',"TextStructureNodeCLEAN")
                error = out.getvalue().strip()
                print error
                if error != str():
                    error = ast.literal_eval(error)
                if "text_name_error" in error:
                    return render(request, 'admin/myimport.html',{'query_results' : query_results,'text_name_error' : True, 'text_name' : error['text_name_error'],'text_name_results' : text_name_results })
                elif "lang_error" in error:
                    return render(request, 'admin/myimport.html',{'query_results' : query_results,'lang_error' : True,'text_name_results' : text_name_results })
                return render(request, 'admin/myimport.html',{"success" : True, 'query_results' : query_results,'text_name_results' : text_name_results})               
    else:
        return render(request, 'admin/myimport.html', {'query_results' : query_results,'text_name_results' : text_name_results})
