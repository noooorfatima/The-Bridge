//*****************************************************************************************************/
/* NOTE
 * Date: 7/6/17
 * As of today, people who are working on this project should be aware that this javascript file
 * among new ones that have been briefly made and tested, RUN THEMSELVES TWO TIMES.
 * So the following code creates a global namespace called "namesp" and a function called isFirstLoad.
 * Then the first conditional calls isFirstLoad to make sure that this is the first time this javascript
 * file has been loaded. To learn more about how this works, visit
 * https://blog.michaelckennedy.net/2012/10/11/preventing-javascript-files-from-loading-multiple-times/
 * If you delete this code, then Javascript should return to running twice. Addiitionally, one of the most
 * important problems with this is when you generate a vocabulary list, page, an alert message appears
 * saying something along the lines of "error, cannot reinitialise data tables." 
 ****************************************************************************************************/


/*switching the buttons. Check configureForm. There's some rather odd behavior with that.*/




var namesp = namesp || {};
var isFirstLoad = function(namesp) {
   var isFirst = namesp.firstLoad === undefined;
   //console.log("isFirst is: " + isFirst);
   namesp.firstLoad = false;
   if (!isFirst) {
       //console.log("warning, this file has been loaded more than once.");
    }
   return isFirst;
 };



var iter = 0;
var globalLang = "";
var dontRunTwice = true;
var itercheck=0;
var forms_are_visible = false;
//var iter2 = 0;
//var iter3 = 0;
//iter3 = iter3 + 1
//console.log("iter 3 value: " + iter3);

