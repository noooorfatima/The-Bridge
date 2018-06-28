# bridge-repo
Refactored version of the Bridge: Now using python 3.5 instead of 2.7!

The broad problem: given two sets of words, find either their intersection or difference. 
  The crucial sub-problem: get the correct two sets of words. 
How we solved it:
HOW TEXTS ARE STORED
Texts, word lists, and text books are broken down into materialzed path trees using treebeard. The trees store location data in a variable called “mindiv.” For example, we humans think of book one paragraph one line one of the Gallic wars as section 1.1.1, but bridge thinks of it as 0.
We can then use mindivs to filter database queries, and return the words in the right mindiv range of the right text. 

The filters use javascript, and so does adding new input boxes to texts to exclude/include. 
The html is in new_bridge/templates, the javascript and css are both in static. 
