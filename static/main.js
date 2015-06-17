//id of currently selected accordion form tab:
var active_form_tab = "tabOne";  

$(document).ready(function() {
    var global_true = true;
//not sure what these two variable do
     var text = ""
    var books = []

/*Monitor for changes in screen width:*/
//set up media query objects:
var mediaQueries = [
    window.matchMedia("screen and (min-width: 320px)"), //very narrow
    window.matchMedia("screen and (max-width: 500px)"),
    window.matchMedia("screen and (min-width: 501px)"), //narrow
    window.matchMedia("screen and (max-width: 700px)"),
    window.matchMedia("screen and (min-width: 701px)"), //medium
    window.matchMedia("screen and (max-width: 1000px)"),
    window.matchMedia("screen and (min-width: 1001px)") //large
    ];

//bind those media query objects to a listener:
for (var i=0; i<mediaQueries.length; i++) {
    handleMediaQuery(mediaQueries[i]); //run once at initialization.
    mediaQueries[i].addListener(handleMediaQuery);  //bind to listener.
}


//This is the spot where we check to make sure there are valid inputs or else the form does not submit on book_select
$("#giant_form_submit").on("click", function(e) {
	listItems = $("#textlist");
	if (validateText() == false) {
	    alert("Please choose a text.");
	    return false;
	}
	if (validateTextSelect() == false){
	    alert("Please submit a valid range.");
	    return false;
	}
	var pairs = [];
    console.log($('.range_select_box :input'));
	$('.range_select_box :input').each(function(i, div){
        var i_over_2 = Math.floor(i / 2);
        if (!pairs[i_over_2]) pairs[i_over_2] = $();
        pairs[i_over_2] = pairs[i_over_2].add(div);
    });
	if (checkbooklist(pairs) == false) {
	    alert("Please submit a valid range.");
	    return false;
	}
});
 
//Function that allows the print button on words page to work
function printData()
{
   var divToPrint=$("#words_generated");
   newWin= window.open("");
   newWin.document.write(divToPrint.outerHTML);
   newWin.print();
   newWin.close();
}
//not sure if this one works
$('#printSubmit').on('click',function(){
printData();
})

$('#tip_button').popover ({
     trigger: 'click'
});

$('.popover-dismiss').popover({
  trigger: 'click'
})

$('#core_tip').popover ({
    trigger: 'click'
});

$('#other_tip').popover ({
    trigger: 'click'
})

$('#booklist_note_button').popover ({
    trigger: 'click'
});

//function that checks full booklist entries
function checkbooklist(list) {
    for (var i=0; i<list.length; i++) {
	if (validateBookSelect(list[i]) == false) {
		return false;
	}
    }
    return true;
}      	

    // For the navbar
    $('.kwicks').kwicks({
        maxSize: "35%",
        autoResize: true,
        spacing: 0,
        duration: 200,
        behavior: 'menu',
        interactive: false,
    });


//Shows the correct tip to choose boxes
$('#Selection').on('click',function(){
        var selects = $('#textlist')
        var selectedValue = selects.val();
        console.log(selectedValue);
        if (selectedValue == "DCC Latin Core" || selectedValue == "DCC Greek Core" || selectedValue == "Herodotus Book 1 Core (412 words > 10 times)") {
                $("#core_tip").css("display","block");
                $("#other_tip").css("display","none");
                }
        else{
                $("#core_tip").css("display","none");
	            $("other_tip").css("display","block");
        }
});

// Filter Function
$('.panel-body input:checkbox').click(function() {
    var panel= $('#filters_panel_body')
    var offset = panel.offset();
    console.log('panel_size',offset)
    var height = panel.height();
    console.log('panel height',height)
    var width = panel.width();
    console.log('panel width',width)
    $('#filters_panel').append('<div id=cover></div>');
    var new_panel = $('#cover');
    new_panel.offset({top:offset.top, left:offset.left});
    new_panel.css("background-color","grey");
    new_panel.css("opacity",".5");
    new_panel.css("height",height);
    new_panel.css("width",width);
    new_panel.css({'cursor':'wait'});
    
    var fin = []; 
    $('.panel-body input:checkbox').each(function() {
        if (!(this.checked)) {
            console.log("Got id: " + $(this).attr("id"))
            fin.push($(this).attr("id")); 
        }   
    }); 
    $('.panel-body input:radio').each(function() {
	if(!(this.checked)) {
            console.log("Got id: " + $(this).attr("id"))
            fin.push($(this).attr("id")); 
        }   
    }); 
	    
    var language = $("#language").text();
    $.post('/filter/'+language+'/', { mine:fin }, function(data){
        console.log(data);
	$('tbody').empty();
	for(var i=0;i<data.words.length;i++) {
	    var string = '<tr id='+i.toString()+'>';
	    string = string +'<td>'+data.words[i].word+'</td>';
	    string = string +'<td>'+data.words[i].definition+'</td>';
	    string = string +'</tr>';
	    $('tbody').append(string);
	}
	$('#cover').remove();
    }); 
});


$("#Verbs").on('click',function() {
	if ($("#Verbs").checked == true) {
		 $('#verb_1st').prop('checked', true);
		 $('#verb_2nd').prop('checked', true);
		 $('#verb_3rd').prop('checked', true);
		 $('#verb_4th').prop('checked', true);
		 $('#irreg_verbs').prop('checked', true);
	}
	else {
		 $('#verb_1st').prop('checked', false);
		 $('#verb_2nd').prop('checked', false);
		 $('#verb_3rd').prop('checked', false);
		 $('#verb_4th').prop('checked', false);
		 $('#irreg_verbs').prop('checked', false);
	}
});			

$("#Nouns").on('click',function() {
        if ($("#Verbs").checked == true) {
                 $('#noun_1st').prop('checked', true);
                 $('#noun_2nd').prop('checked', true);
                 $('#noun_3rd').prop('checked', true);
                 $('#noun_4th').prop('checked', true);
                 $('#noun_5th').prop('checked', true);
		 $('#noun_irreg').prop('checked', true);
        }
	else {
                 $('#noun_1st').prop('checked', false);
                 $('#noun_2nd').prop('checked', false);
                 $('#noun_3rd').prop('checked', false);
                 $('#noun_4th').prop('checked', false);
                 $('#noun_5th').prop('checked', false);
		 $('#noun_irreg').prop('checked', false);
        }
});

$("#Adjectives").on('click',function() {
        if ($("#Verbs").checked == true) {
                 $('#adj_1st').prop('checked', true);
                 $('#adj_3rd').prop('checked', true);
                 $('#adj_defective').prop('checked', true);
        }
	else {
                 $('#adj_1st').prop('checked', false);
                 $('#adj_3rd').prop('checked', false);
                 $('#adj_defective').prop('checked', false);
        }
});

/* //This function not currently being used for export.
    function exportTableToCSV($table, filename) {

        var $rows = $table.find('tr:has(td)'),

            // Temporary delimiter characters unlikely to be typed by keyboard
            // This is to avoid accidentally splitting the actual contents
            tmpColDelim = String.fromCharCode(11), // vertical tab character
            tmpRowDelim = String.fromCharCode(0), // null character

            // actual delimiter characters for CSV format
            colDelim = '","',
            rowDelim = '"\r\n"',

            // Grab text from table into CSV formatted string
            csv = '"' + $rows.map(function (i, row) {
                var $row = $(row),
                    $cols = $row.find('td');

                return $cols.map(function (j, col) {
                    var $col = $(col),
                        text = $col.text();

                    return text.replace('"', '""'); // escape double quotes

                }).get().join(tmpColDelim);

            }).get().join(tmpRowDelim)
                .split(tmpRowDelim).join(rowDelim)
B
                .split(tmpColDelim).join(colDelim) + '"',

B
            // Data URI
            csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);

        $(this)
            .attr({
            'download': filename,
                'href': csvData,
                'target': '_blank'
        });
    }

    // This must be a hyperlink
    $(".export").on('click', function (event) {
        // CSV
        exportTableToCSV.apply(this, [$('#words_generated'), 'export.csv']);
        
        // IF CSV, don't do event.preventDefault() or return false
        // We actually need this to be a typical hyperlink
    });

//This function not currently being used for export.

 $("#excel_export").click(function(e) {
       //getting values of current time for generating the file name
        var dt = new Date();
        var day = dt.getDate();
        var month = dt.getMonth() + 1;
        var year = dt.getFullYear();
        var hour = dt.getHours();
        var mins = dt.getMinutes();
        var postfix = day + "." + month + "." + year + "_" + hour + "." + mins;
        //creating a temporary HTML link element (they support setting file names)
        var a = document.createElement('a');
        //getting data from our div that contains the HTML table
        var data_type = 'data:application/vnd.ms-excel';
        var table_div = $('words_generated');
        var table_html = table_div.outerHTML.replace(/ /g, '%20');
        a.href = data_type + ', ' + table_html;
        //setting the file name
        a.download = 'exported_table_' + postfix + '.xls';
        //triggering the function
        a.click();
        //just in case, prevent default behaviour
        e.preventDefault();
    });
*/

 function exportTableToTSV($table, filename) {

        var $rows = $table.find('tr:has(td)'),

            // Temporary delimiter characters unlikely to be typed by keyboard
            // This is to avoid accidentally splitting the actual contents
            tmpColDelim = String.fromCharCode(11), // vertical tab character
            tmpRowDelim = String.fromCharCode(0), // null character

            // actual delimiter characters for CSV format
            colDelim = '"\t"',
            rowDelim = '"\r\n"',

            // Grab text from table into CSV formatted string
            tsv = '"' + $rows.map(function (i, row) {
                var $row = $(row),
                    $cols = $row.find('td');

                return $cols.map(function (j, col) {
                    var $col = $(col),
                        text = $col.text();

                    return text.replace('"', '""'); // escape double quotes

                }).get().join(tmpColDelim);

            }).get().join(tmpRowDelim)
                .split(tmpRowDelim).join(rowDelim)
                .split(tmpColDelim).join(colDelim) + '"',

            // Data URI
            tsvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(tsv);

        $(this)
            .attr({
            'download': filename,
                'href': tsvData,
                'target': '_blank'
        });
    }

    // This must be a hyperlink
    $(".tab_export").on('click', function (event) {
        // CSV
        exportTableToTSV.apply(this, [$('#words_generated'), 'export.tsv']);
        
        // IF CSV, don't do event.preventDefault() or return false
        // We actually need this to be a typical hyperlink
    });

 

$('#checkAll').click(function() {
        $(".POS").prop("checked",$("#checkAll").prop("checked"));
    });

$('#checkAllExcludes').click(function() {
	$(".Excludes").prop("checked",$("#checkAllExcludes").prop("checked"));
    });

$('#checkAll_greek').click(function() {
        $(".POS").prop("checked",$("#checkAll_greek").prop("checked"));
    });

$('#checkAllExcludes_greek').click(function() {
        $(".Excludes").prop("checked",$("#checkAllExcludes_greek").prop("checked"));
    });


/* EVENT HANDLERS FOR THE GIANT_FORM: */

// Show/hide text range inputs in a booklist thumbnial.
$("#booklist .thumbnail :button").on("click",function() {
    var div = $(this).parent().find(".range_select_box");
    var val = $(this).attr("value");
    if (div.css("display")=="none") {
        //add a hidden checkbox to include this book in the form:
        $('<input>').attr({
            type: 'checkbox',
            checked: "checked",
            class: "hiddencheck",
            name: "book",
            value: val,
            style: "display: none"  
        }).appendTo(this);
        //Show the div:
        div.slideDown(60);
        $(this).parent().css("background","#07325C");
    }
    else {
        div.hide();
        $(this).parent().css("background","#FFFFFF");
        //remove any hidden checkboxes to exclude this book from the form:
        $(".hiddencheck",this).remove();
   }

   // Build a list of selected book titles and insert into panel-contents:
   var headerStr = "";
   var books =  $(".thumbnail :button :input");
   console.log(books.length);
   if (books.length == 1) {
       headerStr = $(books[0]).parent().attr("value");
   }
   else {
       books.each(function() {
           var bookTitle = $(this).parent().attr("value");
           // Shorted book titles to first 7 characters:
           if (bookTitle.length >= 20) {
               headerStr = headerStr + bookTitle.substr(0,20) + "...";
           }
           else {
               headerStr = headerStr + bookTitle+ ", ";
           }
       });
   }
   $("#headingThree .panel-contents").text(headerStr);

   // Hide panel-contents div if empty. Avoids showing a big empty box:
   if (headerStr == "") {
       $("#headingThree .panel-contents").css("display","none");
   }
   else {
       $("#headingThree .panel-contents").css("display","inline-block");
   }

});


//LANGUAGE SELECT BUTTONS:
$("#latin").on("click",{language:"latin"},configureForm);

$("#greek").on("click",{language:"greek"},configureForm);

//TEXT ALL/SELECTION TOGGLE:
$("#all_or_selection").on("click",function(e) {
    displayForm2(e.target);
});

$("#Selection").on("click", function(e) {
    displayForm2(e.target);
});


//ACCORDION FORM TABS:
$("[id^='tab']").on("click", function(e) {
    userFormInteract(e)
});

$("[id^='tab']").on("keyup", function(e) {
    if (e.which == 13) {
        userFormInteract(e);
    }
});

// TEXT SELECT LIST:
$("#textlist").on("click", function() {
    selectedText = $("#textlist").val();
    if ($("#tabTwo .panel-contents").text() != selectedText.text) {
        $("#tabTwo .panel-contents").text(selectedText);
    }
});

});

