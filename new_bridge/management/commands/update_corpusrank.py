#A script for updating the word frequencies of each word.
import new_bridge.models
from django.core.management.base import BaseCommand, CommandError
import sys
import os
import mysql.connector

cnx = mysql.connector.connect(user='root', password='Pushkaisacat881427', host='127.0.0.1', database='new_new_bridge')
cursor = cnx.cursor(buffered=True)

#from new_bridge.models import *
#import pandas as pd
class Command(BaseCommand):
    help = "Run this command to update the corpus_rank field of all entries in the database."
    def add_arguments(self,parser):
        print("adding arguments")
        print(parser, 'parser')
        parser.add_argument("language", nargs="+", type=str, help="The language we are importing for (Greek or Latin)")

    def handle(self, *args, **options):
        lang = str(input("enter either 'greek' or 'latin' (no apostrophes) to specify your language. Press CTRL+C to exit." + '\n'))
        if lang == "Greek" or lang == "greek":
             query = ("SELECT title, count(title) FROM new_bridge_wordappearencesgreek a JOIN `new_bridge_wordpropertygreek`p on a.word_id = p.`id` GROUP by title ORDER BY count(title) DESC")
        elif lang == "Latin" or lang == "latin":
            query = ("SELECT title, count(title) FROM new_bridge_wordappearenceslatin a JOIN `new_bridge_wordpropertylatin`p on a.word_id = p.`id` GROUP by title ORDER BY count(title) DESC")
        assert(query)
        cursor.execute(query)
        same_count_list = []
        prev_word_freq = 10000000
        indexaccu = 0
        rank = 0
        cur_word = ""
        for row in cursor:
               #print("\n==============================================================================")
               if rank == 50 or rank == 80 or rank == 100 or rank == 120 or rank == 140 or rank == 160 or rank == 180 or rank == 200 or rank == 250 or rank == 500 or rank == 1000 or rank == 2000 or rank == 5000 or rank == 10000:
                    print("Currently at rank ", rank, " (note that the larger the rank, the closer you are to done)")
               cur_title = row[0]
               count = row[1]
               if lang == "greek" or lang == "Greek":
                   cur_word = new_bridge.models.WordPropertyGreek.objects.get(title__exact=cur_title)
               elif lang == "latin" or lang == "Latin":
                   cur_word = new_bridge.models.WordPropertyLatin.objects.get(title__exact=cur_title)
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
               #if lang == "latin":
                #   print("\n\ttitle: ", row[0], "\tcorpus_rank: ", new_bridge.models.WordPropertyLatin.objects.get(title__exact=row[0]).corpus_rank, "\tcount: ", row[1])
              # else:
                #   print("\n\ttitle: ", row[0], "\tcorpus_rank: ", new_bridge.models.WordPropertyGreek.objects.get(title__exact=row[0]).corpus_rank, "\tcount: ", row[1])

        print("FINISHED")
