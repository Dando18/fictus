
var submit_btn = document.getElementById('submit_btn');
var vote_pos_btn = document.getElementById('vote_pos_btn');
var vote_neg_btn = document.getElementById('vote_neg_btn');
var vote_may_btn = document.getElementById('vote_may_btn');

var currentVote = "";


function clean(str) {
	return str.replace(/\s/g, '+').replace(/&/g, '%26')
}


submit_btn.addEventListener('click', function() {
	var title = clean(document.getElementById('title').value);
	var content = clean(document.getElementById('content').value);

	/*
	var http = new XMLHttpRequest();
	var url = 'http://localhost:80';
	var params = 'title='+title+'&content='+content+'&type=get';
	http.open('POST', url, true);

	http.setRequestHeader('Content-Type', 'text/plain');

	http.onreadystatechange = function() {
		if (http.readyState == 4 && http.status == 200) {
			console.log(http.responseText);
		}
	}
	http.send(params);
	*/
	fetch('http://localhost:80', {
		method: 'POST',
		body: 'title='+title+'&content='+content+'&type=get'
	}).then(function(response) {
		console.log(response.text());
	});
	
});