function handleMediaQuery(mq) {
    /* Reconfigures site appearance based on CSS media queries.
     * mediaQuery objects are declared and bound in $(document).ready.*/ 
    // if "screen and (max-width: 500px)":
    if (/screen and \(max-width:\s*400px\)/.test(mq.media)) {
       console.log("REAL SMALL" + Math.random()); 
    }
    // if "screen and (max-width: 700px)":
    else if (/screen and \(min-width:\s*401px\)/.test(mq.media) || 
            /screen and \(max-width:\s*700px\)/.test(mq.media)) {
        console.log("KINDA SMALL!" + Math.random());
    }
    // if "screen and (max-width: 1000px)":
    else if (/screen and \(min-width:\s*701px\)/.test(mq.media) || 
            /screen and \(max-width:\s*1000px\)/.test(mq.media)) {
        console.log("MIDDLIN\'"+Math.random());
    }
    // if "screen and (min-width: 1001px)":
    else if (/screen and \(min-width:\s*1001px\)/.test(mq.media)) {
        console.log("MERCY!"+Math.random());
    }
}
    

function configureForm(e) {
    var lang = e.data.language;
    // Set the redirect page to the appropriate lang:
    $("#giant_form").attr("action","words_page_redirect/"+lang+"/");
    
    // Configure SOURCE TEXT TAB to only show texts from specified lang:
    var books = $("#textlist").find("[class$='book']");
    books = books.add($("#booklist").find("[class$='bookthumb']"));
    // Hide all text/book elements NOT part of the selected language:
    books.not("[class*='"+lang+"']").css("display","none");
    // Show all which are part of the selected language:
    books.filter("[class*='"+lang+"']").css("display","block");

    //Erase any panel-contents in the SOURCE TEXT TAB:
    $("#headingTwo .panel-contents").text("");

    //Deselect any texts in the READ TEXT TAB: 
    //(selected texts have a checkbox :input child to their :button)
    $(".thumbnail :button :input").each(function() {
        thumbnail = $(this).parent().parent()
        // Remove the hidden checkbox:
        $(".hiddencheck",this).remove();
        //Hide range select box:
        thumbnail.css("background","#FFFFFF");
        thumbnail.find(".range_select_box").css("display","none");
    });

    //Modify language select accordion tab to reflect selected lang.:
    $("#headingOne .panel-title").css("text-align","left");
    //capitalize language and att it to lang select tab: 
    $("#headingOne .panel-contents").text(lang.charAt(0).toUpperCase() +
            lang.slice(1));

    switchFormTabs($("#tabOne"),$("#tabTwo"));

    // Make the text select accordion tab expand+collapsible: 
    $("#tabThree").attr("data-toggle","collapse");
    $("#tabTwo").attr("data-toggle","collapse");
}

