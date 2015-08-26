#!/usr/bin/env python

"""
Tools for adding a new text (presented as a csv document) to The Bridge.
"""

import sys, os, csv, re
# set Django env variable for tests run from cmd line:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
from new_bridge.models import *

# TODO documentation
def add_word_appearances(appearance_list, loc_list, text_name):
    i = 0
    loc_list_index = 0
    for appearance in appearance_list:
        if appearance[0] != loc_list[loc_list_index]:
            loc_list_index +=1
        entry = WordAppearences(text_name=text_name,
                word_id=appearance[1],mindiv=loc_list_index)
        entry.save()
        i+=1
    print i
    return

# Helper function for build_text_tree.  Builds root node and then calls b_t_t.
#
# txt_name is a str, the name of the text.
# loc_list points to a list of (location, word) tuples sorted by location. 
# Returns the root node of the text structure tree.
def build_text_tree_helper(txt_name, loc_list):
    root = TextStructureNode.add_root(text_name=txt_name, 
            subsection_level=-1, subsection_number=0, least_mindiv=0)
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
# loc_list points to a sorted list of unique locations.
# index (int) is the index in loc_list of the location of this fn call's node.
# subsection_lvl (int) specifies the subsection level of this fn call's node.
# Returns index of the 1st non-descendant location encountered.
def build_text_tree(loc_list, index, subsection_lvl, parent):
    ### Create new TextStructureNode from params:
    location = loc_list[index]
    location_split = location.split('.')
    subsection_num = location_split[subsection_lvl]
    # Cast to int, if subsection notation is not alphabetical:
    if re.search('[0-9]', subsection_num) is not None:
        subsection_num = int(subsection_num)
    node = TextStructureNode(subsection_level=subsection_lvl,
            subsection_number=subsection_num, least_mindiv=index)
    # Make current node a child to node from calling function.  
    #   Saves current node in the db, enabling it to have its own children:
    parent = TextStructureNode.objects.get(pk=parent.pk) #get() node to save it
    parent.add_child(instance=node)
    ### Recursive case 1: 
    #   Build descendant nodes represented by current location.
    #       e.g.:  if loc='1.2.3' and node = 1.x.x then build 1.2.x and 1.2.3
    if subsection_lvl < len(location_split)-1:
        index = build_text_tree(loc_list, index, subsection_lvl+1, node)
    ### Recursive case 2:
    #   If new loc is valid and contains descendants, start new subtree:
    if index < len(loc_list):
        if loc_list[index] == location:  # If prior call to bld_txt_tr
            index+=1
        while (index < len(loc_list) and 
                is_descendant(location,subsection_lvl,loc_list[index])):
            if subsection_lvl < len(location_split)-1:
                index = build_text_tree(loc_list, index, subsection_lvl+1, node)
    ### Base case: no more descendant nodes.
    return index 

# True if location loc2 is descendant of node specified by loc1 & subsectn_lvl
def is_descendant(loc1, subsection_lvl, loc2):
    loc1, loc2 = loc1.split('.'),loc2.split('.') #split into sections list
    for i in range(subsection_lvl+1):
        if re.search('[0-9]',loc1[i]) is not None:
            loc1[i] = int(loc1[i])
        if re.search('[0-9]',loc2[i]) is not None:
            loc2[i] = int(loc2[i])
        if loc1[i] != loc2[i]:
            return False
    return True

# Sorts csv data into sorted list of word locations.
#
# Returns a list of tuples of the form (location, word).
# listified_csv is a list derived from a csv file.
def parse_csv(listified_csv):
    appearances_index = listified_csv[0].index('appearances')
    word_id_index = listified_csv[0].index('word_id')
    text_locations = []
    for row in listified_csv:
        # Exclude empty cells:
        if re.search('[0-9a-zA-Z]', row[appearances_index]) is not None:
            # Create a list of tuples of the form (location, word_id):
            appearances = row[appearances_index].split(',')
            word_id = [row[word_id_index] for i in range(len(appearances))]
            text_locations += zip(appearances, word_id)
    text_locations.pop(0) #remove the column labels
    ### Sort word appearances by location:
    text_locations.sort(cmp=loc_cmp, key=lambda loc: loc[0])
    ### Create a list of unique locations:
    unique_locations = [text_locations[0][0]]
    for appearance in text_locations:
        if loc_cmp(unique_locations[-1],appearance[0]) != 0:
            unique_locations.append(appearance[0])
    return text_locations, unique_locations
    
# Compare function for word locations.
#
# Locations formatted as [section].[subsection].[sub-subsection], 
#   e.g. [book].[chapter].[verse]
def loc_cmp(loc1, loc2):
    loc1, loc2 = loc1.split('.'),loc2.split('.') #split into sections list
    try: 
        for i in range(len(loc1)):
            if re.search('[0-9]',loc1[i]) is not None:
                loc1[i] = int(loc1[i])
            if re.search('[0-9]',loc2[i]) is not None:
                loc2[i] = int(loc2[i])
            if loc1[i] != loc2[i]:
                return cmp(loc1[i],loc2[i])
        return 0
    except:
        print "ERROR!"
        print loc1,'\t',loc2
        return 1

if __name__ == "__main__":
    ### Open CSV file and extract loc. data:
    # Word location data should be in a column labeled "appearances":
    csvfile = open(sys.argv[1],'rb')
    csv_reader = csv.reader(csvfile,delimiter=',',quotechar='"')
    listified_csv = list(csv_reader)
    # Get sorted list of word locations and corresponding words,
    #   and a list of all unique locations in the .csv:
    sorted_appearances, unique_locations = parse_csv(listified_csv)
    print 'Unique locations:\t%s' % len(unique_locations)
    # Build text structure tree and store it in db.
    root = build_text_tree_helper('hoop',unique_locations)
    print  'Successfully built structure tree!'
    # Add word appearances to word appearances table:
    add_word_appearances(sorted_appearances,unique_locations,'hoop')
