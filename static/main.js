$(document).ready(function() {
    var global_true = true;
/*
    var language = ""
    $("#langselect").on("click", function(e) {
	e.preventDefault();
	if ($('#latin').is(':checked')) {
		language = "latin"
	}
	else if ($('#greek').is(':checked')) {
		language = "greek";
	}
	var sendObj = {
		"language": language
	};
	//	$.post('/language_select/', sendObj, function(response) {
		
//	});
    });
*/
//not sure what these two variable do
     var text = ""
    var books = []


//This is the spot where we check to make sure there are valid inputs or else the form does not submit on book_select
    $("#giant_form_submit").on("click", function(e) {
	listItems = $("#textlist");
	if (validateText() == false) {
		alert("Please choose a text.");
		return false;
	if (validateTextSelect() == false){
		alert("Please submit a valid range.");
		return false;
	}
	var pairs = [];
	console.log($('#checkbox_inputs :input'));
        $('#checkbox_inputs :input').each(function(i, div){
        var i_over_2 = Math.floor(i / 2);
        if (!pairs[i_over_2]) pairs[i_over_2] = $();
                pairs[i_over_2] = pairs[i_over_2].add(div);
	});
	if (checkbooklist(pairs) == false) {
	  alert("Please submit a valid range.");
	  return false;
	}
    }}
);
 
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
//This is where the to/from boxes are generated in the booklist page.
    $('#booklist').on("click", function() {
	var my_html = "";
	$('#booklist input').each(function () {
	    if($(this).attr('type')=="checkbox") {
		if($(this).is(':checked')) {
		    console.log(this.value);
		    my_html = my_html + "<label>"+this.value+ " from: <input type=\"text\" name=\""+this.value+" from\" value=\"\" onkeypress=\"return isNumberKey(event)\"/></label> <label>"+this.value+" to: <input type=\"text\" name=\""+this.value+" to\" value=\"\" onkeypress=\"return isNumberKey(event)\" /></label> </br>";
  	    		}		
		}
	});
	document.getElementById('checkbox_inputs').innerHTML=my_html

   });

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
//I will comment on the POS and the verb conj.  The noun and Adj declensions are similar to verb conj so I will not comment as heavily on those.

function showSpinner() {
//Create the Spinner with options
	var spinner = new Spinner({
        	lines: 12, // The number of lines to draw
        	length: 7, // The length of each line
        	width: 5, // The line thickness
        	radius: 10, // The radius of the inner circle
        	color: '#000', // #rbg or #rrggbb
        	speed: 1, // Rounds per second
        	trail: 100, // Afterglow percentage
        	shadow: true // Whether to render a shadow
        }).spin(document.getElementById("container2")); // Place in DOM node called "ajaxContentHolder"
}

/*$('.container2').click(function() {
	//showSpinner();
	filters2();
	//filters3();
});*/

function filters2() {

        var my_list = [];
        var values = [];
        var verb_list = [];
        var conj_vals = [];
        var noun_list = [];
        var noun_vals = [];
        var adj_list = [];
        var adj_vals = [];

        //go through each checkbox (visible or invisible)
        $('.container2 input').each(function() {
            //If it is unchecked it adds it to the list
            if ($(this).attr('name') == "POS" && !($(this).is(':checked'))) {
                var unchecked = $(this).attr('value').slice(0, -1); //this slice takes off the s so Adjectives becomes Adjective
                console.log(unchecked);
                my_list.push(unchecked);
            }
            //Only if select Verbs is checked
            if ($("#select_verbs").is(':checked')) {
                if ($(this).attr('name') == "conj_select" && !($(this).is(':checked'))) {
                    var verb_unchecked = parseInt($(this).attr('value').slice(5,6));
                    console.log(verb_unchecked);
                    verb_list.push(verb_unchecked);
                }
            }
            if ($("#select_nouns").is(':checked')) {
                if ($(this).attr('name') == "noun_decl" && !($(this).is(':checked'))) {
                    var noun_unchecked = parseInt($(this).attr('value').slice(5,6));
                    console.log(noun_unchecked);
                    noun_list.push(noun_unchecked);
                }
            }
            if ($("#select_adj").is(':checked')) {
                if ($(this).attr('name') == "adj_decl" && !($(this).is(':checked'))) {
                    var adj_unchecked = parseInt($(this).attr('value').slice(4,5));
                    console.log(adj_unchecked);
                    adj_list.push(adj_unchecked);
                }
            }
        });

	var idioms_list = [];
        var idioms_vals = [];
        var numbers_list = [];
        var numbers_vals =[];
        var proper_list = [];
        var proper_vals = [];
        var reg_adv_list = [];
        var reg_adv_vals = [];
		
	//go through each checkbox in container3
        $('.container3 input').each(function() {
            //If it is unchecked it adds it to the list
            if ($(this).attr('name') == "Idioms" && !($(this).is(':checked'))) {
                var idioms_unchecked = $(this).attr('value').slice(0, -1); //this slice takes off the s so Adjectives becomes Adjective
                console.log(idioms_unchecked);
                idioms_list.push(idioms_unchecked);
            }
            if ($(this).attr('name') == "Numbers" && !($(this).is(':checked'))) {
                var numbers_unchecked = $(this).attr('value');
                console.log(numbers_unchecked);
                numbers_list.push(numbers_unchecked);
            }
            if ($(this).attr('name') == "Proper nouns" && !($(this).is(':checked'))) {
                var proper_unchecked = $(this).attr('value');
                console.log(proper_unchecked);
                proper_list.push(proper_unchecked);
            }
            if ($(this).attr('name') == "Reg_Adv" && !($(this).is(':checked'))) {
                var reg_adv_unchecked = $(this).attr('value');
                console.log(reg_adv_unchecked);
                reg_adv_list.push(reg_adv_unchecked);
            }
        });
		
		//for container2
        $("#words_generated tbody td:nth-child(2)").each(function() {
                values.push(this.innerHTML.split(","));
        });
        $("#words_generated tbody td:nth-child(5)").each(function() {
                conj_vals.push(parseInt(this.innerHTML));
        });
        $("#words_generated tbody td:nth-child(6)").each(function() {
                noun_vals.push(parseInt(this.innerHTML));
        });
        $("#words_generated tbody td:nth-child(6)").each(function() {
                adj_vals.push(parseInt(this.innerHTML));
        });

		//for container3
	$("#words_generated tbody td:nth-child(2)").each(function() {
                idioms_vals.push(this.innerHTML.split(","));
        });
        $("#words_generated tbody td:nth-child(7)").each(function() {
                numbers_vals.push(this.innerHTML);
        });
        $("#words_generated tbody td:nth-child(8)").each(function() {
                proper_vals.push(this.innerHTML);
        });
        $("#words_generated tbody td:nth-child(9)").each(function() {
                reg_adv_vals.push(this.innerHTML);
        });

        for (var i=0; i<values.length; i++) {
                var num_of_pos = values[i].length
                for (var j=0; j < num_of_pos; j++) {
                        if (my_list.indexOf(values[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        } 
			else if (idioms_list.indexOf(idioms_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
                        else if (numbers_list.indexOf(numbers_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
                        else if (proper_list.indexOf(proper_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
                        else if (reg_adv_list.indexOf(reg_adv_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
			else {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').show();
                        }
                  }
        }
        // This will go through verb conj lists and hide and show
        for (var i=0; i<=conj_vals.length; i++) {
            if (verb_list.indexOf(conj_vals[i]) >=0 && $("#Verbs").is(":checked")) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html()=="Verb") {
                    $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                }
            } else {
                if ($("#Verbs").is(":checked")) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() =="Verb") {
                $('#words_generated tbody tr:nth-child('+(i+1)+')').show();
                }
            }
            }
        }
        //This will go through noun decl lists and hide and show
        for (var i=0; i<=noun_vals.length; i++) {
            if (noun_list.indexOf(noun_vals[i]) >=0) {
                if ($("#Nouns").is(':checked')) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() == "Noun") {
                    $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                }
                }
            } else {
                if ($("#Nouns").is(':checked')) {
                if ($("words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html == "Noun") {
                    $("#words_generated tbody tr:nth-child("+(i+1)+")").show();
                }
                }
            }
        }

        for (var i=0; i<=adj_vals.length; i++) {
            if (adj_list.indexOf(adj_vals[i]) >=0) {
                if ($("#Adjectives").is(':checked')) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() == "Adjective") {
                    $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                }
                }
            } else {
                if ($("#Adjectives").is('checked')) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() == "Adjective") {
                    $("#words_generated tbody tr:nth-child("+(i+1)+")").show();
                }
            }
                }
        }
   };


/*$('.container2_greek').click(function() {
        //showSpinner();
        filters2_greek();
});*/

$('.panel-body input:checkbox').click(function() {
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
    }); 
});

function filters2_greek() {
        var my_list = [];
        var values = [];
        var verb_list = [];
        var conj_vals = [];
        var noun_list = [];
        var noun_vals = [];
        var adj_list = [];
        var adj_vals = [];
        //go through each checkbox (visible or invisible)
        $('.container2_greek input').each(function() {
            //If it is unchecked it adds it to the list
            if ($(this).attr('name') == "POS" && !($(this).is(':checked'))) {
                var unchecked = $(this).attr('value').slice(0, -1); //this slice takes off the s so Adjectives becomes Adjective
                console.log(unchecked);
                my_list.push(unchecked);
            }
            //Only if select Verbs is checked
            if ($("#select_verbs").is(':checked')) {
                if ($(this).attr('name') == "conj_select" && !($(this).is(':checked'))) {
                    var verb_unchecked = parseInt($(this).attr('value').slice(5,6));
                    console.log(verb_unchecked);
                    verb_list.push(verb_unchecked);
                }
            }
            if ($("#select_nouns").is(':checked')) {
                if ($(this).attr('name') == "noun_decl" && !($(this).is(':checked'))) {
                    var noun_unchecked = parseInt($(this).attr('value').slice(5,6));
                    console.log(noun_unchecked);
                    noun_list.push(noun_unchecked);
                }
            }
            if ($("#select_adj").is(':checked')) {
                if ($(this).attr('name') == "adj_decl" && !($(this).is(':checked'))) {
                    var adj_unchecked = parseInt($(this).attr('value').slice(4,5));
                    console.log(adj_unchecked);
                    adj_list.push(adj_unchecked);
                }
            }
        });
		
	var idioms_list = [];
        var idioms_vals = [];
        var numbers_list = [];
        var numbers_vals =[];
        var proper_list = [];
        var proper_vals = [];
        var reg_adv_list = [];
        var reg_adv_vals = [];

        //go through each checkbox in container3)
        $('.container3_greek input').each(function() {
            //If it is unchecked it adds it to the list
            if ($(this).attr('name') == "Idioms" && !($(this).is(':checked'))) {
                var idioms_unchecked = $(this).attr('value').slice(0, -1); //this slice takes off the s so Adjectives becomes Adjective
                console.log(idioms_unchecked);
                idioms_list.push(idioms_unchecked);
            }
            if ($(this).attr('name') == "Numbers" && !($(this).is(':checked'))) {
                var numbers_unchecked = $(this).attr('value');
                console.log(numbers_unchecked);
                numbers_list.push(numbers_unchecked);
            }
            if ($(this).attr('name') == "Proper nouns" && !($(this).is(':checked'))) {
                var proper_unchecked = $(this).attr('value');
                console.log(proper_unchecked);
                proper_list.push(proper_unchecked);
            }
            if ($(this).attr('name') == "Reg_Adv" && !($(this).is(':checked'))) {
                var reg_adv_unchecked = $(this).attr('value');
                console.log(reg_adv_unchecked);
                reg_adv_list.push(reg_adv_unchecked);
            }
        });
		
		// for container2's checkboxes
        $("#words_generated tbody td:nth-child(2)").each(function() {
                values.push(this.innerHTML.split(","));
        });
        $("#words_generated tbody td:nth-child(5)").each(function() {
                conj_vals.push(parseInt(this.innerHTML));
        });
        $("#words_generated tbody td:nth-child(4)").each(function() {
                noun_vals.push(parseInt(this.innerHTML));
        });
        $("#words_generated tbody td:nth-child(4)").each(function() {
                adj_vals.push(parseInt(this.innerHTML));
        });
		
		//for container3's checkboxes
	$("#words_generated tbody td:nth-child(2)").each(function() {
                idioms_vals.push(this.innerHTML.split(","));
        });
        $("#words_generated tbody td:nth-child(2)").each(function() {
                numbers_vals.push(this.innerHTML.split(","));
        });
        $("#words_generated tbody td:nth-child(5)").each(function() {
                proper_vals.push(this.innerHTML);
        });
        $("#words_generated tbody td:nth-child(6)").each(function() {
                reg_adv_vals.push(this.innerHTML);
        });
		
        for (var i=0; i<values.length; i++) {
                var num_of_pos = values[i].length
                for (var j=0; j < num_of_pos; j++) {
                        if (my_list.indexOf(values[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        } 
			else if (idioms_list.indexOf(idioms_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
                        else if (numbers_list.indexOf(numbers_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
                        else if (proper_list.indexOf(proper_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
                        else if (reg_adv_list.indexOf(reg_adv_vals[i][j]) >= 0) {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                        }
			else {
                            $('#words_generated tbody tr:nth-child('+(i+1)+')').show();
                        }
                  }
        }
        // This will go through verb conj lists and hide and show
        for (var i=0; i<=conj_vals.length; i++) {
            if (verb_list.indexOf(conj_vals[i]) >=0 && $("#Verbs").is(":checked")) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html()=="Verb") {
                    $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                }
            } else {
                if ($("#Verbs").is(":checked")) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() =="Verb") {
                $('#words_generated tbody tr:nth-child('+(i+1)+')').show();
                }
            }
            }
        }
        //This will go through noun decl lists and hide and show
        for (var i=0; i<=noun_vals.length; i++) {
            if (noun_list.indexOf(noun_vals[i]) >=0) {
                if ($("#Nouns").is(':checked')) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() == "Noun") {
                    $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                }
                }
            } else {
                if ($("#Nouns").is(':checked')) {
                if ($("words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html == "Noun") {
                    $("#words_generated tbody tr:nth-child("+(i+1)+")").show();
                }
                }
            }
        }

        for (var i=0; i<=adj_vals.length; i++) {
            if (adj_list.indexOf(adj_vals[i]) >=0) {
                if ($("#Adjectives").is(':checked')) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() == "Adjective") {
                    $('#words_generated tbody tr:nth-child('+(i+1)+')').hide();
                }
                }
            } else {
                if ($("#Adjectives").is('checked')) {
                if ($("#words_generated tbody tr:nth-child("+(i+1)+") td:nth-child(2)").html() == "Adjective") {
                    $("#words_generated tbody tr:nth-child("+(i+1)+")").show();
                }
            }
                }
        }
   };


/*$('.container3').click(function() {
        //showSpinner();
	filters2();
});*/


/*$('.container3_greek').click(function() {
        //showSpinner();
        filters2_greek();
});*/


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

	

function show_tip() {
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

// Shows notes under booklist
function show_booklist_notes() {
	$("#booklist input").each(function() {
		if ($( this ).is(":checked")) {
			document.getElementById("booklist_notes").style.display="block";
			return false;
		}
		else {
			document.getElementById("booklist_notes").style.display="none";
		}
	});
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
                hide_column(3);
        }
        else if (document.getElementById("English Definition").checked == true) {
                show_column(3);
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