function userFormInteract(e) {
    var clickedTab = $(e.target).parents("[id^='tab']");
    if ((clickedTab.attr("id") != active_form_tab) &&
        ($("#giant_form").attr("action") != "")) {
            switchFormTabs($("#"+active_form_tab),clickedTab);
        }
    else {
        console.log("PLEASE SELECT A LANGUAGE FIRST!");
        $("headingOne").animate({
            opacity: 0.25
        },1000,function(){});
    }
}

function switchFormTabs(current, next) {
    /* Formats and hides/shows accordion tabs in the main form.
     *
     * current and next are both <a> elements, the clickable part of an 
     *  accordion tab.
     */
    
    //Change current's tab header to look "inactive", and COLLAPSE it:
    current.find(".panel-heading").css("background-color","#FFFFFF");
    current.find(".panel-title").css("color","#428BCA");
    current.find(".panel-contents").css("color","#428BCA");
    current.find(".panel-contents").css("border","1px solid #428BCA");
    current.siblings(".collapse").collapse("hide");
    
    //Change next's tab header to look "active", and EXPAND it:
    next.find(".panel-heading").css("background-color","#07325C");
    next.find(".panel-title").css("color" , "#F1F1F1");
    next.find(".panel-contents").css("color","#F1F1F1");
    next.find(".panel-contents").css("border","1px solid #F1F1F1");
    next.siblings(".collapse").collapse("show");
    
    //Reflect this change in the active form tracking variable:
    active_form_tab = next.attr("id");
}
	

