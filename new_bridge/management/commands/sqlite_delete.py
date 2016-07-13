#import argparse
import sys
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/')
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/new_bridge/management/commands')
from get_data import *
from django.core.management.base import BaseCommand, CommandError
from new_bridge.models import WordPropertyLatin,WordPropertyGreek, TextStructureGlossary, TextStructureNode, WordAppearencesLatin

class Command(BaseCommand):
    help = "Currently supports: WordAppearencesLatin, TextStructureNode"
    def add_arguments(self,parser):
        parser.add_argument("to_delete",nargs=1, type=str, help="Name of model to clear")
        parser.add_argument('text_name', nargs='?', type=str,default=False)

    def handle(self, *args, **options):
        name=False
        to_delete = args[0]
        if len(args)==2:
            text_name=args[1]
            name=True
            print "Warning: you are about to clear all of "+to_delete+" for " +text_name
        else:
            print "Warning: you are about to clear all of "+to_delete
        cont = raw_input("Are you sure you want to continue? (y/n) ")
        if cont[0].lower()=='y':
            if not name:
                if to_delete == 'TextStructureNode':
                  while TextStructureNode.objects.count():
                    ids = TextStructureNode.objects.values_list('pk', flat=True)[:100]
                    TextStructureNode.objects.filter(pk__in = ids).delete()
                elif to_delete == 'WordAppearencesLatin':
                  while WordAppearencesLatin.objects.count():
                    ids = WordAppearencesLatin.objects.values_list('pk', flat=True)[:100]
                    WordAppearencesLatin.objects.filter(pk__in = ids).delete()              
                else:
                    print "That is not currently an option for deleting! You can add it in new_bridge/management/commands/sqlite_delete.py"
            else:
                pass

        elif cont[0].lower()=='n':
            print "Okay! Did not delete"
        else:
            print "That wasn't an option, not deleting"