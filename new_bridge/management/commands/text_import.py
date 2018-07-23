#!/usr/bin/env python

"""
Tools for adding a new text (presented as a csv document) to The Bridge.

Usage: python text_import.py DATAFILE.csv TEXT_NAME LANGUAGE
    DATAFILE.csv is the filename of the csv file with text+word data.
    TEXT_NAME is the name of the text whose data will be imported.
        NOTE! This must match the column label which appears in DATAFILE.csv.
            ALSO must match the text's "name_for_computers" in the
             TextMetaData table.  That table doesn't need to be populated at time
             of import, but the names should be consistent accross tables.
    LANGUAGE is latin or greek.
"""

import sys, os, csv, re
import unicodedata

# set Django env variable for tests run from cmd line:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
from new_bridge.models import *


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
# Add word appearance data to the WordAppearanceLatin/Greek tables.
# is_greek is a bool specifying the text's language.
# text_name is the machine-readable name (i.e. purged of special characters)
#   of the text.  So, in the "TextMetadata" table, the "name_for_computers".
def add_word_appearances(is_greek, appearance_list, loc_list, text_name,listified_csv):
    #print(appearance_list, "Appearance List")
    print("is_greek", is_greek)
    print(loc_list,"Loc_list")
    #print(text_name, "text name")
    #print(listified_csv, "listified csv")
    loc_list_index = 0
    #check if there are local_defs
    try:
        print(text_name)
        TextMetadata.objects.get(name_for_humans=text_name)
    except Exception as e:
        print("ERROR", e)
        error = e
        assert(False)
    if TextMetadata.objects.get(name_for_humans=text_name).local_def:
        local_def_dict = {}
        for entry in listified_csv[1:]:
           local_def_dict[entry[0]]=entry[3]
        for appearance in appearance_list:
            if appearance[0].strip() != loc_list[loc_list_index].strip():
                print('changing loc_list_index, with these two:', appearance[0].strip(), loc_list[loc_list_index].strip())
                loc_list_index +=1
            if is_greek:
                entry = WordAppearencesGreek(text_name=text_name, text_name_for_computers=TextMetadata.objects.get(name_for_humans=text_name).name_for_computers,
                        word_id=appearance[1].strip(),mindiv=loc_list_index, appearance= loc_list[loc_list_index].replace('_','.'),local_def=local_def_dict[appearance[1]] )
            else:

                entry = WordAppearencesLatin(text_name=text_name, text_name_for_computers=TextMetadata.objects.get(name_for_humans=text_name).name_for_computers,
                        word_id=appearance[1].strip(),
                        mindiv=loc_list_index,
                        appearance= loc_list[loc_list_index].replace('_','.'),
                        local_def=local_def_dict[appearance[1]])
            entry.save()
    else:
        print("adding word apps")
        #print(appearance_list)
        for appearance in appearance_list:
            #print( appearance, "APPEARANCE")
            #print( len(appearance_list), "app list")
            if appearance[0].strip() != loc_list[loc_list_index].strip():
                loc_list_index +=1
            if is_greek:
                entry = WordAppearencesGreek(text_name=text_name,
                        word_id=appearance[1].strip(),mindiv=loc_list_index,appearance= loc_list[loc_list_index].replace('_','.'))
            else:
                #print(loc_list)
                #print(loc_list_index)
                #print(loc_list[loc_list_index])
                #print("adding word appearance: for apperarnce ", loc_list[loc_list_index].replace('_','.'), "with mindiv ", loc_list_index)
                entry = WordAppearencesLatin(text_name=text_name,
                        word_id=appearance[1].strip(),
                        mindiv=loc_list_index,
                        appearance= loc_list[loc_list_index].replace('_','.'))
            #print(entry)
            entry.save()
        print("added word apps")
    return


