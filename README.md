# bridge-repo
Bridge is a tool that allows language learners to make customizable vocabulary lists for what they are reading based on what they have read. We have over 100 Greek and Latin works, ranging from core lists and text books to ancient poetry and scientific texts.

Back-end

Regular Users
As with almost all other Haverford digital scholarship, Bridge uses django. This version is using Django 2.0.6. As with most django projects,
most of the server side computation happens in views.py. The main user views appear in the order that they are called. Useful helper functions
are below the main views. For more on how each view works, read the comments in views.py.
Admin
Most of admin originated as manage.py commands, so the scripts that control importing data are in management/commands. They are well named and
commented. 99% of the time if something went wrong with an import, it was a problem with the data. At the time of writing this (July 2018), there
is a preference for making useful errors appear rather than making the importer handle weird data.

Front-end

Javascript:
We make heavy use of jQuery because it is easier. Anywhere you see $(), we are just calling a jQuery function. Since we changed how the user
interacts with the form, there are still some old, out-dated functions that can probably be safely deleted.
HTML:
If an html file has the name of a view, it is the html for that view. Exceptions:
textlist.html is the landing page
filters.html builds the slide-out panel, and slideout_panel.html builds the filters (I did not do that, someone before me did)
CSS:
Mostly in style.css. No idea how/why/if it works


Known problems & potential future improvements:

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

I customized django autocomplete light, and it still works, but sometimes decides to break. Running collectstatic should bring it back.
Otherwise uninstall, run collectstatic and add a global counter to select2.full.js, which is in autocomplete_light/vendor/select2/dist/js, and make it add to the counter for each id, and include the counter in the id. ids are made around line 5138.

TODO:
Make automated tests.