function showTip() {
        var selects = $('textlist');
        var selectedValue = selects.val();
	//Shows all or selection under textlist
                $('#all_or_selection').css("display","block");

        if (selectedValue == "DCC Latin Core" || selectedValue == "DCC Greek Core" || selectedValue == "Herodotus Book 1 Core (412 words > 10 times)" && $("#Selection").checked == true) {
                $("#core_tip").css("display","block");
		$("#other_tip").css("display","none");
		$("#core_tip").popover('hide');
                $("#other_tip").popover('hide');
                }
        else if ($("#Selection").checked==true) {
                $("#core_tip").css("display","none");
		$("#other_tip").css("display","block");
		$("#core_tip").popover('hide');
                $("#other_tip").popover('hide');

        }
}

// Makes sure that user selects a target text
function validateText() {
	var selects = $('textlist')
        var selectedValue = selects.val();
	if (selectedValue == "") {
		return false;
   }
}

// Makes sure that selection input is correct
function validateTextSelect() {
    var x = $("#text_from").value;
    var y = $("#text_to").value; 

    if (x[0] == "." || y[0] == "."){
	return false;
    }
    //if (x.split(".").length != y.split(".").length){
        //return false;
    //}
    else if (x.split(".").length > 3 || y.split(".").length > 3){
	return false;
    }
    else if (x.split(".")[0] > y.split(".")[0]){
        return false;
    }
    else if (x.split(".")[0] == y.split(".")[0]){
         if (x.split(".")[1] > y.split(".")[1]){
		return false;
         }
         else if (x.split(".")[1] == y.split(".")[1]){
	 	if (x.split(".")[2] > y.split(".")[2]){
			return false;
    }}}
}