$(document).ready(function() {
    if (!isFirstLoad(namesp)) {
    //console.log("this conditional was activated");
    //throw new Error("something went wrong");
    return;
 } else {
    //console.log(isFirstLoad(namesp));
    //console.log("failure to identify isFirstLoad as false");
  }   

    //console.log("iter 2: " + iter2);
    // Set up fancy nav bar resizing:
    $('.kwicks').kwicks({
        maxSize: "35%",
    autoResize: true,
    spacing: 0,
    duration: 200,
    behavior: 'menu',
    interactive: false,
    });

    /*===================== Event bindings for INDEX.HTML ===================*/
    if ($("body").data("title") === "index") {

        $("#giant_form")[0].reset(); // Clear form contents on reload

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
        for (var i = 0; i < mediaQueries.length; i++) {
            handleMediaQuery(mediaQueries[i]); //run once at initialization.
            mediaQueries[i].addListener(handleMediaQuery); //bind to listener.
        }


        //Validate form data:
      $("#giant_form_submit").on("click", function(e) {
	    var key = true;
            var selectedValue = "";
            if($("#tabTwo .panel-contents").text()) {
                selectedValue = $("#tabTwo .panel-contents").text();
            } 
           /* $("#dropDownDiv select").each(function() {
                if ($(this).attr("display") == "none") {
                   console.log($(this).attr("id"));
                   $(this).attr("name", "");
                }
            });*/
            if (selectedValue == "") {
                alert("Please choose a text.");
                return false;
            }
            if ($("#text_from,#text_to").is(":visible")) {
		    if (validateTextSelect() == false) {
		        alert("Please submit a valid range.");
		        return false;
		    }};
            var pairs = []
            //console.log($('.range_select_box input'));
            $('.range_select_box').each(function() {
		var new_tuple = []
                $('input:visible', this).each(function(index, value) {
			//console.log(value.value);
			new_tuple.push(value.value);
		});
		pairs.push(new_tuple);
		//var text 
		//text = document.getElementsByClass("text_name");
		//console.log(text);
		for (var i=0; i<pairs.length; i++) {
		    //var text_array
		    //console.log(pairs);
		    //pairs[i].push(text[i])
		    if (pairs[i][0] != "") {
		        if (pairs[i][1] == "") {
		            key = false;
			    return false;
		        }
	            } else if (pairs[i][1] != "") {
		        if (pairs[i][0] == "") {
		            key = false;
			    return false;
		        }
	            } else if (pairs[i][0] == "" && pairs[i][1] == "") {
		        key = false
			return false;
                    }
                    if (checkbooklist(pairs[i]) == false) {
                        key = false;
			return false;
                    }
	        }
        })
		if (key==false) {
			alert("Please enter a valid range");
			return false;
		}
});

        $('#tip_button').popover({
            trigger: 'click'
        });

        $('.popover-dismiss').popover({
            trigger: 'click'
        });

        $('#core_tip').popover({
            trigger: 'click'
        });

        $('#other_tip').popover({
            trigger: 'click'
        });

        $('#booklist_note_button').popover({
            trigger: 'click'
        });

        //function that checks full booklist entries
        function checkbooklist(list) {
            for (var i = 0; i < list.length; i++) {
                if (validateBookSelect(list[i]) == false) {
                    return false;
                }
            }
            return true;
        }

        //Shows the correct tip to choose boxes
       /* $('#Selection').on('click', function() {
            var selects = $('#textlist');
            var selectedValue = selects.val();
            console.log(selectedValue); */
           /* if (selectedValue == "DCC Latin Core" ||
                selectedValue == "DCC Greek Core" ||
                selectedValue ==
                "Herodotus Book 1 Core (412 words > 10 times)") {
                $("#core_tip").css("display", "block");
                $("#other_tip").css("display", "none");
            } else {
                $("#core_tip").css("display", "none");
                $("other_tip").css("display", "block");
            } */
       // });

        /* EVENT HANDLERS FOR THE GIANT_FORM: */

        // Show/hide range select TOGGLE in a booklist thumbnail:
        //click is bound twice to these so I unbounded first
        //Really a fine solution, but also kind of a hack
        $("#booklist .thumbnail :button").unbind("click").on("click", function() {
           /***************************************************************/
           // onClick handler for the button thumbnails in exclude/include section
          /***************************************************************/
            var div = $(this).parent().find(
                ".range-select-toggle");
            if (div.css("display") == "none") {
                div.slideDown(100);
                $(this).children().css("white-space", "normal");
                /*div.slideUp(30, function() {
                  div.css("white-space", "normal");
                });*/
                $(this).parent().css("border",
                    "3px solid #07315B");
                //add a hidden checkbox to include this book in the form:
                var val =
                    $('<input>').attr({
                        type: 'checkbox',
                        checked: "checked",
                        class: "hiddencheck",
                        name: "book",
                        value: $(this).attr("value"),
                        style: "display: none"
                    }).appendTo(this);
            } else {
                div.slideUp(100, function() {
                    $(this).parent().css("border",
                        "1px solid #ccc");
                });
                /*div.slideDown(30, function() {
                    div.css("white-space", "nowrap");
                });*/
                $(this).children().css("white-space", "nowrap");
                //remove any hidden checkboxes to exclude this book from the form:
                $(".hiddencheck", this).remove();
            }
            
            // Build a list of selected book titles and insert into panel-contents:
            var headerStr = "";
            var books = $(".thumbnail :button input");

            if (books.length == 1) {
                headerStr = $(books[0]).parent().attr("value");
            } else {
                books.each(function() {
                    var bookTitle = $(this).parent().attr(
                        "value");
                    // Shorted book titles to first 7 characters:
                    /*if (bookTitle.length >= 20) {
                        headerStr = headerStr +
                            bookTitle.substr(0, 20) +
                            "...,";
                    } else {
                        headerStr = headerStr +
                            bookTitle + ", ";
                    }*/
                  headerStr = headerStr + bookTitle + ", "; //each is added to headerrStr and separated by a comma and space.
                });
            } 
            //headerStr = headerStr.substr(0, headerStr.length -
              //  4); //rmv trailing "...,"
             //^the above was written becaue previously, each title was separated by '...'
            $("#headingThree .panel-contents").text(headerStr);

            // Hide panel-contents div if empty. Avoids showing a big empty box:
            if (headerStr == "") {
                $("#headingThree .panel-contents").css(
                    "display", "none");
            } else {
                $("#headingThree .panel-contents").css(
                    "display", "inline-block");
            }

        });

        //Show/hide range select FIELDS in a booklist thumbnail:
        $(".range-select-toggle .btn-group").on("click", function(e) {
            var clicked = $(e.target);
            //Only do something if inactive button is clicked:
            if (clicked.attr("class").indexOf("active") === -1) {
                var thumbnail = clicked.parents(".thumbnail");
                //console.log(clicked.attr("val"));
                if (clicked.attr("value") === "Selection") {
                    console.log(thumbnail.find(
                        ".range_select_box"));
                    thumbnail.find(".range_select_box").slideDown(
                        100);
                } else {
                    thumbnail.find(".range_select_box").slideUp(
                        100);
                }
            }
        });

        //LANGUAGE SELECT BUTTONS:
        $("#latin").on("click", {
            language: "latin"
        }, configureForm);

        // Viewport size was a big issue this is a hack around it to get
        // the background to look all nice at first and then for the window
        // to be sized appropriately

        $("#latin").on("click", function () {
            $("html").css("height","auto");
        });

        $("#greek").on("click", {
            language: "greek"
        }, configureForm);
        // Same as with latin
        $("#greek").on("click", function () {
            $("html").css("height","auto");
        });

        $(".intro-text").on("click", function() {
           $(".intro-text").css("color", "#FFF");
           //if(!$("#collapseOne").hasClass("in")) {
              
         });

        //TEXT ALL/SELECTION TOGGLE:
        $("#all_or_selection").on("click", function(e) {
            displayForm2(e.target);
        });

        /*$("#Selection").on("click", function(e) {
            displayForm2(e.target);
        });*/

        //READ TEXT INCLUDE/EXCLUDE TOGGLE:
        $("#include_or_exclude .btn-group").on("click", function(e) {
            var clicked = $(e.target);
            //Only do something if inactive button is clicked:
            if (clicked.attr("class").indexOf("active") === -1) {
                //Extract "Includ" or "Exclud" from button text:
                var text = clicked.text().trim().substr(0, 6) +
                    "ing words from:";
                $("#headingThree .panel-title").text(text);
            }
        });

        //ACCORDION FORM TABS:
        $("[id^='tab']").on("click", function(e) {
            userFormInteract(e);
        });

        $("[id^='tab']").on("keyup", function(e) {
            if (e.which == 13) {
                userFormInteract(e);
            }
        });

        // TEXT SELECT LIST:
        /*$("#textlist").on("click", function() {
            selectedText = $("#textlist").val();
            if ($("#tabTwo .panel-contents").text() !=
                selectedText.text) {
                $("#tabTwo .panel-contents").text(selectedText);
            }*/
            //Show panel-contents if it's hidden and contains text:
            /*if ($("#tabTwo .panel-contents").text() !== "" &&
                $("#tabTwo .panel-contents").css("display") ===
                "none") {
                $("#tabTwo .panel-contents").css("display",
                    "inline-block");
            }
        });*/

       $("#latin_TE_DropDown").on("click", function() {
            selectedText = $("#latin_TE_DropDown").val();
            if ($("#tabTwo .panel-contents").text() != selectedText) {
               $("#tabTwo .panel-contents").text(selectedText);
            }

           else if($("#tabTwo .panel-contents").text() !== "" &&
               $("#tabTwo .panel-contents").css("display") ===
               "none") {
               $("#tabTwo .panel-contents").text(selectedText);
               $("#tabTwo .panel-contents").css("display", "inline-block");
             }
        });

       
      $("#latin_TK_DropDown").on("click", function() {
            selectedText = $("#latin_TK_DropDown").val();
            if ($("#tabTwo .panel-contents").text() != selectedText) {
               $("#tabTwo .panel-contents").text(selectedText);
            }
            else if($("#tabTwo .panel-contents").text() !== "" &&
               $("#tabTwo .panel-contents").css("display") ===
               "none") {
               $("#tabTwo .panel-contents").text(selectedText);
               $("#tabTwo .panel-contents").css("display", "inline-block");
             }
        });

       $("#latin_LI_DropDown").on("click", function() {
            selectedText = $("#latin_LI_DropDown").val();
            if ($("#tabTwo .panel-contents").text() != selectedText) {
               $("#tabTwo .panel-contents").text(selectedText);
            }
            else if($("#tabTwo .panel-contents").text() !== "" &&
               $("#tabTwo .panel-contents").css("display") ===
               "none") {
               $("#tabTwo .panel-contents").text(selectedText);
               $("#tabTwo .panel-contents").css("display", "inline-block");
             }
        });

       $("#greek_TE_DropDown").on("click", function() {
            selectedText = $("#greek_TE_DropDown").val();
            if ($("#tabTwo .panel-contents").text() != selectedText) {
               $("#tabTwo .panel-contents").text(selectedText);
            }
            else if($("#tabTwo .panel-contents").text() !== "" &&
               $("#tabTwo .panel-contents").css("display") ===
               "none") {
               $("#tabTwo .panel-contents").text(selectedText);
               $("#tabTwo .panel-contents").css("display", "inline-block");
             }
        });

       $("#greek_TK_DropDown").on("click", function() {
            selectedText = $("#greek_TK_DropDown").val();
            if ($("#tabTwo .panel-contents").text() != selectedText) {
               $("#tabTwo .panel-contents").text(selectedText);
            }
            else if($("#tabTwo .panel-contents").text() !== "" &&
               $("#tabTwo .panel-contents").css("display") ===
               "none") {
               $("#tabTwo .panel-contents").text(selectedText);
               $("#tabTwo .panel-contents").css("display", "inline-block");
             }
        });

       $("#greek_LI_DropDown").on("click", function() {
            selectedText = $("#greek_LI_DropDown").val();
            if ($("#tabTwo .panel-contents").text() != selectedText) {
               $("#tabTwo .panel-contents").text(selectedText);
            }
            else if($("#tabTwo .panel-contents").text() !== "" &&
               $("#tabTwo .panel-contents").css("display") ===
               "none") {
               $("#tabTwo .panel-contents").text(selectedText);
               $("#tabTwo .panel-contents").css("display", "inline-block");
             }
        });



        $("#dropDownDiv select > option").on("click", function () {
           $("#dropDownDiv").children().each( function() {
		if ($(this).css("display") == "none") {
                $(this).attr("name", "");
                //console.log($(this).attr("id"));
                //console.log($(this).attr("name"));
              }
             if ($(this).css("display") == "block") {
                $(this).attr("name", "textlist");
                //console.log($(this).attr("id"));
                //console.log($(this).attr("name"));
              }
           });
        });


       $("#include_or_exclude label").on("click", function() {
           //console.log($(this).attr("value"));
           if($(this).attr("value") == "exclude") {
              $("#filtering_note").text("You can choose to filter all words in one or more texts or selections of one or more texts");
           } else if ($(this).attr("value") == "include") {
              $("#filtering_note").text("You can choose to make a list that includes only those words that appear in your text and one or more texts or selections of texts.");
           }
       });

      /* $("#include_or_exclude label").each(function() {
          if($(this).hasClass("active")) {
           console.log($(this).attr("value") + "is the value");
           if($(this).attr("value") == "exclude") {
             $("#filtering_note").text("You can choose to filter all words in one or more texts or selections of one or more texts");
           }
           else if($(this).attr("value") == "include") {
             $("#filtering_note").text("You can choose to make a list that includes only those words that appear in your text and one or mmore texts or selections of texts.");
           }
          }
       })*/;
      
 
$(".type_of_txt_btn_group label").on("click", function() {
 /********************************************************
  * #INFO: This is responsible for manipulating the three
  * Text, Textbook, and List buttons
  *******************************************************/
           var label = $(this).attr('value');
           var idcomp = globalLang + "_" + label + "_DropDown";
           $("#dropDownDiv select").each(function() {
                var buttoncomp = $(this).attr('id');
                $(this).css("display", "none");
                if(buttoncomp == idcomp) {
                    $(this).css("display", "block");
                }              
          }); 
});



/*$("#dropDownDiv select").on("click", function() {
      selectedValue = $(this).attr('value');
      console.log(selectedValue);
 });*/



      /*$("#latinTextsDropDown").on("click", function() {
           selectedText = $("#latinTextsDropDown").val();
           console.log(selectedText);
          if ($("#tabTwo .panel-contents").text() != 
               selectedText.text) {
              console.log("panel was not equal to selectedText (latin)"); 
              $("#tabTwo .panel-contents").text(selectedText);
          }
         if ($("#tabTwo .panel-contents").text !== "" &&
             $("#tabTwo .panel-contents").css("display") ===
             "none") {
             console.log("panel was not empty but it was on display none. (latin)");
             $("#tabTwo .panel-contents").text(selectedText);
             $("#tabTwo .panel-contents").css("display", "inline-block");
         }
      });

      $("#greekTextsDropDown").on("click", function() {
          selectedText = $("#greekTextsDropDown").val();
          if ($("#tabTwo .panel-contents").text() !=
               selectedText.text) {
              console.log("panel was not equal to selectedText (greek)");
              $("#tabTwo .panel-contents").text(selectedText);
          }
         if ($("#tabTwo .panel-contents").text !== "" &&
             $("#tabTwo .panel-contents").css("display") ===
             "none") {
             console.log("panel was not empty but it was on display none. (greek)");
             $("#tabTwo .panel-contents").text(selectedText);
             $("#tabTwo .panel-contents").css("display", "inline-block");
         }
      });*/
    

    } //END of event bindings for INDEX.HTML!


    /*===== Event bindings for WORDS_LIST.HTML and GREEK_WORDS_LIST.HTML =====*/
    else if ($("body").data("title") === "words_page") {
        // Find scrollbar width and store in global variable.
        // Used to keep UI animations pretty:
        scrollbar_width = getScrollbarWidth();

        // Set POS toggles to "all" on reload:
        $(".pos-toggle-box input").each(function() {
            if ($(this).attr("value") === "all") {
                $(this).button('toggle');
            }
        });


        /* SLIDEOUT PANEL EVENT BINDINGS: */
        //Slideout panel scroll control:
        $(window).scroll(function() {
            resizeSlideoutPanel();
        });
        $(window).resize(function() {
            resizeSlideoutPanel();
        });
        $(document).resize(function() {
            resizeSlideoutPanel();
        });

        $(".filters-container").on("click",function(e) {
            var div = $(e.target).parent().children("div");
            //console.log(div);
            if (div.css("display") === "none") {
                div.slideDown(100);
            }
            else {
                div.slideUp(100);
            }
        });
/*
        //EXPORT button bindings:
        $("#tab_delim_export").on("click", function() {
            var tsv=tableToCSV('\t');
            // Data URI
            var tsvData = 'data:application/tsv;charset=utf-8,' +
                encodeURIComponent(tsv);
            $(this)
                .attr({
                    'download': "export.tsv",
                    'href': tsvData,
                    'target': '_blank',
                    'action': tsvData
                }); 
            //window.location = tsvData;
            /*
            //this is legacy code and you should delete it next time you see it
            $(this)
                .attr({
                    'download': generateFilename("file","0","100"),
                    'href': tsvData,
                    'target': '_blank'
                }); 
            *
        });
*/

//make a column



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


var tableToExcel = (function () {
        var uri = 'data:application/vnd.ms-excel;base64,'
        , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
        , base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))) }
        , format = function (s, c) { return s.replace(/{(\w+)}/g, function (m, p) { return c[p]; }) }
        //console.log(document.getElementById('dlink'))
        $("#excel_export").on("click", function() {
            tableToExcel('words_generated', 'name', 'myfile.xls')

        });


        return function (table, name, filename) {
            if (!table.nodeType) table = document.getElementById("words_generated")
            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML }
            document.getElementById("dlink").href = uri + base64(format(template, ctx));
            document.getElementById("dlink").download = filename;
            document.getElementById("dlink").click();
        

        }
    })();









    //Function that allows the print button on words page to work
    function printData()
    {
       //var previouslen = words_table.page.len();
       //words_table.page.len(-1);
       //words_table.draw();
       //$("#words_generated") = words_table;
       var divToPrint=document.getElementById("words_generated");
       //words_table.page.len(previouslen);
       newWin= window.open("");
       newWin.document.write(divToPrint.outerHTML);
       //words_table.page.len(previouslen);
       //words_table.draw();
       newWin.print();
       //words_table.page.len(previouslen);
       //words_table.draw();
       newWin.close();
    }