# Helper function for build_text_tree.  Builds root node and then calls b_t_t.
#
# txt_name is a str, the name of the text.
# loc_list points to a list of (location, word) tuples sorted by location.
# Returns the root node of the text structure tree.
def build_text_tree_helper(txt_name, loc_list):
    root = TextStructureNode.add_root(text_name=txt_name,
            subsection_level=-1, subsection_id='0', least_mindiv=0)
    # Call recursive fn to build tree for each top-level subsection:

    next_index = build_text_tree(loc_list,0,0,root)
    while next_index < len(loc_list):
        next_index = build_text_tree(loc_list,next_index,0,root)
    return root

# Recursively builds a SQL tree representing the structure of a text.
#   Structure is specified by a list of locations in the text.
#   Params loc_list[index] & subsct_lvl specify node created in each fn call.
#       Recursive calls to build_text_tree this node's descendants.
#

 #loc_list points to a sorted list of unique locations.
 #index (int) is the index in loc_list of the location of this fn call's node.
 #subsection_lvl (int) specifies the subsection level of this fn call's node. IT IS UNRELATED TO THE TEXT'S LEVEL OF SUBSECTIONING
 #Returns index of the 1st non-descendant location encountered.

def build_text_tree(loc_list, index, subsection_lvl, parent):
    #print("recursive call with index = ", index)
    ### Create new TextStructureNode from params:
    location = loc_list[index]
    location_split1 = location.split('.')
    location_split = []
    for i in location_split1:
        location_split.extend(i.split('_'))
    subsection_id = location_split[subsection_lvl]
    node = TextStructureNode(subsection_level=subsection_lvl,
            subsection_id=subsection_id.strip(), least_mindiv=index)
    # Make current node a child to node from calling function.
    #   Saves current node in the db, enabling it to have its own children:
    parent = TextStructureNode.objects.get(pk=parent.pk) #get() node to save it
    parent.add_child(instance=node)
    ### Recursive case 1:
    #   Build descendant nodes represented by current location.
    #       e.g.:  if loc='1.2.3' and node = 1.x.x then build 1.2.x and 1.2.3
    if subsection_lvl < len(location_split)-1:
        #print("in recursive case 1")
        index = build_text_tree(loc_list, index, subsection_lvl+1, node)
    ### Recursive case 2:
    #   If new loc is valid and contains descendants, start new subtree:
    if index < len(loc_list):
        #print('entered recursive case 2')
        if loc_list[index] == location:  # If prior call to bld_txt_tr
            index+=1
            #print("added 1 to index")
        while (index < len(loc_list) and is_descendant(location,subsection_lvl,loc_list[index])):
            #print("in while loop in recursion")
            if subsection_lvl < len(location_split) -1:
                #print("actually making recursive call in case 2")
                index = build_text_tree(loc_list, index, subsection_lvl+1, node)
            else:
                index = build_text_tree(loc_list, index, subsection_lvl+1, node)

    ### Base case: no more descendant nodes.
    return index

# True if location loc2 is descendant of node specified by loc1 & subsectn_lvl
def is_descendant(loc1, subsection_lvl, loc2):
    loc1, loc2 = loc1.split('_'),loc2.split('_') #split into sections list #Changed to '_' from '.' to reflect new spreadsheet
    try:
        for i in range(subsection_lvl+1):
            if re.search('[0-9]',loc1[i]) is not None:
                loc1[i] = int(loc1[i])
            if re.search('[0-9]',loc2[i]) is not None:
                loc2[i] = int(loc2[i])
            if loc1[i] != loc2[i]:
                return False
        return True
    except IndexError:
        print("ERROR! in is_descendant")
        print(loc1,'\t',loc2)
        return False



