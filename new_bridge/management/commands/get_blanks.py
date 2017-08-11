import sys
import os
from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import WordPropertyLatin,WordPropertyGreek, TextStructureGlossary, WordAppearencesLatin, WordAppearencesGreek

class Command(BaseCommand):
    help = "Imports/updates the database"
    def add_arguments(self,parser):
        parser.add_argument("language",nargs=1, type=str, help="The language we are importing for (Greek or Latin)")

    def handle(self, *args, **options):
        lang = args[0]
        with open("blanks.txt","w") as f:
            checked_words = {}
            if lang[0].lower() == "l":
                appearances = WordAppearencesLatin.objects.all()
                for app in appearances: #there are 100000 so it might take a bit
                    word = app.word
                    try:
                        checked_words[word.title]
                    except KeyError:
                        if word.title == "ADEMO":
                            print word.title,":",word.display_lemma    
                        checked_words[word.title] = True
                        if word.display_lemma == "" or word.display_lemma == "0":
                            f.write(word.title+"\n")