/*function renderFn( column, display, data) {
    return;

}

    function renderDatatableCell(table, row, column, renderFn ) {
          var data = row.data();
          var cell = $(table.rows().nodes(row)).children("td:nth-child(" + (column + 1) + ")");
          $(cell).html( renderFn( data[column], "display", data ) );
        }

       function renderDatatableColumn( oTable, column ) {
          var rows = oTable.fnGetData().length;
          if (rows > 0) {
            var renderFn = oTable.fnSettings().aoColumns[column].mRender;
            for (row = 0; row < rows; row ++) {
            renderDatatableCell( oTable, row, column, renderFn );
            }
          }
       }*/
    $("#tag4exportAll").on('click', function (event) {
        // CSV
        //console.log("DEBUG YOU CLICKED THIS");
        visibility_list = []
        words_table.columns().every( function() {
          if (this.visible()) {
            visibility_list.push(true);
          } else {
            visibility_list.push(false);              
          }
       });
        //console.log("DEBUG", visibility_list);
        //make every row displayed
        var accu=0;
        /*var table_columns = words_table.settings().init().columns;
        table_columns.every( function() {
          this.visible(true);
        });*/
        words_table.columns().every( function() {
           this.visible(true);
        });
           // words_table.columns($(global_columns[i]).data("fieldname")).visible(true);
        //};
       /* function renderDatatableCell( oTable, row, column, renderFn ) {
          var data = oTable.fnGetData( row ); 
          var cell = $(oTable.fnGetNodes( row )).children("td:nth-child(" + (column + 1) + ")");
          $(cell).html( renderFn( data[column], "display", data ) );
        }

       function renderDatatableColumn( oTable, column ) {
          var rows = oTable.fnGetData().length;
          if (rows > 0) {
            var renderFn = oTable.fnSettings().aoColumns[column].mRender;
            for (row = 0; row < rows; row ++) {
            renderDatatableCell( oTable, row, column, renderFn );
            }
          }
       }*/
        var previouslen = words_table.page.len();
        words_table.page.len(-1);
        words_table.draw();
        /*words_table.rows().every( function() {
           renderDatatableCell(words_table, this, words_table.column(7), renderFn);
        });*/
        //console.log("HEADERS", words_table.columns().header());
        //console.log("DEBUG here we are.");
        exportTableToTSV.apply(this, [$('#words_generated'), 'export.tsv']);
        var visList_accu = 0;
        words_table.columns().every( function() {
           this.visible(visibility_list[visList_accu]);
           visList_accu+=1;
        });
        words_table.page.len(previouslen);
        words_table.draw();

        // IF CSV, don't do event.preventDefault() or return false
        // We actually need this to be a typical hyperlink
});



    //not sure if this one works
    $('#printSubmit').on('click',function(){
    printData();
    });

    /*$("#printAllRows").on("click", function() {
      printAllData();
    });*/

//console.log(tableToExcel)
        /* FILTERING/CHECKBOX BINDINGS: */
        
        // Filter buttons on click event
        $('.panel-body .checkdiv').click(function() {
            setCheckdiv(this);
            filterTable();
        });
        $('.panel-body .pos-toggle-box .btn-group').click(function(e) {
            $(e.target).button('toggle');
            togglePOSToggle(e.target);
            if ($(e.target).attr("value") !== "select") {
                filterTable();
            }
        });

        //CHECK ALL filter bindings:
        $('.toggleAll').click(function() {
            var check = $(this).data("check"); // Determine button action.
            // Set POS toggle states accordingly:
            $(".pos-toggle-box input").each(function() {
                if ($(this).attr("value") !== "select") {
                    if (check && $(this).attr("value") === "all") {
                        $(this).parent().button('toggle');
                    }
                    else if (!(check) && $(this).attr("value") === "none") {
                        $(this).parent().button('toggle'); 
                    }
                    togglePOSToggle(this); // apply appropriate styles to pos-toggle.
                }
            });
            // Check/uncheck all checkboxes:
            $("#filters_panel .checkdiv").each(function() {
                setCheckdiv(this,check);
            });
            $(this).data("check",!(check)); // Flip button function.
            filterTable(); // Update table.
        });
        
        /*/ This must be a hyperlink
        $(".tab_export").on('click', function(event) {
            // CSV
            exportTableToTSV.apply(this, [$('#words_generated'),
                'export.tsv'
            ]);

            // IF CSV, don't do event.preventDefault() or return false
            // We actually need this to be a typical hyperlink
        });*/
        
        /* Load words from server: */
        //$("#loading_gif").css("display","block");
        // AJAX request:
        //console.log(words_metadata,words_metadata.text)
        var requestUrl= "/get_words/"+words_metadata.language+'/'+words_metadata.text_comp+
            '/'+words_metadata.bookslist+'/'+words_metadata.text_from+
            '/'+words_metadata.text_to+'/'+words_metadata.add_remove+'/';
        console.log(requestUrl);
        itercheck = itercheck + 1;
        console.log("before JSON, itercheck = " + itercheck);
        $.getJSON(requestUrl)
            .done(function(receivedData) {
                words_data = loadWordData(receivedData);
                console.log("itercheck's value: " + itercheck);
                // Hide "loading" notifications, show "loaded" ones:
                //$("#loading_gif").css("display","none"); //bye kitty!
                $("#word_load_info").css("display","none");
                $("#word_load_success span").text(receivedData.length);
                $("#word_load_success").css("display","block");
                $("#words_generated_div").css("display","block");
                // Initialize DataTables object:
                initTable(); 
                // Make sure slideout isn't overlapping head/foot:
                resizeSlideoutPanel();
                // Enable s/lideout panel slide behavior once words load:
                $("#slideout-pulltab").css({
                    "background":"gray",
                    "border":"1px solid gray"
                });
                $("#slideout-pulltab").on("click",function(e) {
                    toggleSlideoutPanel();  //show/hide filter panel
                    // Activate body click listener when panel is open:
                    if (!($("#slideout-panel").data("stowed"))) {
                        $("body").on("click",slideoutPanelHelper);
                    }
                    else {
                        $("body").off("click",slideoutPanelHelper);
                    }
                });
            })

          .fail(function(receivedData) {
   /**************************************************************************************/
   /************* THIS IS WHAT HAPPENS WHEN THERE IS A FAILURE TO RECEIVE DATA ***********/
   /**************************************************************************************/
               console.log("failure to generate vocabulary list");
               console.log(receivedData);
               $("#word_load_info").css("display", "none");
               $("#word_load_failure").css("display", "block");
               resizeSlideoutPanel();
               toggleSlideoutPanel();
               //$("#slideout-pulltab").on("click",function(e) {
                 
               //});            
          });
        
    } // END of event bindings for WORDS_LIST.HTML and GREEK_WORDS_LIST.HTML!


}); // END OF $(document).ready!