# Sorts csv data into sorted list of word locations.
#
# Returns a list of tuples of the form (location, word).
# listified_csv is a list derived from a csv file.
def parse_csv(listified_csv, text_name):
    try:
        print("Entered parse_csv")
        print(listified_csv[0])
        appearances_index = listified_csv[0].index(text_name)
    except ValueError:
        print(text_name, "\t is not a column header in the CSV!")
        return {"text_name_error":text_name}

    word_id_index = listified_csv[0].index('word_id')
    text_locations = []
    for row in listified_csv[1:]:
        # Exclude empty cells:
        if re.search('[0-9a-zA-Z]', row[appearances_index]) is not None:
            # Create a list of tuples of the form (location, word_id):
            appearances = row[appearances_index]
            appearances = appearances.replace(" ", "").split(',')
            word_id = [row[word_id_index] for i in range(len(appearances))] #makes a list of the same word id equal in lenght to the appearances
            text_locations += list(zip(appearances, word_id))
    #text_locations.pop(0) #remove the column labels # now done with listified_csv[1:]
    ### Sort word appearances by location:
    ### Create a list of unique locations:
    print(text_locations[0:10])
    text_locations.sort(key= cmp_to_key(lambda loc1, loc2: loc_cmp(loc1[0], loc2[0])))
    print("sorted text_locations")
    print(text_locations)
    unique_locations = set()
    [unique_locations.add(appearance[0].strip()) for appearance in text_locations]
    unique_locations = list(unique_locations)
    print('about to sort unique_locations')
    unique_locations.sort(key= cmp_to_key(loc_cmp))
    print(unique_locations, 'sorted locations')
    print(len(text_locations), 'number of total locations')
    return text_locations, unique_locations


# Compare function for word locations.
#
# Locations formatted as [section].[subsection].[sub-subsection],
#   e.g. [book].[chapter].[verse]
# Location compare
def loc_cmp(loc1, loc2):

    loc1 = loc1.split('_')
    loc2 = loc2.split('_') #split into sections list
    #Might need to change this to underscores for update
    if len(loc1)==len(loc2):
        #D#print "Going in 1"
        #print(loc1, "loc 1")
        #print(loc2, "loc 2")
        try:
            for i in range(len(loc1)):
                if re.search('[0-9]',loc1[i]) is not None and re.search('[a-z]', loc1[i]) is None:
                    #print('loc1 has an int')
                    loc1[i] = int(loc1[i])
                elif re.search('[a-z]', loc1[i]) is not None:
                    loc1[i] = 1000000000 + ord(loc1[i]) #if there is a letter, make sure it goes after
                if re.search('[0-9]',loc2[i]) is not None and re.search('[a-z]', loc2[i]) is None:
                    #print('loc2 has an int')
                    loc2[i] = int(loc2[i])
                elif re.search('[a-z]', loc2[i]) is not None:
                    loc2[i] = 1000000000 + ord(loc2[i]) #if there is a letter, make sure it goes after
                if loc1[i] != loc2[i]:
                    return cmp(loc1[i],loc2[i])

            return 0
        except:
            print("ERROR! (line 190) Try using _ instead of .")
            print(loc1,'\t',loc2)
            return 1
    elif len(loc1)<len(loc2):
        #D#print "Venturing down 2"
        try:
            for i in range(len(loc1)):
                if re.search('[0-9]',loc1[i]) is not None and re.search('[a-z]', loc1[i]) is None:
                    loc1[i] = int(loc1[i])
                elif re.search('[a-z]', loc1[i]) is not None:
                    loc1[i] = 1000000000 + ord(loc1[i]) #if there is a letter, make sure it goes after
                if re.search('[0-9]',loc2[i]) is not None and re.search('[a-z]', loc2[i]) is None:
                    loc2[i] = int(loc2[i])
                elif re.search('[a-z]', loc2[i]) is not None:
                    loc2[i] = 1000000000 + ord(loc2[i]) #if there is a letter, make sure it goes after
                if loc1[i] != loc2[i]:
                    return cmp(loc1[i],loc2[i])
            #This is what is different from above
            return -1
        except:
            print("ERROR! (line 206)")
            print(loc1,'\t',loc2)
            return 1

    elif len(loc1)>len(loc2):
        #D#print "Exploring 3"
        try:
            #This is what is different from above
            for i in range(len(loc2)):
                if re.search('[0-9]',loc1[i]) is not None and re.search('[a-z]',loc1[i]) is None:
                    loc1[i] = int(loc1[i])
                elif re.search('[a-z]', loc1[i]) is not None:
                    loc1[i] = 1000000000 + ord(loc1[i]) #if there is a letter, make sure it goes after
                if re.search('[0-9]',loc2[i]) is not None and re.search('[a-z]' , loc2[i]) is None:
                    loc2[i] = int(loc2[i])
                elif re.search('[a-z]', loc2[i]) is not None:
                    loc2[i] = 1000000000 + ord(loc2[i]) #if there is a letter, make sure it goes after the real location
                if loc1[i] != loc2[i]:
                    return cmp(loc1[i],loc2[i])
            #This is what is different from above
            return 1
        except:
            print("ERROR! (line 223)")
            print(loc1,'\t',loc2)
            return 1


    else:
        print("Something is horribly wrong")