// Makes sure that selection input is correct
function validateBookSelect(a) {
    var x = a[0].value;
    var y = a[1].value;

    if (x[0] == "." || y[0] == "."){
        return false;
    }
    if (x.split(".").length != y.split(".").length){
        return false;
    }
    else if (x.split(".").length > 3){
        return false;
    }
    else if (parseInt(x.split(".")[0]) > parseInt(y.split(".")[0])){
        return false;
    }
    else if (parseInt(x.split(".")[0]) == (parseInt(y.split(".")[0]))){
         if (parseInt(x.split(".")[1]) > parseInt(y.split(".")[1])){
                return false;
         }
         else if ((parseInt(x.split(".")[1]) == parseInt(y.split(".")[1]))){
                if (parseInt(x.split(".")[2]) > parseInt(y.split(".")[2])){
                        return false;
    }}}
}

// Only allows numbers and periods to be entered in the selection fields
function isNumberKey(evt)
      {
         var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)){
            return false;
         }
         else{
	    return true;
	 }
      }

// Displays all or selection for textlist
function displayForm2(c){ 
    var btnText = $(c).attr("value");
	if(btnText == "All"){  
        $("#text_selection").slideUp(60);
        $("text_from").val("");
        $("text_to").val("");
        $("text_from").required = false;
        $("#text_to").required = false;
        }
    else if(btnText =="Selection") {
        $("#text_selection").slideDown(60);
	    $("#text_from").required = true;
	    $("#text_to").required = true; 
        } 
    else{ }      
}  


