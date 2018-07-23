# bridge-repo
Refactored version of the Bridge: Now using python 3.5 instead of 2.7!

The broad problem: given two sets of words, find either their intersection or difference.
  The crucial sub-problem: get the correct two sets of words.
How we solved it:
Each text is stored as a materialized path tree. Each location is tied to a mindiv: mindiv 0 is the start of the text (usually human location 1,
1.1, or 1.1.1), 1 is the next section, and so forth until the end of the text. The WordApperances tables store word IDs, mindivs, and text names
(which are the same as the TextMetadata name for humans). Django's database queries let us filter the word WordApperances based on text name and
midiv range. We store the word ids from each section in a set, and do the operation the user requested (intersection or difference), and then
find the title for the word ids. This is one of the slowest parts for large queries, and can sometimes take two minutes.

Remaining problems:
A great deal of energy is being spent converting name_for_humans to name_for_computers (and vice versa), so here is a quick break down of where
we use each one:
name_for_computers:
  URLs
  showing the right subsection data on the landing page
name_for_humans:
  the autocomplete field
  word_appearences tables
  converting locations to mindivs
  convert location to node
Possible solutions:
We could switch to using the name for humans for subsections (a matter of changing text_structure TextStructureGlossaries), and slugify the url.
We could change the way things are made in the importer, so that word appearances and TextStructureNodes use name for computers. If we do this
one, it will be easier to mark texts with local definitions in the search box, since we will only be using name for humans there.
Some stuff in the html is acting weird.

Where things are:
  javascript: /static and /static/js (collect static put everything directly in static)
  css: /static and static/css
  html: new_bridge/templates
  importing stuff: new_bridge/management/commands
The autocomplete field sometimes decides to break. Run collectstatic and it should come back, otherwise uninstall, run collectstatic and add a global counter to select2.full.js, which is in autocomplete_light/vendor/select2/dist/js, and make it add to the counter for each id, and include the counter in the id. There should be a version of it somewhere in this repository. 