/*===========================================================================
  ======================  FUNCTION DEFS for INDEX.HTML  =====================
  ===========================================================================*/
//id of currently selected accordion form tab:
var active_form_tab = "tabOne";


function handleMediaQuery(mq) {
    /* Reconfigures site appearance based on CSS media queries.
     * mediaQuery objects are declared and bound in $(document).ready.*/
    // if "screen and (max-width: 500px)":
    if (/screen and \(max-width:\s*400px\)/.test(mq.media)) {
    }
    // if "screen and (max-width: 700px)":
    else if (/screen and \(min-width:\s*401px\)/.test(mq.media) ||
        /screen and \(max-width:\s*700px\)/.test(mq.media)) {
    }
    // if "screen and (max-width: 1000px)":
    else if (/screen and \(min-width:\s*701px\)/.test(mq.media) ||
        /screen and \(max-width:\s*1000px\)/.test(mq.media)) {
    }
    // if "screen and (min-width: 1001px)":
    else if (/screen and \(min-width:\s*1001px\)/.test(mq.media)) {
    }
}

/*Configures giant_form to match the language selected by the user. */
function configureForm(e) {
    /****************************************/
    /*Where filtering takes place for languages, so let's add filtering for buttons (or pay attention)*/
    /****************************************/
    var lang = e.data.language;
    globalLang = lang;
    //console.log(lang + globalLang);
    // Set the redirect page to the appropriate lang:
    $("#giant_form").attr("action", "words_page_redirect/" + lang + "/");
    // Configure SOURCE TEXT TAB to only show texts from specified lang:
    var books = $("#textlist").find("[class$='book']");
    books = books.add($("#booklist").find("[class$='bookthumb']"));
    $(".type_of_txt_btn_group label").each(function() {
          $(this).removeClass("active");
     });
     if(!$("#first-active").hasClass("active")) {
        $("#first-active").addClass("active");
      }

        if(lang=="greek") {
        //hide the latin selector.
        $(".intro-text").css({'color':'#1E9E6B','-webkit-transition':'color 0.4s ease','-moz-transition':'color 0.4s ease','-o-transition':'color 0.4s ease','transition':'color 0.4s ease'}); //#457798 shade of green
        $("#dropDownDiv [id*='latin']").css("display", "none");
        $("#dropDownDiv [id*='greek']").css("display", "block");
        $("#greek_LI_DropDown").css("display", "block");
        $("#greek_TK_DropDown").css("display", "none");
        $("#greek_TE_DropDown").css("display", "none");
        //Make it so that all Latin text buttons are hidden.
        $(".latinbookthumb").css("display", "none");
        $(".greekbookthumb").css("display", "inline");
        $(".greekbookthumb").each(function() {  
	   if($(this).hasClass("booktypeTE")) { 
                 $("$thumbTE").append($(this));
           }
           else if ($(this).hasClass("booktypeLI")) {
                 $("#thumbLI").append($(this));
         } else if ($(this).hasClass("booktypeTK")) {
             $("#thumbTK").append($(this));
         } 
       });
    }
    else if (lang=="latin") {
        $(".intro-text").css({'color':'#cb4332','-webkit-transition':'color 0.4s ease','-moz-transition':'color 0.4s ease','-o-transition':'color 0.4s ease','transition':'color 0.4s ease'}); //#cb4332 is the same shade of red as the latin button
        $("#dropDownDiv [id*='greek']").css("display", "none");
        $("#dropDownDiv [id*='latin']").css("display", "block");
        $("#latin_LI_DropDown").css("display", "block");
        $("#latin_TK_DropDown").css("display", "none");
        $("#latin_TE_DropDown").css("display", "none");
        $(".greekbookthumb").css("display", "none");
        $(".latinbookthumb").css("display", "inline");
        $(".latinbookthumb").each(function() { 
           if($(this).hasClass("booktypeTE")) {
                 $("#thumbTE").append($(this));
           }
           else if ($(this).hasClass("booktypeLI")) {
                 //console.log("latin list detected");
                 $("#thumbLI").append($(this));
         } else if ($(this).hasClass("booktypeTK")) {
             //console.log("latin textbook detected");
             $("#thumbTK").append($(this));
         }
       });

    }
    // Hide all text/book elements NOT part of the selected language:
    books.not("[class*='" + lang + "']").css("display", "none");
    // Show all which are part of the selected language:
   // books.filter("[class*='" + lang + "']").css("display", "block");
    //What if I had a function that took books as an arg, and then applied filters based on event.

    //Clear and hide panel-contents in SOURCE TEXT TAB:
    $("#headingTwo .panel-contents").text("");
    $("#headingTwo .panel-contents").css("display", "none");

    //Deselect any texts in the READ TEXT TAB: 
    //(selected texts have a checkbox input child to their :button)
    // Remove the hidden checkbox:
    $(".hiddencheck").remove();
    // Remove any book titles in the read text tab:
    $("#headingThree .panel-contents").text("");
    $("#headingThree .panel-contents").css("display", "none");
    $(".thumbnail").css("background", "#FFFFFF");
    $(".thumbnail").css("border", "1px solid #ccc");
    $(".range_select_box").css("display", "none");
    $(".range-select-toggle").css("display", "none");

    //Modify language select accordion tab to reflect selected lang.:
    $("#headingOne .panel-title").css("text-align", "left");
    //capitalize language and att it to lang select tab: 
    $("#headingOne .panel-contents").text(lang.charAt(0).toUpperCase() +
        lang.slice(1));
    $("#headingOne .panel-contents").css("display", "inline-block");

    switchFormTabs($("#tabOne"), $("#tabTwo"));

    // Make the text select accordion tab expand+collapsible: 
    $("#tabThree").attr("data-toggle", "collapse");
    $("#tabTwo").attr("data-toggle", "collapse");
}

/*if(!$("#tabThree").hasClass("collapsed")) {
    console.log("currently collapsed");
}*/

/***********************************************************
 * FUNCTIONING FOR MAKING "EXCLUDE PART FOLLOW WHEN YOU SCROLL
 * making changes
*************************************************************/
/*$("#headingThree").parent().scroll(function() { 
    $('#headingThree').css('top', $(this).scrollTop());
});*/

/*alert($("#headingThree").parent().attr("id"));*/

function userFormInteract(e) {
    var clickedTab = $(e.target).parents("[id^='tab']");
    /*console.log(clickedTab.attr("id"));
    console.log(active_form_tab);
    console.log(clickedTab.attr("id") != active_form_tab);
    if ((clickedTab.attr("id") == "tabOne") && (active_form_tab == "tabOne")) {
        console.log("gotcha!");
         console.log("the clickedtab id: " + clickedTab.attr("id"));
        console.log("the active form tab: " + active_form_tab);
        if ($("#tabOne").attr("aria-expanded") == "true") {
           console.log("oh no you don't!");
           $("#tabOne").attr("aria-expanded", "true");
           return;
        }
     }*/ 
       //lat time no dragon ball z we learned that this accurately identifies the scenario it needs to
       //when one tries to click the select a language bit right at the home page.
       //However, adding the return statement does nothing. something else is changing stuff.
    if ((clickedTab.attr("id") != active_form_tab) && 
        ($("#giant_form").attr("action") != "")) {
        //console.log("we still got here!");
        switchFormTabs($("#" + active_form_tab), clickedTab);
     } /*else if ((clickedTab.attr("id") == "tabOne") && (active_form_tab == "tabOne")) {
        console.log("gotcha!");
        if ($("#tabOne").attr("aria-expanded") == "true") {
           console.log("yessss");
           return;*/
        /* else {
          console.log(clickedTab.attr("aria-expanded"));
        }*/
      
      else {
        console.log("PLEASE SELECT A LANGUAGE FIRST!"); //switch in "headingOne"
        /*$(".intro-text").animate({
            opacity: 0.25
        }, 1000, function() {});*/ //Commented this out because this currntly isn't having a good effect.
    }
}

