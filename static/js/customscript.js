var results;

var rightArrowClass = "fa-angle-double-right";
var downArrowClass = "fa-angle-double-down";

var subjectNameId = "#subject-name";
var subjectDetailsId = "#subject-details";
var subjectArrowId = "#subject-name-arrow";

var bubblesId = "#bubbles-";
var tablesId = "#tables-";

$(document).ready(function(){
    // load saved data from db
	$.getJSON("/get-custom-data", function(result) {
		results = result;
		displayData();
	});

	$("#refresh").click(function(){
		displayData();
	})

	// data loading code
	$("#submit-btn").click(function(){
		var query = $("input[name=query]").val();
		if (query!="") {
		    // sanitize input
		    query = query.replace(/[^0-9a-z -]/gi, '')
		    // display loading spinner
			$("#loader").css("display", "block");
			$.getJSON("/load-custom-data/" + query, function(result) {
				$("#loader").css("display", "none");
				// refresh display
				$.getJSON("/get-custom-data", function(result) {
					results = result;
					displayData();
				});
			});
		}
	});
});
function displayData() {
	if (results!=null) {
		writeHtml();
		addHtmlContent();
		setListeners();
	}
}
function writeHtml() {
	// Reset display container
	$("#data-display .container").empty();
	// Fill in variable names
	for (var i=0; i<results.length; i++) {
		var thisTableHtml = tablesHtml.replace('subject-name-here', 'subject-name'+i);
		thisTableHtml = thisTableHtml.replace('subject-details-here', 'subject-details'+i);
		thisTableHtml = thisTableHtml.replace('bubbles-id-here', 'bubbles-'+i);
		thisTableHtml = thisTableHtml.replace('tables-id-here', 'tables-'+i);
		thisTableHtml = thisTableHtml.replace('graph-table-positive-here', 'graph-table-positive'+i);
		thisTableHtml = thisTableHtml.replace('graph-table-negative-here', 'graph-table-negative'+i);
		thisTableHtml = thisTableHtml + "<br><br>";
		// Add html to container
		$("#data-display .container").append(thisTableHtml);
	}
}

function addHtmlContent() {
	// Draw tables with Google Charts API
	google.charts.load('current', {'packages':['table']});
	google.charts.setOnLoadCallback(drawTables);
	// Fill in speech bubbles
	addBubbles();
	// Insert additional details for each query
	for (var i=0; i<results.length; i++) {
		// Hide data to start
		$(subjectDetailsId + i).css("display", "none");
		$(tablesId + i).css("display", "none");

	    var subject_name = results[i]['subject'];
	    // Add thumbs up or thumbs down based on score
	    var scoreIcon = "";
	    if (results[i].score>0) {
	    	scoreIcon = '<i class="fa fa-thumbs-o-up" aria-hidden="true"></i>';
	    } else {
	    	scoreIcon = '<i class="fa fa-thumbs-o-down" aria-hidden="true"></i>';
	    }
	    // Insert the score
	    $(subjectNameId + i).append("<h1 style='display:inline'>" + "<i class='fa fa-angle-double-right' aria-hidden='true' id='subject-name-arrow" + i + "'></i> " 
	    	+ subject_name + "</h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class='subject-score'>" + "<span style='color:orange'>Score:</span> " 
	    	+ results[i].score + " " + scoreIcon + "</span>");
	    // Insert summary of tweet results
	    $(subjectDetailsId + i).prepend(
	    	"Positive tweets: " 
	    	+ results[i].positive.length + "<br>Negative tweets: "
	    	+ results[i].negative.length + "<br>Neutral tweets (Not counted): " 
	    	+ results[i].neutralCount + "<br><br>");
	    // Add view setters
	    $(subjectDetailsId + i).prepend(viewSetterHtml.replace('bubbles-view-btn', 'bubbles-view-btn'+i).replace('tables-view-btn','tables-view-btn'+i));
	    // Add labels
	    $("#graph-table-positive" + i).before("<div>Most Impactful <em>Positive</em> Tweets</div>");
	    $("#graph-table-negative" + i).before("<div>Most Impactful <em>Negative</em> Tweets</div>");
	}
}