def cmp(a, b): #cmp was a built on function for python 2, but it is gone in 3. it did a useful thing, so we are defining it here based on the docs for python2
    if a > b:
      return 1
    elif a == b:
       return 0
    else:
       return -1

#Reads 3 input strs from command line.  Returns the input strs.
def cmd_parse():
    if len(sys.argv) == 4:
        dataFile_name, targetText_name, language = sys.argv[1::]
        return dataFile_name, targetText_name, language
    # If invalid input:
    else:
        progname = os.path.basename(sys.argv[0])
        print(('usage:\t'+progname+
                '  DATAFILE.csv TEXT_NAME LANGUAGE'), file=sys.stderr)
        sys.exit(1)

def main(csvfilename, language):
    #print("beep boop bop beep") #Odi et amo Dylan
    print("in text_import.py main")
    text_name= "Text Name now set later based on header of second column"
    print(csvfilename,text_name,language)
    with open(csvfilename) as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=',',quotechar='"')
        listified_csv = list(csv_reader)
        text_name=listified_csv[0][2]

        # Remove any old entries
        if language.lower() == "latin":
           print(text_name, "text_name, line 263 of text_import")
           print("Deleting this many old entries:", len(WordAppearencesLatin.objects.filter(text_name=text_name)))
           WordAppearencesLatin.objects.filter(text_name=text_name).delete()

        else:
           print("Deleting this many old entries:", len(WordAppearencesGreek.objects.filter(text_name=text_name)))
           WordAppearencesGreek.objects.filter(text_name=text_name).delete()

        # Get sorted list of word locations and corresponding words,
        #   and a list of all unique locations in the .csv:
        try:
            sorted_appearances, unique_locations = parse_csv(listified_csv, text_name)
        except ValueError:
            return  {"text_name_error":text_name}
        print('Unique locations:\t%s' % len(unique_locations))

        # Build text structure tree and store it in db.
        print("about to start build_text_tree_helper")
        print("A CALL TO BUILD TEXT TREE HELPER")
        root = build_text_tree_helper(text_name,unique_locations)
        print('Successfully built structure tree!')

        # Add word appearances to word appearances table:
        is_greek = (language.lower() == "greek")

        catch_error = add_word_appearances(is_greek, sorted_appearances,
           unique_locations, text_name, listified_csv) #ok so this is really, really weird, bear with me:
           #add_word_appearances should not return anything, and is a purely imperative function. However, for error catching purposes, if there is an error, we return it.
        if catch_error:
            print("add_word_appearances failed")
            print(catch_error)
        else:
            print('Added word appearance info to DB. Done!')

        print('Added word appearance info to DB. Done!')


if __name__ == "__main__":
    ### Open CSV file and extract loc. data:
    # Word location data should be in a column labeled "appearances":
    csvfilename, text_name, language = cmd_parse()
    with open(csvfilename) as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=',',quotechar='"')
        listified_csv = list(csv_reader)

        # Get sorted list of word locations and corresponding words,
        #   and a list of all unique locations in the .csv:
        sorted_appearances, unique_locations = parse_csv(listified_csv, text_name)
        print('Unique locations:\t%s' % len(unique_locations))

        # Build text structure tree and store it in db.
        print("A CALL TO BUILD TEXT TREE HELPER")
        root = build_text_tree_helper(text_name,unique_locations)
        print('Successfully built structure tree!')

        # Add word appearances to word appearances table:
        print(language.lower())
        is_greek = (language.lower() == "greek")
        add_word_appearances(is_greek, sorted_appearances,
               unique_locations, text_name,listified_csv)