function switchFormTabs(current, next) {
    /* Formats and hides/shows accordion tabs in the main form.
     *

     * current and next are both <a> elements, the clickable part of an 
     *  accordion tab.
     */

    //Change current's tab header to look "inactive", and COLLAPSE it:

    current.find(".panel-heading").css("background-color", "#FFFFFF");
    current.find(".panel-title").css("color", "black");
    current.find(".panel-contents").css("color", "gray");
    current.find(".panel-contents").css("border", "1px solid gray");
    current.siblings(".collapse").collapse("hide");

    //Change next's tab header to look "active", and EXPAND it:
    next.find(".panel-heading").css("background-color", "#FFFFFF");
    next.find(".panel-title").css("color", "black");
    next.find(".panel-contents").css("color", "black");
    next.find(".panel-contents").css("border", "1px solid black");
    next.parent().removeClass("hidden")
    next.parent().next().removeClass("hidden")
    $("#giant_form_submit").removeClass("hidden")
    next.siblings(".collapse").collapse("show");

    //Reflect this change in the active form tracking variable:
    active_form_tab = next.attr("id");
}

//function showTip() {
    //var selects = $('textlist'); //What is textlist's value? Where does this come from
    //var selectedValue = selects.val();
    //Shows all or selection under textlist
    /* Commenting out 6/20/17, doesn't seem to do anything? $('#all_or_selection').css("display", "block");*/

    /*if (selectedValue == "DCC Latin Core" ||
        selectedValue == "DCC Greek Core" ||
        selectedValue == "Herodotus Book 1 Core (412 words > 10 times)" &&
        $("#Selection").checked == true) {
        $("#core_tip").css("display", "block");
        $("#other_tip").css("display", "none");
        $("#core_tip").popover('hide');
        $("#other_tip").popover('hide');
    } else if ($("#Selection").checked == true) {
        $("#core_tip").css("display", "none");
        $("#other_tip").css("display", "block");
        $("#core_tip").popover('hide');
        $("#other_tip").popover('hide');

    }*/
    
//}

// Makes sure that selection input is correct
function validateTextSelect() {
    var x = $("#text_from").val();
    var y = $("#text_to").val();

    if (x != "") {
        if (y == "") {
            return false;
        }
    } else if (y != "") {
        if (x == "") {
            return false;
        }
    } else if (x == "" && y == "") {
	return false
    } else if (x[0] == "." || y[0] == ".") {
        return false;
    } else if (x.split(".").length > 3 || y.split(".").length > 3) {
        return false;
    } else if (x.split(".")[0] > y.split(".")[0]) {
        return false;
    } else if (x.split(".")[0] == y.split(".")[0]) {
        if (x.split(".")[1] > y.split(".")[1]) {
            return false;
	}
    } else if (x.split(".")[1] == y.split(".")[1]) {
        if (x.split(".")[2] > y.split(".")[2]) {
            return false;
	}
    }
}


// Makes sure that selection input is correct
function validateBookSelect(a) {
    var x = a[0].value;
    var y = a[1].value;

    if (x[0] == "." || y[0] == ".") {
        return false;
    }
    if (x.split(".").length != y.split(".").length) {
        return false;
    } else if (x.split(".").length > 3) {
        return false;
    } else if (parseInt(x.split(".")[0]) > parseInt(y.split(".")[0])) {
        return false;
    } else if (parseInt(x.split(".")[0]) == (parseInt(y.split(".")[0]))) {
        if (parseInt(x.split(".")[1]) > parseInt(y.split(".")[1])) {
            return false;
        } else if ((parseInt(x.split(".")[1]) == parseInt(y.split(".")[1]))) {
            if (parseInt(x.split(".")[2]) > parseInt(y.split(".")[2])) {
                return false;
            }
        }
    }
}

// Displays all or selection for textlist
function displayForm2(c) {
    var btnText = $(c).attr("value");
    if (btnText == "All") {
        $("#text_selection").slideUp(60); //slideUp?
        $("text_from").val("");
        $("text_to").val("");
        $("text_from").required = false;
        $("#text_to").required = false;
    } else if (btnText == "Selection") {
        $("#text_selection").slideDown(60); //slideDown?
        $("#text_from").required = true;
        $("#text_to").required = true;
    } else {}
}



/*===========================================================================
  ======  FUNCTION DEFS for WORDS_LIST.HTML and GREEK_WORDS_LIST.HTML  ======
  ===========================================================================*/
var words_metadata; // Object. Properties are parameters for vocab AJAX request.
var words_table; // Table of words, a DataTable object.  
var words_data;  // Parsed JSON object of words (WordTable obj.s).
                 // Data first loaded in by loadWordData call in inline script.
var scrollbar_width; // Width of a scrollbar in user's browser.

/* Click handler for POS toggles.  
 * Shows/hides pos-toggle-box checkboxes and sets their state as appropriate. */
function togglePOSToggle(clicked) {
    //console.log(clicked);
    var val = $(clicked).attr("value");
    // Get div containing filters for individual conjugations/declensions:
    var subcat_box = $(clicked).closest('.pos-toggle-box')
        .find(".pos-subcategory-box");

    if (val === "select") {
        subcat_box.slideDown(80);
    }
    else {
        subcat_box.slideUp(80);
        // Apply appropriate state to all of subcat_box's checkboxes:
        var checked = (val === "all");
        subcat_box.find(".checkdiv").each(function() {
            setCheckdiv(this,checked);
        });
    }
}

//var pos_flag=false;
/* Sets the state (checked/unchecked) of a checkdiv.
 * Sets state to check, or flips state if check is undefined. */
function setCheckdiv(clicked,check) {
    var checkbox =$(clicked).find(".checkdiv-checkbox"); 
    // Flip state if set_state is unspecified:
    if (check===undefined) {
        check = !(checkbox.data("state"));
    }
    //console.log("check: " + check);
    //console.log(checkbox.data("state"));
    checkbox.data("state",check);
    //console.log(checkbox.data("state"));
    // Apply appropriate styles to checkbox:
    if (check) {
        //console.log("check did exist");
        checkbox.css("background-color","#808080");
    }
    else {
        //console.log("check didn't exist");
        checkbox.css("background-color","#F1F1F1");
    }
}

//Stows slideout panel if user clicks on page body (excluding slideout panel).
// e is click event.
function slideoutPanelHelper(e) {
    if ($(e.target).parents("#slideout-panel").length === 0 &&
            $(e.target).parents("#slideout-pulltab").length === 0) {
        toggleSlideoutPanel();
        $("body").off("click",slideoutPanelHelper);
    }
}

//Opens/closes the slideout panel:
function toggleSlideoutPanel() {
    var panel = $("#slideout-panel");
    var pulltab = $("#slideout-pulltab");
    // If stowed, slide to the left:
    var panel_slide = 0;
    var pulltab_slide = panel.width();
    var scrollbar = "scroll"; //css for shwoing/hiding scrollbar.
    // If slideout-panel has a scrollbar, compensate for extra width:
    if ($("#slideout-container")[0].scrollHeight >=
            $("#slideout-container").height()) {
        pulltab_slide += scrollbar_width; // scrollbar_width is a global var.
    }
    
    // If the panel isn't stowed, slide to the right:
    if (!(panel.data("stowed"))) {
        //console.log("DYLAN", pulltab_slide)
        panel_slide = -1*pulltab_slide;
        pulltab_slide = 0;
        scrollbar = "hidden";
    }
    // Show/hide scrollbar:
    $("#slideout-container").css("overflow-y",scrollbar);

    // animate panel and pulltab sliding: 
    //console.log("DYLAN", panel_slide)
    panel.animate({
        right: panel_slide
    });
    pulltab.animate({
        right: pulltab_slide
    });
    //Make the container have no width if it is not open
    //Note that this is a bad way of doing this and I don't really know what I am doing
    //-Dylan

    //console.log(pulltab.css("right"),DYLAN)
    if (pulltab.css("right") != '0px') {
        var div_o = 40;
    }
    else{
        var div_o = 360

    }
    $("#slideout-container").animate({
        "width" : div_o
    });
    panel.data("stowed", !(panel.data("stowed")));
    
    // reverse the direction of the chevron glyphs:
    $("#pulltab .glyphicon")
        .toggleClass("glyphicon-chevron-right glyphicon-chevron-left");
}

