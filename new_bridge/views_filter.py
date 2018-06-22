# from new_bridge.models import 'insert class/model names here' 
from django.views import generic
from new_bridge.models import BookTable, WordTable, BookTitles, BookTableGreek, WordTableGreek, BookTitlesGreek
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
import json
#thank you who ever wrote this with tabs instead of with four spaces, you are my favorite person who has been here before
#not sure if we are acutally using this file though
def filter(request, language):
	print(request.POST, 'request in views_filter.py')
	unchecked = request.POST.getlist('mine[]')
	print(unchecked)
	if language == "Latin":
		return latin_filter(request, unchecked)
	else: # language == "greek"
		return greek_filter(request, unchecked)

def latin_filter(request, unchecked):
	print ("in latin_filter")
	filtered_list = request.session.get('global_list')
	delete_list = []
	for i in unchecked:
		print(i)
		if i == "adj_1st" or i == "adj_3rd" or i == "adj_5th":
			filter_by = i[4]
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.decl == filter_by:
					delete_list.append(filtered_list[j])

		elif (i == "noun_1st" or i == "noun_2nd" or i == "noun_3rd" 
                        or i == "noun_4th" or i == "noun_5th" or i == "noun_6th"):
			filter_by = i[5]
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.decl == filter_by:
					delete_list.append(filtered_list[j])

		elif (i == "verb_1st" or i == "verb_2nd" or i == "verb_3rd" 
                        or i == "verb_4th" or i == "verb_5th"):
			filter_by = i[5]
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.conj == filter_by:
					delete_list.append(filtered_list[j])

		elif i == "Idioms":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.idiom == filter_by:
					delete_list.append(filtered_list[j])

		elif i == "Numbers":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.number == filter_by:
					delete_list.append(filtered_list[j])

		elif i == "Proper nouns":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.proper == filter_by:
					delete_list.append(filtered_list[j])

		elif i == "Reg_Adv":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if word.reg_adj_adv == filter_by:
					delete_list.append(filtered_list[j])

		else: # what is in unchecked at indexed i is merely a part of speech like "Nouns," "Adjectives," "Conjunctions," etc.
			filter_by = i[:-1]
			for j in range(len(filtered_list)-1):
				word = WordTable.objects.filter(title = filtered_list[j])
				word = word[0]
				if  word.part_of_speech == filter_by:
					delete_list.append(filtered_list[j])
	final_words = []
	for word in filtered_list:
		if not word in delete_list:
			final_words.append(word)

	final = []
	for word in final_words:
		temp_word = WordTable.objects.filter(title = word)
		temp_word = temp_word[0]
		final.append({"word":temp_word.display_lemma,"definition":temp_word.english_extended})
	return HttpResponse(json.dumps({"words": final}), content_type="application/json")

			

def greek_filter(request, unchecked):
	try:
		filtered_list = request.session.get('global_list')
		delete_list = []
		for i in unchecked:
			if (i == "adj_1st" or i == "adj_3rd" or i == "adj_5th") and "all_adj" in unchecked:
				filter_by = i[4]
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title= filtered_list[j])
					word = word[0]
					if word.decl == filter_by:
						delete_list.append(filtered_list[j])

			elif (i == "noun_1st" or i == "noun_2nd" or i == "noun_3rd" or i == "noun_6th") and "all_nouns" in unchecked:
				filter_by = i[5]
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title= filtered_list[j])
					word = word[0]
					if word.decl == filter_by:
						delete_list.append(filtered_list[j])

			elif i == "Idioms":
				filter_by = "1"
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title= filtered_list[j])
					word = word[0]
					if word.idiom == filter_by:
						delete_list.append(filtered_list[j])

			elif i == "Numbers":
				filter_by = "1"
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title= filtered_list[j])
					word = word[0]
					if word.number == filter_by:
							delete_list.append(filtered_list[j])

			elif i == "Proper nouns":
				filter_by = "1"
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title= filtered_list[j])
					word = word[0]
					if word.proper == filter_by:
						delete_list.append(filtered_list[j])

			elif i == "Reg_Adv":
				filter_by = "1"
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title= filtered_list[j])
					word = word[0]
					if word.reg_adject_adv_form == filter_by:
						delete_list.append(filtered_list[j])

			else: # what is in unchecked at index i is merely a part of speech word like "Adjectives," "Particles," etc.
				filter_by = i[:-1]
				for j in range(len(filtered_list)):
					word = WordTableGreek.objects.filter(title = filtered_list[j])
					word = word[0]
					part_of_speech_list = word.part_of_speech.split(",")
					
					for each in part_of_speech_list:
						each = each.replace(" ", "")
						if each  == filter_by:
							delete_list.append(filtered_list[j])
							break

		
		final_words = []
		for word in filtered_list:
			if not word in delete_list:
				final_words.append(word)
		
		final = []
		for word in final_words:
			temp_word = WordTableGreek.objects.filter(title = word)
			temp_word = temp_word[0]
			final.append({"word":temp_word.display_lemma,"definition":temp_word.english_definition})
			
		return HttpResponse(json.dumps({"words": final}), content_type="application/json")
	except Exception as e:
		print("ERROR: " + str(e))
