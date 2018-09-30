
var submit_btn = document.getElementById('submit_btn');
var vote_pos_btn = document.getElementById('vote_pos_btn');
var vote_neg_btn = document.getElementById('vote_neg_btn');
var vote_may_btn = document.getElementById('vote_may_btn');

var currentVote = "";

var finalRating = 0.0;
var titleRating = 0.0;
var contentRating = 0.0;
var voteRating = 0.0;
var scrapeRating = -1;


function clean(str) {
	return str.replace(/\s/g, '+').replace(/&/g, '%26')
}

function clamp(min, max, val) {
	return (val<min)?min:((val>max)?max:val);
}

function save() {
	// read in fields
	var title = document.getElementById('title').value;
    var link = document.getElementById('link').value;
	chrome.storage.sync.set({'title': title}, function(){});
	chrome.storage.sync.set({'link': link}, function(){});
}

function load() {
	chrome.storage.sync.get(['title'], function(result) {
		if (result.title) {
			document.querySelector('#title').parentNode.MaterialTextfield.change(result.title);
		}
	});
	chrome.storage.sync.get(['link'], function(result) {
		if (result.link) {
			document.querySelector('#link').parentNode.MaterialTextfield.change(result.link);
		}
	});
}

function updateTotal() {
	if (voteRating == -1) {
		finalRating = (0.3*scrapeRating + 0.5*contentRating + 0.2*titleRating);
	} else if (scrapeRating == -1) {
		finalRating = (0.4*voteRating + 0.4*contentRating + 0.2*titleRating);
	} else {
		finalRating = (0.2*voteRating + 0.3*scrapeRating + 0.2*titleRating + 0.3*contentRating);
	}

	document.getElementById('overall_rating').innerHTML = (100.0*finalRating).toFixed(3) + '%';

	if (finalRating > 0.65) {
		document.getElementById('overall_rating').style.color = 'green';
	} else if (finalRating > 0.45) {
		document.getElementById('overall_rating').style.color = '#ffad33';
	} else {
		document.getElementById('overall_rating').style.color = 'red';
	}
}


function setVotingButtonsDisabled(dis) {
	document.getElementById('vote_pos_btn').disabled = dis;
	document.getElementById('vote_neg_btn').disabled = dis;
	document.getElementById('vote_may_btn').disabled = dis;
}

function writeOutput(data) {
	document.getElementById('pos').innerHTML = data.pos;
	document.getElementById('neg').innerHTML = data.neg;
	document.getElementById('may').innerHTML = data.may;
	if (data.pos == 0 && data.neg == 0) {
		voteRating = -1;
	} else if (data.neg == 0) {
		voteRating = 1;
	} else {
		voteRating = (data.pos/data.neg / 2.0);
	}

	titleRating = data.title_prob;
	document.getElementById('title_prob').innerHTML = (100*data.title_prob).toFixed(3) + '%';
	if (data.title_prob > 0.65) {
		document.getElementById('title_prob').style.color = 'green';
	} else if (data.title_prob > 0.45) {
		document.getElementById('title_prob').style.color = '#ffad33';
	} else {
		document.getElementById('title_prob').style.color = 'red';
	}

	contentRating = data.content_prob;
	document.getElementById('content_prob').innerHTML = (100*data.content_prob).toFixed(3) + '%';
	if (data.content_prob > 0.65) {
		document.getElementById('content_prob').style.color = 'green';
	} else if (data.content_prob > 0.45) {
		document.getElementById('content_prob').style.color = '#ffad33';
	} else {
		document.getElementById('content_prob').style.color = 'red';
	}
	updateTotal();
}


submit_btn.addEventListener('click', function() {
	var title = clean(document.getElementById('title').value);
	var content = clean(document.getElementById('content').value);
	var link = document.getElementById('link').value;
	
	var data = {'title': title, 'link': link, 'content': content, 'type': 'get'};
	
	fetch('http://localhost:80', {
		method: 'POST',
		body: JSON.stringify(data),
	}).then(function(response) {
		if (response.status !== 200) {
			console.log('http error. status code: ' + response.status);
			return;
		}
		response.json().then(function(data) {
			// data is good and correct. make call to writeOutput
			writeOutput(data);
			setVotingButtonsDisabled(false);
			
			// create loading spindle
			document.getElementById('scrape_spinner').classList.add('is-active');
		});
	});
	
	var getScrape = {'title': title, 'link': link, 'content': content, 'type': 'getScrape'};
	fetch('http://localhost:80', {
		method: 'POST',
		body: JSON.stringify(getScrape),
	}).then(function(response) {
		if  (response.status !== 200) {
			return;
		}
		response.json().then(function(data) {
			var scr = clamp(0.0, 1.0, 2.5*data.scrape_rating);
			scrapeRating = scr;

			if (scr > 0.65) {
				document.getElementById('scrape_rating').style.color = 'green';
			} else if (scr > 0.45) {
				document.getElementById('scrape_rating').style.color = '#ffad33';
			} else {
				document.getElementById('scrape_rating').style.color = 'red';
			}

			document.getElementById('scrape_spinner').classList.remove('is-active');

			document.getElementById('scrape_rating').innerHTML = (100.0*scr).toFixed(3)+'%';

			updateTotal();
		});
	});
});

vote_pos_btn.addEventListener('click', function() {
	var title = clean(document.getElementById('title').value);
	var content = clean(document.getElementById('content').value);
	
	var data = {'title': title, 'content': content, 'type': 'pos'};
	
	fetch('http://localhost:80', {
		method: 'POST',
		body: JSON.stringify(data),
	}).then(function(response) {
		// increment the positive num in table
		var pos = document.getElementById('pos');
		pos.innerHTML = ''+(Number(pos.innerHTML)+1);
		setVotingButtonsDisabled(true);
	});
});

vote_neg_btn.addEventListener('click', function() {
	var title = clean(document.getElementById('title').value);
	var content = clean(document.getElementById('content').value);
	
	var data = {'title': title, 'content': content, 'type': 'neg'};
	
	fetch('http://localhost:80', {
		method: 'POST',
		body: JSON.stringify(data),
	}).then(function(response) {
		// increment the positive num in table
		var neg = document.getElementById('neg');
		neg.innerHTML = ''+(Number(neg.innerHTML)+1);
		setVotingButtonsDisabled(true);
	});
});

vote_may_btn.addEventListener('click', function() {
	var title = clean(document.getElementById('title').value);
	var content = clean(document.getElementById('content').value);
	
	var data = {'title': title, 'content': content, 'type': 'may'};
	
	fetch('http://localhost:80', {
		method: 'POST',
		body: JSON.stringify(data),
	}).then(function(response) {
		// increment the positive num in table
		var may = document.getElementById('may');
		may.innerHTML = ''+(Number(may.innerHTML)+1);
		setVotingButtonsDisabled(true);
	});
});

document.getElementById('title').addEventListener('keyup', save);
document.getElementById('content').addEventListener('keyup', save);
document.getElementById('link').addEventListener('keyup', save);


document.body.onload = function() {
	setVotingButtonsDisabled(true);
	
	load();

};