// Shows all or selection for Nouns
function displayFormNoun(c) {
        if (c.checked){
            $("#noun_box").css("display","inline");
        } else {
            $("#noun_box").css("display","none");
            $("#noun_decl_box").css("display","none");
        }
    }

// Shows all or selection for Adjectives
function displayFormAdj(c) {
        if (c.checked) {
            $("#adj_box").css("display","inline");
        } else {
            $("#adj_box").css("display","none");
            $("#adj_decl_box").css("display","none");
        }
    }

// Shows all or selection for Verbs
function displayFormVerb(c) {
        if (c.checked) {
            $("#verb_box").css("display","inline");
        } else {
            $("#verb_box").css("display","none");
	    $("#verb_conj_box").css("display","none");
        }
    }

// Shows declension options for Nouns
function displayFormNounDecl(c) {
        if (c.value == "select_nouns") {
            $("#noun_decl_box").css("display","block");
        } else if (c.value == "all_nouns") {
            $("#noun_decl_box").css("display","none");
        }
    }

// Shows declension options for Adjectives
function displayFormAdjDecl(c) {
        if (c.value == "select_adj") {
            $("#adj_decl_box").css("display","block");
        } else if (c.value == "all_adj") {
            $("#adj_decl_box").css("display","none");
        }
    }

// Shows conjugation options for Verbs
function displayFormVerbConj(c) {
	if (c.value == "all_verbs"){
		$("#verb_conj_box").css("display","none");
	} else if (c.value == "select_verbs"){
		$("#verb_conj_box").css("display","block");
	}
    }

function def_function() {
	if ($("#No definitions").checked == true) {
		hide_column(3);
		hide_column(4);
	}
	else if ($("#English-Core Definition").checked == true) {
		hide_column(4);
		show_column(3);
	}
	else if ($("#English-Extended Definition").checked == true) {
		hide_column(3);
		show_column(4);
	}
}

function greek_def_function() {
        if ($("#No definitions").checked == true) {
                hide_column(2);
        }
        else if ($("#English Definition").checked == true) {
                show_column(2);
        }
}

function lemma_function() {
	if ($("#Dictionary Entry (macron)").checked == true) {
		hide_column(2);
		show_column(1);
	}
	else {
		hide_column(1);
		show_column(2);
	}
}


function hide_column(a){
                // if your table has header(th), use this
                $("#words_generated tbody td:nth-child("+a+")").hide();
		$("#words_generated thead th:nth-child("+a+")").hide();
            }

function show_column(b){
                // if your table has header(th), use this
                $("#words_generated tbody td:nth-child("+b+")").show();
		$("#words_generated thead th:nth-child("+b+")").show();
            }


$('#backToTopBtn').click(function(){
        $('html,body').animate({scrollTop:0},'slow');return false;
    });


var tableToExcel = (function () {
        var uri = 'data:application/vnd.ms-excel;base64,'
        , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
        , base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))) }
        , format = function (s, c) { return s.replace(/{(\w+)}/g, function (m, p) { return c[p]; }) }
        return function (table, name, filename) {
            if (!table.nodeType) table = $("#words_generated")
            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML }

            $("#dlink").href = uri + base64(format(template, ctx));
            $("#dlink").download = filename;
            $("#dlink").click();

        }
    })()

var $table = $('.table');
var $fixedColumn = $table.clone().insertBefore($table).addClass('fixed-column');

$fixedColumn.find('th:not(:first-child),td:not(:first-child)').remove();

$fixedColumn.find('tr').each(function (i, elem) {
    $(this).height($table.find('tr:eq(' + i + ')').height());
});