function addBubbles() {
	for (var j=0; j<results.length; j++) {
		var speechBubblesHtml = "<div>Most Impactful Tweets</div>";

		var thisBubbleHtml = bubblesHtml.replace('TRIANGLE_CLASS_HERE', 'triangle-positive');
		thisBubbleHtml = thisBubbleHtml.replace('speech-details', 'speech-details-positive');
		thisBubbleHtml = thisBubbleHtml.replace('TWEET_HERE', results[j].positive[0].tweet);
		thisBubbleHtml = thisBubbleHtml.replace(/USERNAME_HERE/g, results[j].positive[0].user);
		thisBubbleHtml = thisBubbleHtml.replace('FOLLOWERS_HERE', results[j].positive[0].followers);
		thisBubbleHtml = thisBubbleHtml.replace('SCORE_HERE', results[j].positive[0].score);
		speechBubblesHtml = speechBubblesHtml + thisBubbleHtml;

		var thisBubbleHtml = bubblesHtml.replace('TRIANGLE_CLASS_HERE', 'triangle-negative');
		thisBubbleHtml = thisBubbleHtml.replace('speech-details', 'speech-details-negative');
		thisBubbleHtml = thisBubbleHtml.replace('TWEET_HERE', results[j].negative[0].tweet);
		thisBubbleHtml = thisBubbleHtml.replace(/USERNAME_HERE/g, results[j].negative[0].user);
		thisBubbleHtml = thisBubbleHtml.replace('FOLLOWERS_HERE', results[j].negative[0].followers);
		thisBubbleHtml = thisBubbleHtml.replace('SCORE_HERE', results[j].negative[0].score);
		speechBubblesHtml = speechBubblesHtml + thisBubbleHtml;

		// insert into HTML
		$(bubblesId + j).html(speechBubblesHtml);
	}
}

function setListeners() {
	// add click listener
	$(".subject-name").click(function() {
		var currentId = $(this).attr("id").slice(-1);
		var currentsubjectDetailsId = subjectDetailsId + currentId;
		var currentsubjectArrowId = subjectArrowId + currentId;
		var currentDisplay = $(currentsubjectDetailsId).css("display");
		// Show details
		if (currentDisplay == "none") {
			$(currentsubjectArrowId).removeClass(rightArrowClass);
			$(currentsubjectArrowId).addClass(downArrowClass);
			$(currentsubjectDetailsId).css("display", "block");
		} // Hide details
		else {
			$(currentsubjectArrowId).removeClass(downArrowClass);
			$(currentsubjectArrowId).addClass(rightArrowClass);
			$(currentsubjectDetailsId).css("display", "none");
		}
		
	});
	// Change to speech bubbles view
	$(".bubbles-btn").click(function() {
		var currentId = $(this).attr("id").slice(-1);
		var currentBubblesId = bubblesId + currentId;
		var currentTablesId = tablesId + currentId;
		var currentDisplay = $(currentBubblesId).css("display");
		if (currentDisplay == "none") {
			$(currentTablesId).css("display", "none");
			$(currentBubblesId).css("display", "block");
		}
	});
	// Change to tables view
	$(".tables-btn").click(function() {
		var currentId = $(this).attr("id").slice(-1);
		var currentBubblesId = bubblesId + currentId;
		var currentTablesId = tablesId + currentId;
		var currentDisplay = $(currentTablesId).css("display");
		if (currentDisplay == "none") {
			$(currentBubblesId).css("display", "none");
			$(currentTablesId).css("display", "block");
		}
	});
}

function drawTables() {
	// Draw positive and negative tweets tables
	for (var j=0; j<results.length; j++) {
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

// HTML display templates
var viewSetterHtml = '<div class="view-setter">Display Mode:<br><span class="bubbles-btn" id="bubbles-view-btn">Bubbles</span> &nbsp; | &nbsp; <span class="tables-btn" id="tables-view-btn">Tables</span></div><br><br>'
var bubblesHtml = '<div class="speechcontainer"><p class="triangle-border TRIANGLE_CLASS_HERE">TWEET_HERE</p><a class="twitter-user" href="https://twitter.com/USERNAME_HERE" target="_blank">USERNAME_HERE</a><span class="speech-details">Followers: FOLLOWERS_HERE &nbsp;&nbsp; Score: SCORE_HERE</span></div>'
var tablesHtml = '<div id="subject-name-here" class="subject-name"></div><br><div id="subject-details-here"><div id="bubbles-id-here"></div><div id="tables-id-here"><div id="graph-table-positive-here"></div><br><div id="graph-table-negative-here"></div><br><br></div></div>'