function resizeSlideoutPanel() {
    var viewportHeight = $(window).height();
    var viewportBot = $(window).scrollTop() + viewportHeight; // In DOCUMENT.
    var navbarBot = $("#main-nav").offset().top+$("#main-nav").height(); // In DOCUMENT. //switched to main-nav from navbar
    var footerTop = $(".site-footer").offset().top; // In DOCUMENT.
    var divTop = parseInt($("#slideout-container").css("top")); // In VIEWPORT.
    // Keep from overlapping header:
    var divTop_new = Math.max(0, navbarBot - $(this).scrollTop());
    // Keep from overlapping footer:
    var divHeight_new = Math.min(viewportBot, footerTop);
    divHeight_new -= $(this).scrollTop() + divTop_new;

    $("#slideout-container").css({
        "top" : divTop_new,
        "height" : divHeight_new,
    });

    // Also keep slideout toggle below the header:
    $("slideout-toggle").css({
        "top" : Math.max(0,navbarBot+5-$(this).scrollTop())
    });
}

function greek_def_function() {
    if ($("#No definitions").checked == true) {
        hide_column(2);
    } else if ($("#English Definition").checked == true) {
        show_column(2);
    }
}

function lemma_function() {
    //console.log($("#Dictionary Entry (macron)"));
    if ($("#Dictionary Entry (macron)").checked == true) {
        hide_column(2);
        show_column(1);
    } else {
        hide_column(1);
        show_column(2);
    }
}

$('#backToTopBtn').click(function() {
    $('html,body').animate({
        scrollTop: 0
    }, 'slow');
    return false;
});


