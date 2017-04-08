var schools;
var restaurants;
var tv_shows;
var athletes;

// load json data for presets into memory
$.getJSON("/results/schools", function(result) {
	schools = result;
});
$.getJSON("/results/restaurants", function(result) {
	restaurants = result;
});
$.getJSON("/results/shows", function(result) {
	tv_shows = result;
});
$.getJSON("/results/athletes", function(result) {
	athletes = result;
});

var results;

var rightArrowClass = "fa-angle-double-right";
var downArrowClass = "fa-angle-double-down";

var subjectNameId = "#subject-name";
var subjectDetailsId = "#subject-details";
var subjectArrowId = "#subject-name-arrow";

$(document).ready(function() {
	// listeners for each preset topic
	$("#load-university").click(function() {
		toggle_data(1);
	});
	$("#load-food").click(function() {
		toggle_data(2);
	});
	$("#load-tv").click(function() {
		toggle_data(3);
	});
	$("#load-sports").click(function() {
		toggle_data(4);
	});
	addListener();
	// $(".subject-name").click(function() {
	// 	var currentId = $(this).attr("id").slice(-1);
	// 	var currentsubjectDetailsId = subjectDetailsId + currentId;
	// 	var currentsubjectArrowId = subjectArrowId + currentId;
	// 	var currentDisplay = $(currentsubjectDetailsId).css("display");
	// 	// display data
	// 	if (currentDisplay == "none") {
	// 		$(currentsubjectArrowId).removeClass(rightArrowClass);
	// 		$(currentsubjectArrowId).addClass(downArrowClass);
	// 		$(currentsubjectDetailsId).css("display", "block");
	// 	} else { // hide data
	// 		$(currentsubjectArrowId).removeClass(downArrowClass);
	// 		$(currentsubjectArrowId).addClass(rightArrowClass);
	// 		$(currentsubjectDetailsId).css("display", "none");
	// 	}
	// });
});


var rightArrowClass = "fa-angle-double-right";
var downArrowClass = "fa-angle-double-down";

var subjectNameId = "#subject-name";
var subjectDetailsId = "#subject-details";
var subjectArrowId = "#subject-name-arrow";


// Closes the sidebar menu
$("#menu-close").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
});
// Opens the sidebar menu
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
});
// Scrolls to the selected menu item on the page
$(function() {
    $('a[href*=#]:not([href=#],[data-toggle],[data-target],[data-slide])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') || location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});
//#to-top button appears after scrolling
var fixed = false;
$(document).scroll(function() {
    if ($(this).scrollTop() > 250) {
        if (!fixed) {
            fixed = true;
            // $('#to-top').css({position:'fixed', display:'block'});
            $('#to-top').show("slow", function() {
                $('#to-top').css({
                    position: 'fixed',
                    display: 'block'
                });
            });
        }
    } else {
        if (fixed) {
            fixed = false;
            $('#to-top').hide("slow", function() {
                $('#to-top').css({
                    display: 'none'
                });
            });
        }
    }
});

var currentCollection = 0;

function toggle_data(collection) {
	// set results var to corresponding data to be displayed
	if (collection==1) {
		results = schools;
	} else if (collection==2) {
		results = restaurants;
	} else if (collection==3) {
		results = tv_shows;
	} else if (collection==4) {
		results = athletes;
	}
	if (collection!=currentCollection) {
		currentCollection = collection;
		// reset display container
		$("#data-display .container").empty();
		// iterate through results and generate the HTML based on the template
		for (var i=0; i<results.length; i++) {
			var thisTableHtml = tablesHtml.replace('subject-name-here', 'subject-name'+i);
			thisTableHtml = thisTableHtml.replace('subject-details-here', 'subject-details'+i);
			thisTableHtml = thisTableHtml.replace('graph-table-positive-here', 'graph-table-positive'+i);
			thisTableHtml = thisTableHtml.replace('graph-table-negative-here', 'graph-table-negative'+i);
			// add new HTML to page DOM
			$("#data-display .container").append(thisTableHtml);
		}
		
		addContent();
	    addListener();
	}
	
}

