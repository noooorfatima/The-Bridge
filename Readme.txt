Refactored version of the Bridge.

How to test/see changes:
    - Within the bridge-repo directory, type:
        python manage.py runserver 0.0.0.0:8000
    - Going to localhost:8000 in a web browser will now show you the site.

Where to Find CSS/Javascript files:
    - From bridge-repo,
	cd static
    - CSS is in style.css
    - Javascript is in main.js

Where to Find HTML:
    - From bridge-repo,
	cd templates


+How to add new texts to the About page table+

Make sure that The Bridge's about page stays up to date. All entries in it should be sorted alphatebtically, so keep that in mind when you update it.  The about page is called "newabout.html" and its pathway is 
   "bridge-repo/templates/newabout.html"

Comments have been placed in the newabout.html file to show where the table starts and ends. Here are the lines of comments and the table tag that should show the table's start:
           <!--========= TABLE STARTS HERE! ============-->

		<!--==========================================================================-->
		<!--==========================================================================-->
		<!--===== TABLE WITH ALL BRIDGE TEXTS. CONSTANTLY NEEDS TO BE UPDATED.========-->
		<!--==========================================================================-->
		<!--==========================================================================-->		
		<table class="table table-bordered">

And now here are the lines of code that should show the table's end:
   		<!--========= STOP ============-->

		<!--==========================================================================-->
		<!--==========================================================================-->
		<!--======THIS CONCLUDES THE CODE FOR THE TABLE OF BRIDGE TEXTS. =============-->
		<!--==========================================================================-->
		<!--==========================================================================-->
		</table>
Don't go beyond the <table> tags.

There are 4 steps to outline here, but each step is explained more in depth below. 
1. If you have a Greek text to add, find the Greek section. If you have a Latin text, go to the Latin section. Each section is divided by starting and ending <td> tags.
2. Now find the subsection that to enter your text in. The subsection corresponds with what type of text you have.
3. Keep entries in alphabetical order and add your entry. (Note: this step also shows how to use the <a> and <em> tags for linking and italicizing respectively)
4. Be weary of syntactical errors, and other reminders.


1. If you have a Greek text to add, find the Greek section. If you have a Latin text, go to the Latin section. Each section is divided by starting and ending <td> tags.

Here's the Greek column's start...
                <!--================================================================-->
		<!--GREEK TEXTS START HERE==========================================-->
		<!--================================================================-->
		<td valign="top">
		    <h4>Core Lists</h4>

And the Greek column's end..
		<!--===============================================================-->
		<!--STOP! GREEK TEXTS END HERE=====================================-->
		<!--===============================================================-->
            </td>
And below it starts the Latin section. The comments are made in a similar format

2. Find the subsection that you want to update. The subsections specify what type of text you are adding to The Bridge Each section starts and ends with a <ul> and </ul> tag respectively. There is also a header made using the <h4> tag that labels eaach subsection.
The Greek section contains the following subsections: (Greek) Core Lists, (Greek) Textbooks
The Latin section contains the following subsections: (Latin) Core Lists, (Latin) Texts, (Latin) Textbooks

Here is an example of the Latin's Core Lists subsection.
	     <h4>Core Lists</h4>
	        <!-- ______________________________________________________ -->
	        <!-- (Latin) Core Lists -->
		<!--________________________________________________________-->
	     <ul>
		<li><a href="http://dcc.dickinson.edu/latin-vocabulary-list">DCC Latin Core</a></li>
                ...
             </ul>

3. Once you've found the section you need to update, search for where the text would belong in that subsection in alphabetical order then add it.
All bullets (meaning, all individual text entries) within the list start and end with the <li> and </li> tag respectively. Never forget about the opening and closing tags for each entry you make, otherwise the lists within the table will not look right at all.
-    To add some plain text, you would simply need to write
            <li>The name of some text</li>
-    Some entries use italics. For any part that you would like to see in italics, place a <em> tag before the first letter you want italicized and an </em> tag after the last letter you want italicized. Here's an example.
            <li><em>Alpha to Omega </em>(Groton)</li>
"Alpha to Omega" is italicized, but "(Groton)" is not.
-    Some entries turn the text in the table into a hyperlink. These entries are the ones that have blue colored text. If you want to make your text entry into a hyperlink, use the <a> tag with the following attributes:
            <a href="https://yourlinktosomewhere.com">This text is now a hyperlink that will take you to yourlinkesomewhere.com</a>
Here is an example:
            <li><a href="https://camws.org/sites/default/files/ColbyLatin.pdf" >Colby Latin List</a> (Years 1-4, for CAWMS Translation Exams)</li>

4. Remember
-    Most of the tags you'll use will have starting tags and ending tags (ex: <li> and </li>) so remember to open and close these otherwise the page may start concatenating bullets or just look bad.
-    Try to put the entries in alphabetical order.
-    Do not edit already-existing entries in the table.
-    Be weary of any syntactical errors. All tags start with a '<' and '>' but it's pretty easy to forget these. Make sure you close your quotation marks.
-    Want to leave a comment in the html file? Comments will be visible to whoever is writing code for the page, and will not show up on the page. If you have something in mind that could be useful to people updating the about page in the future, leave a comment. A comment starts with '<!--' and ends with '-->'