/* Given text name and text ranges, returns a valid file name.*/
function generateFilename(text, text_from, text_to) {
    var formatted = text.replace(/,|\.|:|"|'/g,'');
    var formatted = formatted.split(/ /).join('_');
    var filename = formatted.slice(0,30)+"--"+words_metadata.text_from
                +"_to_"+words_metadata.text_to
    return filename
}

global_valid_ths = [];
global_columns = [];

/* Determine settings of and initialize the words_table: */
function initTable() { 
    //Determine columns from data attrs of <th> elements: 
    //  data-fieldname is the name of a property in WordTable.fields.
    //  data-visible determines whether this col is shown by default.

    //iter = iter + 1;
    //console.log("iteration: " + iter);

    var columns = [];
    var valid_ths = []; // list of <th>s turned into DataTables columns.
    var fields;
    var accu2=0;
    // Find a wordTable object, used for validating fieldname:
    for (var prop in words_data) {
        //accu2+=1;
        //console.log("accu's value followed by prop: " + accu2);
        //console.log(prop);//words data actually contains... every WordProperty model. That's where you were.
        if (words_data.hasOwnProperty(prop) && words_data[prop].length > 0) {
            fields = words_data[prop][0].fields;
            break; //this was break, maybe supposed to be continue?
        } else {
          //console.log(prop);
         }
    }
    //console.log("FIELDS", fields);
    //console.log("FIELDS.LOGEION", fields.logeion_url);
    // Get field names and visibility from table column headers:
    $("#words_generated th").each(function() { //The first step in adding a new column is to add it as a words_generated th. 
        //console.log("[inittable] fieldname: " + $(this).data("fieldname"));
        if (fields.hasOwnProperty($(this).data("fieldname"))) { //if valid prop 
            valid_ths.push(this);
            // Create dataTables column based on <th> data-attrs:
            // Note
            if ($(this).data("fieldname") == "logeion_url" && !$(this).hasClass("logUrl2")) {
               //console.log("CREATING LOGEION URL COLUMN");
               columns.push({
                  "name": $(this).data("fieldname"),
                  "data" : "fields."+$(this).data("fieldname"),
                  "render" : function ( data, type, full, meta ) {
                     return '<a target="_blank" href="'+data+'">Logeion</a>';
                   },
                  "visible" : $(this).data("visible")
              });
            } else if ($(this).data("fieldname") == "logeion_url" && $(this).hasClass("logUrl2")) {
              //console.log("FULL LINK DETECTED");
              columns.push({
                  "name": $(this).data("fieldname"),
                  "data" : "fields."+$(this).data("fieldname"),
                  "visible" : false,
                });
           } else if ($(this).data("fieldname") == "corpus_rank") {
                columns.push({
                  "name": $(this).data("fieldname"),
                  "data": "fields."+$(this).data("fieldname"),
                  "render": function( data, type, full, meta) {
                      if (data > 9600) {
                        return "rare";
                      } else {
                        return data;
                     }
                   },
                  "visible": $(this).data("visible"),
             });
           } else if ($(this).data("fieldname") == "english_extended") {
             columns.push({
               "name": $(this).data("fieldname"),
               "data": "fields."+$(this).data("fieldname"),
               "visible": $(this).data("visible"),
               "width": "20%"
            });
          }




              //a second row for the full unrendered logeion URL is pushed.
              /*columns.push({
                 "name": "FullUrl",
                 "data": "fields."+$(this).data("fieldname"),
                 "visible" : false,
              });*/
             else { 
                 columns.push({
                    "name" : $(this).data("fieldname"),
                    "data" : "fields."+$(this).data("fieldname"),
                    "visible" : $(this).data("visible")
                    });
               }
         }
      
            //I THINK THIS WAS BAD- DYLAN
            //if (!($(this).data("visible"))) { // hide table header of non-visible columns.
                //$(this).css("display","none");
            
        else {
            console.log('WARNING!\nCouldn\'t find field \'' + 
                $(this).data('fieldname') + 
                '\' in the data.  Removing corresponding column \'' + 
                $(this).text() +'\'.');
            $(this).remove();
        }
       });
       //console.log("columns:");
    var accu=0
    /*$("tr td:nth-child(1)").each( function() {
       console.log("CONDITIONAL");
       console.log("NTH CHILD", $(this));
    var colNum = $(this).index();
    var rowNum = $(this).parent().index();
        $(this).wrap('<a href="example.com/hello.html?column=' + colNum + '&row=' + rowNum +'">');
    });*/

    global_valid_ths = valid_ths;
    global_columns = columns;

    // Get filter states and initialize DataTable object:
    var filter_states = determineFilterState();
    //console.log("filter states");
    //console.log(filter_states);
    var word_data_filtered = filterWordData(filter_states);
    words_table = $("#words_generated").DataTable({
        "data" : word_data_filtered,
        "columns" : columns,	 //should this be global_ocolumns
        "aLengthMenu": [[25, 50, 100, 200, -1],
                [25, 50, 100, 250, "All"]],
        "pageLength": 100,
    });
    //console.log("CORPUS RANK COLUMN", words_table.column("corpus_rank").nodes());
    /*words_table.column("corpus_rank").nodes().each( function(cell, i) {
        console.log(words_table.cell(i, 2).data());
    });*/
    //words_table.buttons.export_data
    //words_table.buttons().container().appendTo(words_table.table().container());
    initColumnFilters(valid_ths);
}

/* Builds the "Show/Hide Columns" buttons from a list of <th> elements. */
function initColumnFilters(th_list) {
    var checkdiv_prototype = $(".colFilters_container checkdiv");
    var toggle_prototype = $(".colFilters_container .col-toggle-box");
    // Sort by field type:
    var fieldtypes = {};
    //console.log("Thlist length: " + th_list.length);
    for (var i=0; i<th_list.length; i++) {
        var fieldtype = $(th_list[i]).data("fieldtype");
        // Add <th> to existing array, else create a new array:
        if (fieldtypes.hasOwnProperty(fieldtype)) {
            fieldtypes[fieldtype].push(th_list[i]);
        }
        else {
            fieldtypes[fieldtype] = [th_list[i]];
        }
    } 
    var n=0;
    // Build radio toggle button-groups or checkdivs for each data column:
    for (fieldtype in fieldtypes) {
        n = n + 1
        console.log("iteration: " + n + "   fieldtype: " + fieldtype);
        //debugger;
        if (fieldtypes.hasOwnProperty(fieldtype)) {  // skip inherited prop.s
            if ($(fieldtypes[fieldtype][0]).data('radio')) {
                buildToggle(fieldtypes[fieldtype]);
            }
            else {
                buildCheckdivs(fieldtypes[fieldtype]);
            }
        }
    }
} 

/* Helper for initColumnFilters. Builds bootstrappy radio toggle for
 *  visibility of table columns in field_options.*/
function buildToggle(field_options) {
    //console.log(field_options,"DYLAN")
    var toggle = $("#prototype_container .col-toggle-box").clone();
    // Set label text and ID of toggle:
    var labelText = $(field_options[0]).data('fieldtype'); 
    toggle.attr('id', labelText+'_toggle');
    toggle.find("h4").first().text(labelText);
    
    // Build a toggle button from attr.s of each <th>:
    var proto_btn = toggle.find('.btn').first(); // "none" btn
    for (var i=0; i<field_options.length; i++) {
        var field = $(field_options[i]);
        var btn = proto_btn.clone();
        var btn_input = btn.children().first();
        btn.removeClass('btn-primary');
        btn.attr('value',field.data('fieldname'));
        btn_input.attr('value',field.data('fieldname'));
        btn_input.attr('name',field.data('fieldtype'));
        btn.text(field.text());
        // Add to btn-group, BEFORE "none" btn.
        btn.insertBefore(proto_btn);
       // console.log(field_options);
        //debugger;
    }
    toggle.find('.btn-group').css('width','100%');
    toggle.find('.btn').css('width',
            '100%');
    //Changed this^ from (100/toggle.find('.btn').length)+'%'); //Dylan
    // Set an active button, indicated via the data-visible attr:
    var toggled = false
    for (var i=0; i<field_options.length; i++) {
        var field = $(field_options[i])
        //console.log("in buildToggle, field on " + i)
        //console.log(field)

        if (field[0].attributes['data-visible'].nodeValue=='true') {
            //toggle that button!
            var name = field[0].attributes['data-fieldname'].nodeValue
            btn=toggle.find('.btn')
            
            for (var n=0; n<btn.length; n++) {
                if (btn[n].attributes['value'].value==name){
                    toggled = true
                    btn[n].attributes['class'].nodeValue="btn active" ;
                }
            }
        }
    }
    if (!(toggled)) {
        btn=toggle.find('.btn')
        for (var n=0; n<btn.length; n++) {
            if (btn[n].attributes['value'].value=='none'){
                btn[n].attributes['class'].nodeValue="btn active" 
            }
        }
    }
    // Append to DOM and bind toggle event handlers:
    var container = jQuery('<div/>', {
        class: 'colFilters_container'
    });
    container.append(toggle);
    $('#display_panel_body').append(container);
    container.find('.btn').on('click', function() {
        //toggle visibility (visible col. indicated by .btn class 'active'):
        var thisCol = $(this).attr('value');
        var activeCol = $(this).siblings('.active').attr('value');
        //console.log("thisCol: " + thisCol);
        //console.log("activeCol: " + activeCol);
        words_table.column(activeCol+':name').visible(false);
        // If none, don't show any columns:
        if (thisCol !== 'none') {
            words_table.column(thisCol+':name').visible(true);
        }
        //apply styles:
        //CHANGE TO LIGHT GRAY IF LIKE THAT MORE DYLAN
        //Did that
        $(this).siblings('.active').css({
                'color' : '#000',
                'background-color' : '#E1E1E1'
            });
        $(this).css({
                'color' : '#FFF',
                'background-color' : '#808080'
            });
        $(this).addClass('active');
        $(this).siblings('.active').removeClass('active');
    });
}

/* Helper for initColumnFilters. Builds checkdivs governing visibility of 
 *  table columns in field_options.*/
function buildCheckdivs(field_options) {
    //console.log(field_options,"DYLAN")
    var container = jQuery('<div/>', {
        class: 'colFilters_container'
    });
    // Build a checkdiv from attr.s of each <th>:
    //console.log("legnh of field options: " + field_options.length);
    var proto_checkdiv = $('#prototype_container .checkdiv');
    for (var i=0; i<field_options.length; i++) {
        //console.log("field options positon " + i + ": " + field_options[i]);
        var field = $(field_options[i]);
        if (field.hasClass('logUrl2')) {
           continue; //don't build checkbox!
        }
        var checkdiv = proto_checkdiv.clone(true); //'true' keeps event binding
        var checkdiv_checkbox = checkdiv.find(".checkdiv-checkbox").first();
        checkdiv_checkbox.attr('value',field.data('fieldname'));
        //console.log(field.data('fieldname')); //debug
        //console.log(field[i]);
        //console.log(field[i].attributes['data-visible'].value=='true'); //debug
        checkdiv_checkbox.attr('name',field.data('fieldtype'));
        checkdiv.find('.checkdiv-label').text(field.text());
        if (field.data('fieldname') == "part_of_speech" || field.data('fieldname') == "logeion_url" || field.data('fieldname') == "corpus_rank") {
         //Special conditional for part_of_speech so that it does not keep its check mark.
             checkdiv.attr("data-state", "false");
             checkdiv_checkbox.css("background-color", "#F1F1F1");
        }
        container.append(checkdiv);
    }
    // Add to DOM and bind event handlers:
    $('#display_panel_body').append(container);
    container.find('.checkdiv').on('click',function() {
        var isVisible = $(this).find('.checkdiv-checkbox').data('state');
        var fieldname = $(this).find('.checkdiv-checkbox').attr('value');
        words_table.column(fieldname + ":name").visible(isVisible);
        //debugger;
    });
}

/* Show or hide words based on state of filters: */
function filterTable() {
    // Cover the filter panel with a gray div:
    var panel = $('#filters_panel_body');
    var offset = panel.offset();
    var height = panel.height();
    var width = panel.width();
    $('#filters_panel').append('<div id=cover></div>');
    var new_panel = $('#cover');
    new_panel.offset({
        top: offset.top,
        left: offset.left
    });
    new_panel.css("background-color", "grey");
    new_panel.css("opacity", ".5");
    new_panel.css("height", height);
    new_panel.css("width", width);
    new_panel.css({
        'cursor': 'wait'
    });
    
    // Re-draw words_table based on state of filtering checkboxes:
    var filter_states = determineFilterState()
    //console.log(filter_states);
    var word_data_filtered = filterWordData(filter_states);
    words_table.clear().draw();
    words_table.rows.add(word_data_filtered).draw();
    $("#cover").remove() //remove the gray div
     
}

/*$('#words_generated').on('draw.dt', function (e, settings) {
   console.log("CORPUS RANK DRAW EVENT TRIGGERED");
   if(column("corpus_rank").visible()) {
    console.log("CORPUS RANK COLUMN VISIBLE");
    $(settings.nTBody).find('tr td:last-child').each(function(idx, ele) {
        console.log("IN DRAWING FUNCTION");
        console.log(ele.textContent);
        if (+ele.textContent < 40) {
            ele.textContent = 'unranked';
        }
    });
  }
}).DataTable();*/

/* Determines which words to filter based on state of filter checkboxes.
 * Returns a list of the parts of speech whose words will be displayed. */
function determineFilterState() { 
    var included_pos = []; //which parts of speech pass thru filter
    // Determine filter state of POS toggles (nouns, verbs, etc. 
    //  w/ multiple decl.s and conj.s).
    //  The active btn is always child to an active label.
    $(".pos-toggle-box .btn-group .active input").not("[value='none']")
        .each(function() {
        var pos_checkboxes = $(this).closest(".pos-toggle-box")
                                    .find(".checkdiv-checkbox");
        // If "select" toggled, only include checked checkdivs:
        if ($(this).attr("value") === "select") {
            pos_checkboxes = pos_checkboxes.filter(function() {
                return $(this).data("state");
            });
        }
        // Add checkdiv POS names to the list:
        pos_checkboxes.each(function() {
            included_pos.push($(this).attr("id"));
        });
    });

    //Get other checkboxes' states:
    $(".panel-body .checkdiv-checkbox")
        .not('[name$="_decl"]').not("[name='verb_conj']")
        .each(function() {
            //console.log($(this));
            if ($(this).data("state")) {
                included_pos.push($(this).attr("id"));
            }
    });
    //console.log("included pos: ");
    //console.log(included_pos);
    return included_pos;
}

/* Given array of word categories, returns an array of relevant wordTable objects.
 * wordTable objects are retrieved from word category arrays in words_data.*/
function filterWordData(pos_list) {
    // can turn to true for some helpful console logs!
    var DEBUG = false;


    var words_data_filtered = [];
    var words_data_keys = Object.getOwnPropertyNames(words_data);
    //console.log("WORDS DATA KEYS",  words_data_keys);
    /* So needed to do is identify 'Adverb, preposition' as 'adverb'
     * and 'preposition'. I made a dictionary (pos_dictionary) with a
     * list of everything it should add when it finds that word.
     * So 'Adverb' will be:
     * 'Adverb' : ['Adverb', 'Adverb, Conjunction', 'Adverb, Preposition'] etc.
     */

    // Intialize a dictionary with all the parts of speech we want to add
    var pos_dictionary = {};
    for (var i=0; i<pos_list.length; i++){
	var pos = pos_list[i];
	pos_dictionary[pos]= [];
		
    }

    // Now add (hopefully) all pos from the data appropriately

    // neither adj_2 or adj_ are buttons in the slideout, so we have to add them separate
    // We group them with adj_1 after we add all the other parts of speech
    var has_adj_2 = false;
    var has_adj_ = false;
    for (var i=0; i<words_data_keys.length; i++) {
	var key = words_data_keys[i];
	
	// neither of these are buttons in the slideout, so we have to add them separate
	// We group them with adj_1 after we add all the other data
        if (key == 'Adjective_2'){
          has_adj_2 = true;
        }
        if (key == 'Adjective_'){
	  has_adj_ = true;
	}



        // A regex that matches 1 or more commas and any number of spaces
        prop_list = key.split(/,+\s*/);
	for (var j=0; j<prop_list.length; j++){
           var prop = prop_list[j];
	   if(pos_dictionary[prop] != undefined){
	      pos_dictionary[prop].push(key);
           }
	   else{
             if (DEBUG == true){
               console.log("Part of speech: ", prop, "from key: ", key, " will not be included in the data");
	     }
           }
	}
	
    }
    if (has_adj_2 && pos_dictionary['Adjective_1'] != undefined){
      pos_dictionary['Adjective_1'].push('Adjective_2');
    }
    if (has_adj_ && pos_dictionary['Adjective_1'] != undefined){
      pos_dictionary['Adjective_1'].push('Adjective_');
    }
    if (DEBUG == true){
      console.log(pos_dictionary, "POS_DICT");
    }
    // pos_dictionary now complete

    var modified = {}; // modified: tracks the things we have already changed so we don't double add
    for (var i=0; i<words_data_keys.length; i++) {
        var key = words_data_keys[i];
        var key_index = pos_list.indexOf(key);
	if (key_index>=0) {
	    for(var j=0; j<pos_dictionary[key].length; j++){
	      var prop = pos_dictionary[key][j];
	      if (modified[prop] == undefined){
	        modified[prop] = true;
	        if (DEBUG == true){
		  console.log(prop, "POS added to data");
                }
                words_data_filtered = words_data_filtered.concat(words_data[prop]);
	      }

	    }
	   // We used to removed items instead of marking them as modified
	   // but then you couldn't properly view the list in console
	   // so I switched it, but here is the line a removed
           // pos_list.splice(key_index,1); //rm that key from pos_list
        }
    }
    if (DEBUG == true){
      console.log(words_data_filtered, 'Words returned by filter');
    }
    return words_data_filtered;
}

/* Sort array of words (as WordTables objects) by part of speech */
function loadWordData(data) {
    // Group word objects by filtering category:
    var words_data = {}; // Obj containing array of wordTables objects. Logging these will allow you see the word objects with all of their fields as populated by django.
    for (var i=0; i<data.length; i++) {
        var word = data[i];
        var pos = word.fields["part_of_speech"];
        //if(word.fields["proper"] == 1) {
        
        if( word.fields["proper"] == 1) {
            //Reading the Proper column of the database to determine if there's a proper noun.
            pos = "Proper_nouns"
        }
        // Add declension or conjugation to part of speech:
        if (pos == "Noun" || pos == "Adjective") {
            pos = pos+ ("_" + word.fields["decl"]);
        }
        else if (pos == "Verb") {
	    if (word.fields['conj'] != undefined) {
               pos = pos+ ("_" + word.fields["conj"]);
	    }
	}
        // Add word to existing POS array, else create a new array:
        if (words_data.hasOwnProperty(pos)) {
            words_data[pos].push(word);
        }    
        else {
            words_data[pos] = [word];
        }
    }
    return words_data;
}

/* Sets GLOBAL VAR words_metadata, containing parameters for Ajax call.
 * Called by inline script. */
function setVocabMetadata(lang, text, text_comp, bookslist, text_from, text_to, add_remove) {
    words_metadata = {"language":lang, "text":text, "text_comp":text_comp, "bookslist":bookslist, "text_from":text_from, "text_to":text_to, "add_remove":add_remove};
}


// Converts words_table (visible col.s only) to a CSV file.
// Column delimiter (usually \t or ,) specified by delimiter parameter.
function tableToCSV(delimiter) {
    // Get indices of currently visible columns:
    //var visible_cols = [];
    var cols = words_table.columns().visible();
    //console.log(words_table.columns().data())
    //console.log(cols)
    /*for (var i=0; i<cols.length; i+=1) {
        if (cols[i]) {
            visible_cols.push(i);
        }
    }*/
    var rowDelim = '\r\n';
    var docstring = "";
   // console.log(words_table)
    //console.log(words_table.rows())
    var header = ""
    $("#words_generated th").each(function() {
        header += $(this)[0].attributes['data-fieldname'].nodeValue + delimiter
         })
    docstring += header + rowDelim
    for (var i=0; i<words_table.rows()[0].length; i+=1) {
        for (var j=0; j<cols.length; j+=1) {
            if (cols[j]==true){
                //Previous person was doing alot of things with quotes that seemed silly - Dylan
                //docstring += '"'; // Begin CSV entry
                var ss = (""+words_table.cell({"row":  i,"column": j}).data());
               // console.log(ss)
                docstring += ss;
                docstring+=(delimiter); // Close CSV entry    
            }

        }
        docstring+=rowDelim; // End CSV row
    }
    return docstring;
}

function TableToTSV($table, filename) {

    var $rows = $table.find('tr:has(td)'),

        // Temporary delimiter characters unlikely to be typed by keyboard
        // This is to avoid accidentally splitting the actual contents
        tmpColDelim = String.fromCharCode(11), // vertical tab character
        tmpRowDelim = String.fromCharCode(0), // null character

        // actual delimiter characters for CSV format
        colDelim = '"\t"',
        rowDelim = '"\r\n"',

        // Grab text from table into CSV formatted string
        tsv = '"' + $rows.map(function(i, row) {
            var $row = $(row),
                $cols = $row.find('td');

            return $cols.map(function(j, col) {
                var $col = $(col),
                    text = $col.text();

                return text.replace('"', '""'); // escape double quotes

            }).get().join(tmpColDelim);

        }).get().join(tmpRowDelim)
        .split(tmpRowDelim).join(rowDelim)
        .split(tmpColDelim).join(colDelim) + '"',

        // Data URI
        tsvData = 'data:application/csv;charset=utf-8,' +
        encodeURIComponent(tsv);

    $(this)
        .attr({
            'download': filename,
            'href': tsvData,
            'target': '_blank'
        });
}


var tableToExcel = (function() {
    var uri = 'data:application/vnd.ms-excel;base64,',
        template =
        '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
        base64 = function(s) {
            return window.btoa(unescape(encodeURIComponent(s)))
        },
        format = function(s, c) {
            return s.replace(/{(\w+)}/g, function(m, p) {
                return c[p];
            })
        }
    return function(table, name, filename) {
        if (!table.nodeType) table = $("#words_generated");
        var ctx = {
            worksheet: name || 'Worksheet',
            table: table.innerHTML
        }

        $("#dlink").href = uri + base64(format(template, ctx));
        $("#dlink").download = filename;
        $("#dlink").click();

    }
})()

/* This function was copied from a Stack Overflow post! */
function getScrollbarWidth() {
    var outer = document.createElement("div");
    outer.style.visibility = "hidden";
    outer.style.width = "100px";
    outer.style.msOverflowStyle = "scrollbar"; // needed for WinJS apps

    document.body.appendChild(outer);

    var widthNoScroll = outer.offsetWidth;
    // force scrollbars
    outer.style.overflow = "scroll";

    // add innerdiv
    var inner = document.createElement("div");
    inner.style.width = "100%";
    outer.appendChild(inner);        

    var widthWithScroll = inner.offsetWidth;

    // remove divs
    outer.parentNode.removeChild(outer);

    return widthNoScroll - widthWithScroll;
}

  /*  $(window).resize( function() {
            if( $(window).width() >= ('992px') ) {
                $(".btn .btn-primary").each( function() {
                   $(this).css("font-size", ".8em");
                 });
            }
        
    }); */


  //$(".type_of_txt_btn_group label").on("click", function() {
    //  console.log("you clicked correctly");
      /*var label = $(this).attr('value');
      var buttoncomp = globalLang + "_" + ($(this).attr('id')) + "_DropDown";
      alert(buttoncomp);*/
  //})
