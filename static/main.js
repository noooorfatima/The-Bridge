$(document).ready(function() {
    var global_true = true;
//not sure what these two variable do
     var text = ""
    var books = []

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
	//console.log($('#checkbox_inputs :input'));
	$('#checkbox_inputs :input').each(function(i, div){
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
   var divToPrint=document.getElementById("words_generated");
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

/*
//This is where the to/from boxes are generated in the booklist page.
$('#booklist').on("click", function() {
	var my_html = "";
	$('#booklist input').each(function () {
		if($(this).is(':checked')) {
		    console.log(this.value);
		    my_html = my_html + "<label>"+this.value+ " from: <input type=\"text\" name=\""+this.value+" from\" value=\"\" /></label> <label>"+this.value+" to: <input type=\"text\" name=\""+this.value+" to\" value=\"\" /></label> </br>";
		}
	});
	document.getElementById('checkbox_inputs').innerHTML=my_html

});
*/

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
        var selects = document.getElementById('textlist')
        var selectedValue = selects.options[selects.selectedIndex].value
        if (selectedValue == "DCC Latin Core" || selectedValue == "DCC Greek Core" || selectedValue == "Herodotus Book 1 Core (412 words > 10 times)") {
                document.getElementById("core_tip").style.display='block';
		document.getElementById("other_tip").style.display='none';
                }
        else{
                document.getElementById("core_tip").style.display='none';
		document.getElementById("other_tip").style.display='block';
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
	if (document.getElementById("Verbs").checked == true) {
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
        if (document.getElementById("Verbs").checked == true) {
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
        if (document.getElementById("Verbs").checked == true) {
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
        var table_div = document.getElementById('words_generated');
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

    //"#checkAll").click(function () {
    //"input:checkbox").prop('checked', $(this).prop("checked"));
    // });
 

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

});

	

function showTip() {
        var selects = document.getElementById('textlist')
        var selectedValue = selects.options[selects.selectedIndex].value
	//Shows all or selection under textlist
                document.getElementById('all_or_selection').style.display='block';

        if (selectedValue == "DCC Latin Core" || selectedValue == "DCC Greek Core" || selectedValue == "Herodotus Book 1 Core (412 words > 10 times)" && document.getElementById("Selection").checked == true) {
                document.getElementById("core_tip").style.display='block';
		document.getElementById("other_tip").style.display='none';
		$("#core_tip").popover('hide');
                $("#other_tip").popover('hide');


                }
        else if (document.getElementById("Selection").checked==true) {
                document.getElementById("core_tip").style.display='none';
		document.getElementById("other_tip").style.display='block';
		$("#core_tip").popover('hide');
                $("#other_tip").popover('hide');

        }
}

// Makes sure that user selects a target text
function validateText() {
	var selects = document.getElementById('textlist')
        var selectedValue = selects.options[selects.selectedIndex].value
	if (selectedValue == "") {
		return false;
   }
}

// Makes sure that selection input is correct
function validateTextSelect() {
    var x = document.getElementById("text_from").value;
    var y = document.getElementById("text_to").value; 

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
	if(c.value == "All"){  
            document.getElementById("text_selection").style.visibility='hidden'; 
	    document.getElementById("text_from").value = "";
	    document.getElementById("text_to").value = "";
	    document.getElementById("text_from").required = false;
	    document.getElementById("text_to").required = false;
        } else if(c.value =="Selection"){ 
            document.getElementById("text_selection").style.visibility='visible';
	    document.getElementById("text_from").required = true;
	    document.getElementById("text_to").required = true; 
        } else{ 
        }      
}  


// Show/hide text range inputs in a booklist thumbnial.
function selectBookThumbnail(book) {
    var thumbnail = $(".thumbnail[value='"+book+"']")[0];
    var div = $(thumbnail).find(".range_select_box");
    if (div.css("display")=="none") {
        div.show();
        $(thumbnail).css("background","#418CAE");
    }
    else {
        div.hide();
        $(thumbnail).css("background","#FFFFFF");
    }
}


// Shows all or selection for Nouns
function displayFormNoun(c) {
        if (c.checked){
            document.getElementById("noun_box").style.display = 'inline';
        } else {
            document.getElementById("noun_box").style.display = 'none';
            document.getElementById("noun_decl_box").style.display = 'none';
        }
    }

// Shows all or selection for Adjectives
function displayFormAdj(c) {
        if (c.checked) {
            document.getElementById("adj_box").style.display = 'inline';
        } else {
            document.getElementById("adj_box").style.display = 'none';
            document.getElementById("adj_decl_box").style.display = 'none';
        }
    }

// Shows all or selection for Verbs
function displayFormVerb(c) {
        if (c.checked) {
            document.getElementById("verb_box").style.display = 'inline';
        } else {
            document.getElementById("verb_box").style.display = 'none';
	    document.getElementById("verb_conj_box").style.display = 'none';
        }
    }

// Shows declension options for Nouns
function displayFormNounDecl(c) {
        if (c.value == "select_nouns") {
            document.getElementById("noun_decl_box").style.display = 'block';
        } else if (c.value == "all_nouns") {
            document.getElementById("noun_decl_box").style.display = 'none';
        }
    }

// Shows declension options for Adjectives
function displayFormAdjDecl(c) {
        if (c.value == "select_adj") {
            document.getElementById("adj_decl_box").style.display = 'block';
        } else if (c.value == "all_adj") {
            document.getElementById("adj_decl_box").style.display = 'none';
        }
    }

// Shows conjugation options for Verbs
function displayFormVerbConj(c) {
	if (c.value == "all_verbs"){
		document.getElementById("verb_conj_box").style.display = 'none';
	} else if (c.value == "select_verbs"){
		document.getElementById("verb_conj_box").style.display = 'block';
	}
    }

function def_function() {
	if (document.getElementById("No definitions").checked == true) {
		hide_column(3);
		hide_column(4);
	}
	else if (document.getElementById("English-Core Definition").checked == true) {
		hide_column(4);
		show_column(3);
	}
	else if (document.getElementById("English-Extended Definition").checked == true) {
		hide_column(3);
		show_column(4);
	}
}

function greek_def_function() {
        if (document.getElementById("No definitions").checked == true) {
                hide_column(2);
        }
        else if (document.getElementById("English Definition").checked == true) {
                show_column(2);
        }
}

function lemma_function() {
	if (document.getElementById("Dictionary Entry (macron)").checked == true) {
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
            if (!table.nodeType) table = document.getElementById("words_generated")
            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML }

            document.getElementById("dlink").href = uri + base64(format(template, ctx));
            document.getElementById("dlink").download = filename;
            document.getElementById("dlink").click();

        }
    })()

var $table = $('.table');
var $fixedColumn = $table.clone().insertBefore($table).addClass('fixed-column');

$fixedColumn.find('th:not(:first-child),td:not(:first-child)').remove();

$fixedColumn.find('tr').each(function (i, elem) {
    $(this).height($table.find('tr:eq(' + i + ')').height());
});