function addContent() {
	// call google charts API
	google.charts.load('current', {'packages':['table']});
    google.charts.setOnLoadCallback(drawTables);

    for (var i=0; i<results.length; i++) {
    	// Tables hidden to start
    	$(subjectDetailsId + i).css("display", "none");

	    var subject_name = results[i]['subject'];
	    // Put thumbs up or down based on score
	    var scoreIcon = "";
	    if (results[i].score>0) {
	    	scoreIcon = '<i class="fa fa-thumbs-o-up" aria-hidden="true"></i>';
	    } else {
	    	scoreIcon = '<i class="fa fa-thumbs-o-down" aria-hidden="true"></i>';
	    }
	    // Insert the score
	    $(subjectNameId + i).append("<h1 style='display:inline'>" + "<i class='fa fa-angle-double-right' aria-hidden='true' id='subject-name-arrow" + i + "'></i> " 
	    	+ subject_name + "</h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class='subject-score'>" + "<span style='color:yellow'>Score:</span> " 
	    	+ results[i].score + " " + scoreIcon + "</span>");
	    // Insert summary of tweet results
	    $(subjectDetailsId + i).prepend(
	    	"Positive tweets: " 
	    	+ results[i].positive.length + "<br>Negative tweets: "
	    	+ results[i].negative.length + "<br>Neutral tweets (Not counted): " 
	    	+ results[i].neutralCount + "<br><br>");
	    // Insert labels
	    $("#graph-table-positive" + i).before("<div>Most Impactful <em>Positive</em> Tweets</div>");
	    $("#graph-table-negative" + i).before("<div>Most Impactful <em>Negative</em> Tweets</div>");
    }
}

function addListener() {
	// add click listener
	// listener for a particular subject (eg. the walking dead, lebron james, etc.)
    $(".subject-name").click(function() {
		var currentId = $(this).attr("id").slice(-1);
		var currentsubjectDetailsId = subjectDetailsId + currentId;
		var currentsubjectArrowId = subjectArrowId + currentId;
		var currentDisplay = $(currentsubjectDetailsId).css("display");
		// Show data
		if (currentDisplay == "none") {
			$(currentsubjectArrowId).removeClass(rightArrowClass);
			$(currentsubjectArrowId).addClass(downArrowClass);
			$(currentsubjectDetailsId).css("display", "block");
		} else { // Hide data
			$(currentsubjectArrowId).removeClass(downArrowClass);
			$(currentsubjectArrowId).addClass(rightArrowClass);
			$(currentsubjectDetailsId).css("display", "none");
		}
	});
}

function drawTables() {
	// Draw positive and negative tweet tables for each search result
	for (var j=0; j<results.length; j++) {
		// Set columns
		var data = new google.visualization.DataTable();
		data.addColumn('string', 'User');
		data.addColumn('number', 'Followers');
		data.addColumn('string', 'Tweet');
		data.addColumn('string', 'Score');

		var data2 = new google.visualization.DataTable();
		data2.addColumn('string', 'User');
		data2.addColumn('number', 'Followers');
		data2.addColumn('string', 'Tweet');
		data2.addColumn('string', 'Score');
		// Display top 10 results in table
		for (var i=0; i<10; i++) {
			if (i<results[j].positive.length) data.addRow([results[j].positive[i].user, results[j].positive[i].followers, results[j].positive[i].tweet, results[j].positive[i].score]);
			if (i<results[j].negative.length) data2.addRow([results[j].negative[i].user, results[j].negative[i].followers, results[j].negative[i].tweet, results[j].negative[i].score]);
		}
		
		var table = new google.visualization.Table(document.getElementById('graph-table-positive' + j));
		var table2 = new google.visualization.Table(document.getElementById('graph-table-negative' + j));

		table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
		table2.draw(data2, {showRowNumber: true, width: '100%', height: '100%'});
	}
}


// HTML table display template
var tablesHtml = '<div id="subject-name-here" class="subject-name"></div><br><div id="subject-details-here"><div id="graph-table-positive-here"></div><br><div id="graph-table-negative-here"></div></div>'
