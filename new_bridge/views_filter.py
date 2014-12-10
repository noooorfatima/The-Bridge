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
# defining global variables
global_list = [] # final_list

def filter(request, language):
	print request.POST
	unchecked = request.POST.getlist('mine[]')
	print unchecked
	if language == "latin":
		return latin_filter(request, unchecked)
	else: # language == "greek"
		return greek_filter(request, unchecked)

def latin_filter(request, unchecked):
	filtered_list = global_list[:]
	for i in unchecked:
		if i == "adj_1st" or i == "adj_3rd" or i == "adj_5th":
			filter_by = i[4]
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.decl == filter_by:
					del filtered_list[j]

		elif i == "noun_1st" or i == "noun_2nd" or i == "noun_3rd" or i == "noun_4th" or i == "noun_5th" or i == "noun_6th":
			filter_by = i[5]
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.decl == filter_by:
					del filtered_list[j]

		elif i == "verb_1st" or i == "verb_2nd" or i == "verb_3rd" or i == "verb_4th" or i == "verb_5th":
			filter_by = i[5]
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.conj == filter_by:
					del filtered_list[j]

		elif i == "Idioms":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.idiom == filter_by:
					del filtered_list[j]

		elif i == "Numbers":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.number == filter_by:
					del filtered_list[j]

		elif i == "Proper nouns":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.proper == filter_by:
					del filtered_list[j]

		elif i == "Reg_Adv":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.reg_adj_adv == filter_by:
					del filtered_list[j]

		else: # what is in unchecked at indexed i is merely a part of speech like "Nouns," "Adjectives," "Conjunctions," etc.
			filter_by = i[:-1]
			for j in range(len(filtered_list)):
				word = WordTable.objects.get(TITLE == filtered_list[j])
				if word.part_of_speech == filter_by:
					del filtered_list[j]
	
	return HttpResponse(json.dumps({"words": filtered_list}), content_type="application/json")

			

def greek_filter(request, unchecked):
	filtered_list = global_list[:]
	for i in unchecked:
		if i == "adj_1st" or i == "adj_3rd" or i == "adj_5th":
			filter_by = i[4]
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.decl == filter_by:
					del filtered_list[j]

		elif i == "noun_1st" or i == "noun_2nd" or i == "noun_3rd" or i == "noun_6th":
			filter_by = i[5]
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.decl == filter_by:
					del filtered_list[j]

		elif i == "Idioms":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.idiom == filter_by:
					del filtered_list[j]

		elif i == "Numbers":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.number == filter_by:
						del filtered_list[j]

		elif i == "Proper nouns":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.proper == filter_by:
					del filtered_list[j]

		elif i == "Reg_Adv":
			filter_by = "1"
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.reg_adject_adv_form == filter_by:
					del filtered_list[j]

		else: # what is in unchecked at index i is merely a part of speech word like "Adjectives," "Particles," etc.
			print "HERE: " + str(i)
			filter_by = i[:-1]
			for j in range(len(filtered_list)):
				word = WordTableGreek.objects.get(TITLE == filtered_list[j])
				if word.part_of_speech == filter_by:
					del filtered_list[j]

	return HttpResponse(json.dumps({"words": filtered_list}), content_type="application/json")
