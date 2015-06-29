$(document).ready(function() {
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
            listItems = $("#textlist");

            var selects = $('textlist');
            var selectedValue = selects.val();
            if (selectedValue == "") {
                alert("Please choose a text.");
                return false;
            }
            if (validateTextSelect() == false) {
                alert("Please submit a valid range.");
                return false;
            }
            var pairs = [];
            console.log($('.range_select_box :input'));
            $('.range_select_box :input').each(function(i, div) {
                var i_over_2 = Math.floor(i / 2);
                if (!pairs[i_over_2]) pairs[i_over_2] =
                    $();
                pairs[i_over_2] = pairs[i_over_2].add(
                    div);
            });
            if (checkbooklist(pairs) == false) {
                alert("Please submit a valid range.");
                return false;
            }
        });

        //Function that allows the print button on words page to work
        function printData() {
            var divToPrint = $("#words_generated");
            newWin = window.open("");
            newWin.document.write(divToPrint.outerHTML);
            newWin.print();
            newWin.close();
        }
        //not sure if this one works
        $('#printSubmit').on('click', function() {
            printData();
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
        $('#Selection').on('click', function() {
            var selects = $('#textlist');
            var selectedValue = selects.val();
            console.log(selectedValue);
            if (selectedValue == "DCC Latin Core" ||
                selectedValue == "DCC Greek Core" ||
                selectedValue ==
                "Herodotus Book 1 Core (412 words > 10 times)") {
                $("#core_tip").css("display", "block");
                $("#other_tip").css("display", "none");
            } else {
                $("#core_tip").css("display", "none");
                $("other_tip").css("display", "block");
            }
        });

        /* EVENT HANDLERS FOR THE GIANT_FORM: */

        // Show/hide range select TOGGLE in a booklist thumbnail:
        $("#booklist .thumbnail :button").on("click", function() {
            var div = $(this).parent().find(
                ".range-select-toggle");
            if (div.css("display") == "none") {
                div.slideDown(100);
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
                //remove any hidden checkboxes to exclude this book from the form:
                $(".hiddencheck", this).remove();
            }

            // Build a list of selected book titles and insert into panel-contents:
            var headerStr = "";
            var books = $(".thumbnail :button :input");

            if (books.length == 1) {
                headerStr = $(books[0]).parent().attr("value");
            } else {
                books.each(function() {
                    var bookTitle = $(this).parent().attr(
                        "value");
                    // Shorted book titles to first 7 characters:
                    if (bookTitle.length >= 20) {
                        headerStr = headerStr +
                            bookTitle.substr(0, 20) +
                            "...,";
                    } else {
                        headerStr = headerStr +
                            bookTitle + ", ";
                    }
                });
            }
            headerStr = headerStr.substr(0, headerStr.length -
                4); //rmv trailing "...,"
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
                console.log(clicked.attr("val"));
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

        $("#greek").on("click", {
            language: "greek"
        }, configureForm);

        //TEXT ALL/SELECTION TOGGLE:
        $("#all_or_selection").on("click", function(e) {
            displayForm2(e.target);
        });

        $("#Selection").on("click", function(e) {
            displayForm2(e.target);
        });

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
        $("#textlist").on("click", function() {
            selectedText = $("#textlist").val();
            if ($("#tabTwo .panel-contents").text() !=
                selectedText.text) {
                $("#tabTwo .panel-contents").text(selectedText);
            }
            //Show panel-contents if it's hidden and contains text:
            if ($("#tabTwo .panel-contents").text() !== "" &&
                $("#tabTwo .panel-contents").css("display") ===
                "none") {
                $("#tabTwo .panel-contents").css("display",
                    "inline-block");
            }
        });
    } //END of event bindings for INDEX.HTML!


    /*===== Event bindings for WORDS_LIST.HTML and GREEK_WORDS_LIST.HTML =====*/
    else if ($("body").data("title") === "words_page") {
        //Check all checkboxes on reload:
        $(":checkbox").each(function() {
            $(this).prop("checked",true);
        });

        /* SLIDEOUT PANEL EVENT BINDINGS: */
        //show/hide filter panel:
        $("#slideout-pulltab").on("click",function(e) {
            var pulltab = $("#slideout-pulltab");
            var panel = $("#slideout-panel");
            var panel_width = panel.width();
            console.log("SLIDIN!");
            if (panel.data("state") === "stowed") {
                // animate panel and pulltab to open position
                pulltab.animate({
                    right: "250px"
                });
                panel.animate({
                    right: "0px"
                });

                panel.data("state","opened");
            }
            else {
                // animate panel and pulltab to STOWED position
                pulltab.animate({
                    right: "0px"
                });
                panel.animate({
                    right: "-250px"
                });
                
                panel.data("state","stowed");
            }
            
            // reverse the direction of the chevron glyphs:
            $("#pulltab .glyphicon")
                .toggleClass("glyphicon-chevron-right glyphicon-chevron-left");
        });

        //Slideout panel scroll control:
        $(window).scroll(function() {
            $("#slideout-panel").css("top", 
                Math.max(0, 265 - $(this).scrollTop()));
            
        });

        /* FILTERING/CHECKBOX BINDINGS: */
        // Filter Function
        $('.panel-body input:checkbox').click(function() {
            console.log("checkbox checked!");
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
            var word_data_filtered = filterWordData(filter_states);
            words_table.clear().draw();
            words_table.rows.add(word_data_filtered).draw();
            console.log(words_table.init);
            $("#cover").remove() //remove the gray div
        });

        $("#Verbs").on('click', function() {
            if ($("#Verbs").checked == true) {
                $('#Verb_1').prop('checked', true);
                $('#Verb_2').prop('checked', true);
                $('#Verb_3').prop('checked', true);
                $('#Verb_4').prop('checked', true);
                $('#irreg_verbs').prop('checked', true);
            } else {
                $('#Verb_1').prop('checked', false);
                $('#Verb_2').prop('checked', false);
                $('#Verb_3').prop('checked', false);
                $('#Verb_4').prop('checked', false);
                $('#irreg_verbs').prop('checked', false);
            }
        });

        $("#Nouns").on('click', function() {
            if ($("#Nouns").checked == true) {
                $('#Noun_1').prop('checked', true);
                $('#Noun_2').prop('checked', true);
                $('#Noun_3').prop('checked', true);
                $('#Noun_4').prop('checked', true);
                $('#Noun_5').prop('checked', true);
                $('#noun_irreg').prop('checked', true);
            } else {
                $('#Noun_1').prop('checked', false);
                $('#Noun_2').prop('checked', false);
                $('#Noun_3').prop('checked', false);
                $('#Noun_4').prop('checked', false);
                $('#Noun_5').prop('checked', false);
                $('#noun_irreg').prop('checked', false);
            }
        });

        $("#Adjectives").on('click', function() {
            if ($("#Adjectives").checked == true) {
                $('#Adjective_1').prop('checked', true);
                $('#Adjective_3').prop('checked', true);
                $('#adj_defective').prop('checked', true);
            } else {
                $('#Adjective_1').prop('checked', false);
                $('#Adjective_3').prop('checked', false);
                $('#adj_defective').prop('checked', false);
            }
        });

        //CHECK ALL filter bindings:
        $('#checkAll').click(function() {
            $(".POS").prop("checked", $("#checkAll").prop(
                "checked"));
        });

        $('#checkAllExcludes').click(function() {
            $(".Excludes").prop("checked", $(
                "#checkAllExcludes").prop("checked"));
        });

        $('#checkAll_greek').click(function() {
            $(".POS").prop("checked", $("#checkAll_greek").prop(
                "checked"));
        });

        $('#checkAllExcludes_greek').click(function() {
            $(".Excludes").prop("checked", $(
                "#checkAllExcludes_greek").prop(
                "checked"));
        });

        // This must be a hyperlink
        $(".tab_export").on('click', function(event) {
            // CSV
            exportTableToTSV.apply(this, [$('#words_generated'),
                'export.tsv'
            ]);

            // IF CSV, don't do event.preventDefault() or return false
            // We actually need this to be a typical hyperlink
        });
        
        // Gray out everything until words load:
        var panel = $('#big_wrap');
        var offset = panel.offset();
        var height = panel.height();
        var width = panel.width();
        $('#filters_panel').append('<div id=cover></div>');
        var new_panel = $('#big_cover');
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

        // Load words from server:
        var data; // JSON retrieved via AJAX
        console.log("SENDING AJAX REQUEST:");
        // AJAX request:
        var requestUrl= "/get_words/"+words_metadata.language+'/'+words_metadata.text+
            '/'+words_metadata.bookslist+'/'+words_metadata.text_from+
            '/'+words_metadata.text_to+'/'+words_metadata.add_remove+'/';
        $.getJSON(requestUrl)
            .done(function(receivedData) {
                words_data = loadWordData(receivedData);
                // Initialize DataTables object:
                var columns;
                if (words_metadata.language === "Greek") {
                    columns = [ 
                        {"data" : "fields.display_lemma"},
                        {"data" : "fields.english_definition"}
                        ]
                }
                else {
                    columns = [ 
                        {"data" : "fields.display_lemma"},
                        //{"data" : "fields.display_lemma_macronless"},
                        //{"data" : "fields.english_core"},
                        {"data" : "fields.english_extended"}
                        ]
                }
                var filter_states = determineFilterState();
                var word_data_filtered = filterWordData(filter_states);
                // Initialize DataTable object:
                words_table = $("#words_generated").DataTable({
                    "data" : word_data_filtered,
                    "columns" : columns
                });
                $("big_cover").remove();
            });
        console.log("AJAX REQUEST SUCCEEDED!");
        console.log("PARSED AJAX DATA INTO OBJECT.  SORTING...");
        
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
    var lang = e.data.language;
    // Set the redirect page to the appropriate lang:
    $("#giant_form").attr("action", "words_page_redirect/" + lang + "/");

    // Configure SOURCE TEXT TAB to only show texts from specified lang:
    var books = $("#textlist").find("[class$='book']");
    books = books.add($("#booklist").find("[class$='bookthumb']"));
    // Hide all text/book elements NOT part of the selected language:
    books.not("[class*='" + lang + "']").css("display", "none");
    // Show all which are part of the selected language:
    books.filter("[class*='" + lang + "']").css("display", "block");

    //Clear and hide panel-contents in SOURCE TEXT TAB:
    $("#headingTwo .panel-contents").text("");
    $("#headingTwo .panel-contents").css("display", "none");

    //Deselect any texts in the READ TEXT TAB: 
    //(selected texts have a checkbox :input child to their :button)
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

function userFormInteract(e) {
    var clickedTab = $(e.target).parents("[id^='tab']");
    if ((clickedTab.attr("id") != active_form_tab) && 
        ($("#giant_form").attr("action") != "")) {
        switchFormTabs($("#" + active_form_tab), clickedTab);
    } else {
        console.log("PLEASE SELECT A LANGUAGE FIRST!");
        $("headingOne").animate({
            opacity: 0.25
        }, 1000, function() {});
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
    current.find(".panel-title").css("color", "#428BCA");
    current.find(".panel-contents").css("color", "#428BCA");
    current.find(".panel-contents").css("border", "1px solid #428BCA");
    current.siblings(".collapse").collapse("hide");

    //Change next's tab header to look "active", and EXPAND it:
    next.find(".panel-heading").css("background-color", "#07325C");
    next.find(".panel-title").css("color", "#F1F1F1");
    next.find(".panel-contents").css("color", "#F1F1F1");
    next.find(".panel-contents").css("border", "1px solid #F1F1F1");
    next.siblings(".collapse").collapse("show");

    //Reflect this change in the active form tracking variable:
    active_form_tab = next.attr("id");
}

function showTip() {
    var selects = $('textlist');
    var selectedValue = selects.val();
    //Shows all or selection under textlist
    $('#all_or_selection').css("display", "block");

    if (selectedValue == "DCC Latin Core" ||
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

    }
}

// Makes sure that selection input is correct
function validateTextSelect() {
    var x = $("#text_from").value;
    var y = $("#text_to").value;

    if (x[0] == "." || y[0] == ".") {
        return false;
    } else if (x.split(".").length > 3 || y.split(".").length > 3) {
        return false;
    } else if (x.split(".")[0] > y.split(".")[0]) {
        return false;
    } else if (x.split(".")[0] == y.split(".")[0]) {
        if (x.split(".")[1] > y.split(".")[1]) {
            return false;
        } else if (x.split(".")[1] == y.split(".")[1]) {
            if (x.split(".")[2] > y.split(".")[2]) {
                return false;
            }
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
        $("#text_selection").slideUp(60);
        $("text_from").val("");
        $("text_to").val("");
        $("text_from").required = false;
        $("#text_to").required = false;
    } else if (btnText == "Selection") {
        $("#text_selection").slideDown(60);
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

// Shows all or selection for Nouns
function displayFormNoun(c) {
    if (c.checked) {
        $("#noun_box").css("display", "inline");
    } else {
        $("#noun_box").css("display", "none");
        $("#noun_decl_box").css("display", "none");
    }
}

// Shows all or selection for Adjectives
function displayFormAdj(c) {
    if (c.checked) {
        $("#adj_box").css("display", "inline");
    } else {
        $("#adj_box").css("display", "none");
        $("#adj_decl_box").css("display", "none");
    }
}

// Shows all or selection for Verbs
function displayFormVerb(c) {
    if (c.checked) {
        $("#verb_box").css("display", "inline");
    } else {
        $("#verb_box").css("display", "none");
        $("#verb_conj_box").css("display", "none");
    }
}

// Shows declension options for Nouns
function displayFormNounDecl(c) {
    if (c.value == "select_nouns") {
        $("#noun_decl_box").slideDown(80);
    } else if (c.value == "all_nouns") {
        $("#noun_decl_box").slideUp(80);
    }
}

// Shows declension options for Adjectives
function displayFormAdjDecl(c) {
    if (c.value == "select_adj") {
        $("#adj_decl_box").slideDown(80);

    } else if (c.value == "all_adj") {
        $("#adj_decl_box").slideUp(80);
    }
}

// Shows conjugation options for Verbs
function displayFormVerbConj(c) {
    if (c.value == "select_verbs") {
        $("#verb_conj_box").slideDown(80);
    }
    else if (c.value == "all_verbs") {
        $("#verb_conj_box").slideUp(80);
    }
}

function def_function() {
    if ($("#No definitions").checked == true) {
        hide_column(3);
        hide_column(4);
    } else if ($("#English-Core Definition").checked == true) {
        hide_column(4);
        show_column(3);
    } else if ($("#English-Extended Definition").checked == true) {
        hide_column(3);
        show_column(4);
    }
}

function greek_def_function() {
    if ($("#No definitions").checked == true) {
        hide_column(2);
    } else if ($("#English Definition").checked == true) {
        show_column(2);
    }
}

function lemma_function() {
    if ($("#Dictionary Entry (macron)").checked == true) {
        hide_column(2);
        show_column(1);
    } else {
        hide_column(1);
        show_column(2);
    }
}


function hide_column(a) {
    // if your table has header(th), use this
    $("#words_generated tbody td:nth-child(" + a + ")").hide();
    $("#words_generated thead th:nth-child(" + a + ")").hide();
}

function show_column(b) {
    // if your table has header(th), use this
    $("#words_generated tbody td:nth-child(" + b + ")").show();
    $("#words_generated thead th:nth-child(" + b + ")").show();
}


$('#backToTopBtn').click(function() {
    $('html,body').animate({
        scrollTop: 0
    }, 'slow');
    return false;
});


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

var $table = $('.table');
var $fixedColumn = $table.clone().insertBefore($table).addClass('fixed-column');

$fixedColumn.find('th:not(:first-child),td:not(:first-child)').remove();

$fixedColumn.find('tr').each(function(i, elem) {
    $(this).height($table.find('tr:eq(' + i + ')').height());
});

/* Determines which words to filter based on state of filter checkboxes.
 * Returns a list of the parts of speech whose words will be displayed. */
function determineFilterState() { 
            var included_pos = []; //which parts of speech are included
            // Determine which adj.+noun declensions and verb conjugations:
            var include_adjs = $("#Adjective").prop("checked");
            var all_adjs = $("#all_adj").prop("checked");
            $('#adj_decl_box :input').each(function() {
                if (include_adjs && (all_adjs || $(this).prop("checked"))) {
                    included_pos.push($(this).attr("id"));
                }
            });
            var include_nouns = $("#Nouns").prop("checked");
            var include_all_nouns= $("#all_nouns").prop("checked");
            $('#noun_decl_box :input').each(function() {
                if (include_nouns && (all_nouns || $(this).prop("checked"))) {
                    included_pos.push($(this).attr("id"));
                }
            });
            var include_verbs = $("#Verbs").prop("checked");
            var include_all_verbs = $("#all_verbs").prop("checked");
            $('#verb_conj_box :input').each(function() {
                if (include_verbs && (all_verbs || $(this).prop("checked"))) {
                    included_pos.push($(this).attr("id"));
                }
            });
            //Get other checkboxes' states:
            $('.panel-body input:checked')
                .not('[name$="_decl"]').not("[name='verb_conj']")
                .each(function() {
                included_pos.push($(this).attr("id"));
            });
            return included_pos;
}

/* Given array of word categories, returns an array of relevant wordTable objects.
 * wordTable objects are retrieved from word category arrays in words_data.*/
function filterWordData(pos_list) {
    var words_data_filtered = [];
    var words_data_keys = Object.getOwnPropertyNames(words_data);
    for (var i=0; i<words_data_keys.length; i++) {
        var key = words_data_keys[i];
        var key_index = pos_list.indexOf(key)
        if (key_index >=0) {
            words_data_filtered = words_data_filtered.concat(words_data[key]);
            pos_list.splice(key_index,1); //rm that key from pos_list
        }        
    }
    return words_data_filtered;
}

/* Sort array of words (as WordTables objects) by part of speech */
function loadWordData(data) {
    // Group word objects by filtering category:
    var words_data = {}; // Obj containing array of wordTables objects
    for (var i=0; i<data.length; i++) {
        var word = data[i];
        var pos = word.fields["part_of_speech"];
        // Add declension or conjugation to part of speech:
        if (pos == "Noun" || pos == "Adjective") {
            pos = pos+ ("_" + word.fields["decl"]);
        }
        else if (pos == "Verb") {
            pos = pos+ ("_" + word.fields["conj"]);
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
function setVocabMetadata(lang, text, bookslist, text_from, text_to, add_remove) {
    words_metadata = {"language":lang, "text":text, "bookslist":bookslist, "text_from":text_from, "text_to":text_to, "add_remove":add_remove};
    console.log("WORDS METADATA:");
    console.log(words_metadata);
}
