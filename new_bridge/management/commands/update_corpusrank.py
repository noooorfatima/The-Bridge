#A script for updating the word frequencies of each word.

from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import *
import sys
import os


#from new_bridge.models import *
#import pandas as pd
class Command(BaseCommand):
    help = "Run this command to update the corpus_rank field of all entries in the database."
    def add_arguments(self,parser):
                parser.add_argument("language",nargs=1, type=str, help="The language we are importing for (Greek or Latin)")

    def handle(self, *args, **options):
        lang = ""
        try:
           lang = args[0]
        except:
          print "No argument for language detected. This script requires an argument denoting which languange's corpus ranks you would like to update."
          print "enter either 'greek' or 'latin' as an argument"
          return
        if lang != "greek" and lang != "latin":
            while lang != "greek" and lang != "latin":
               print "Please specify which language's corpus ranks you would like to update."
               print "enter either 'greek' or 'latin' on the following line."
               lang = raw_input("enter either 'greek' or 'latin' (no apostrophes) to specify your language. Press CTRL+C to exit.")
        if lang == "greek":
             query = ("SELECT title, count(title) FROM new_bridge_wordappearencesgreek a JOIN `new_bridge_wordpropertygreek`p on a.word_id = p.`id` GROUP by title ORDER BY count(title) DESC")
        elif lang == "latin":
             query = ("SELECT title, count(title) FROM new_bridge_wordappearenceslatin a JOIN `new_bridge_wordpropertylatin`p on a.word_id = p.`id` GROUP by title ORDER BY count(title) DESC")
	cursor.execute(query)
	same_count_list = []
	prev_word_freq = 10000000
	indexaccu = 0
	rank = 0
        cur_word = ""
	for row in cursor:
               print "\n=============================================================================="
               if rank == 50 or rank == 80 or rank == 100 or rank == 120 or rank == 140 or rank == 160 or rank == 180 or rank == 200 or rank == 250:
                    print "Currently at rank ", rank, " (note that the larger the rank, the closer you are to done)"
               cur_title = row[0]
               count = row[1]
               if lang == "greek":
                   cur_word = WordPropertyGreek.objects.get(title__exact=cur_title)
               elif lang == "latin":
                   cur_word = WordPropertyLatin.objects.get(title__exact=cur_title)
               if prev_word_freq == count:
                   same_count_list.append(count)
                   rank+=1
                   #print "this corpus rank should be the same as the one before it"
                   #print "subtraction expression: rank - len(same_count) == ", str(rank-len(same_count_list))
                   #print "length of same count list at this time", len(same_count_list)
                   cur_word.corpus_rank = rank - len(same_count_list)
               elif prev_word_freq > count:
                   prev_word_freq = count
                   rank+=1
                   #"print this corpus rank is less than the one before it"
                   #"print length of same_count: ", len(same_count_list)
                   #"rank ", rank
                   if len(same_count_list) != 0:
                      same_count_list = []
                   cur_word.corpus_rank = rank
               cur_word.save()
               if lang == "latin":
                   print "\n\ttitle: ", row[0], "\tcorpus_rank: ", WordPropertyLatin.objects.get(title__exact=row[0]).corpus_rank, "\tcount: ", row[1]
               else:
                   print "\n\ttitle: ", row[0], "\tcorpus_rank: ", WordPropertyGreek.objects.get(title__exact=row[0]).corpus_rank, "\tcount: ", row[1]

               '''#print "\nSTART OF FOR LOOP, RANK: ", rank
		rank+=1
                print "\n=========================================================================================="
                print "\nSTART OF FOR LOOP, RANK: ", rank, "\ttitle: ", row[0]
		#print "\n\ttitle: ", row[0], "\tcorpus_rank: ", WordPropertyGreek.objects.get(title__exact=row[0]).corpus_rank, "\tcount: ", row[1]
    		cur_title = row[0]
    		count = row[1]
                #print "prev_word_freq: ", prev_word_freq
                #print "count: ", count
    		if prev_word_freq == count:
                        print "prev_word_freq == count.\trank: ", rank
			indexaccu+=1
                        #if indexaccu==1:
                           #same_count_list.append(prev_word_freq)
                        same_count_list.append(count)
                        print "SAME COUNT LIST: ", str(same_count_list)
			prev_word_freq = count
       			cur_word = WordPropertyGreek.objects.get(title__exact=cur_title)
			cur_word.corpus_rank = rank - indexaccu
                        cur_word.save()
                        prev_rank = rank - indexaccu
                        #last_indexaccu = indexaccu
                        print "In first conditional, prev_rank: ", prev_rank
                        print "INDEX ACCU: ", indexaccu
                        
		elif prev_word_freq > count:
			if indexaccu != 0:
				print "indexaccu is not 0. Rank value: ", rank, "\tindexaccu: ", indexaccu, "\tprev_rank: ", prev_rank
				rank = prev_rank
                                print "new rank: ", rank
                                print "SAME COUNT LIST (prev_word > count): ", str(same_count_list)
                                prev_word_freq = count
                                indexaccu = 0
				cur_word = WordPropertyGreek.objects.get(title__exact=cur_title)
				cur_word.corpus_rank = rank + 1
				cur_word.save()
                                #rank+=1
			else:
                                print "indexaccu IS 0. RANK VALUE: ", rank, "\tprev_rank: ", prev_rank
                                #if prev_word_freq > count:
                                   #rank+=1
                                print "SAME COUNT LIST (prev_word > count): ", str(same_count_list)
				prev_word_freq = count
				cur_word = WordPropertyGreek.objects.get(title__exact=cur_title)
				cur_word.corpus_rank = rank
				cur_word.save()
    		#word_list.append((title, count),)
		print "\n\ttitle: ", row[0], "\tcorpus_rank: ", WordPropertyGreek.objects.get(title__exact=row[0]).corpus_rank, "\tcount: ", row[1]
                print "-------------------------------------------------------------------------------------------------"

                #if count > 200:
    		    #print cur_title, " rank: ", WordPropertyGreek.objects.get(title__exact=cur_title).corpus_rank, "\tcount : ", count'''
	print "FINISHED"
