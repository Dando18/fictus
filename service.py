#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import re
from train import *
from scrape import *
import json

# takes the article title and returns the vote count formatted as
# (pos, neg, maybe). returns (0,0,0) if not in .dat file
def getVotes(title):
    title = title.replace(' ', '_')
    with open('votes.dat', 'r') as f:
        for line in f.readlines():
            if line.startswith(title):
                vals = line.split(' | ')
                return (vals[1], vals[2], vals[3].strip())
    return (0, 0, 0)

# increments the votes for title by (d0, d1, d3)
def incVotes(title, delta):
    title = title.replace(' ', '_')
    lines = []
    with open('votes.dat') as f:
        for line in f.readlines():
            vals = line.split(' | ')
            if line.startswith(title):
                vals[1] = str( int(vals[1]) + delta[0])
                vals[2] = str( int(vals[2]) + delta[1])
                vals[3] = str( int(vals[3]) + delta[2])
            lines += [vals]
    with open('votes.dat', 'w') as f:
        for line in lines:
            # convert line (tuple) to array of strings with map
            f.write(' | '.join(map(str,line)))


class Service(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def do_GET(self):
        self._set_headers()
        self.wfile.write('')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        
        # return value at end of POST
        ret = ''

        title = post_data['title']
        content = post_data['content']
        link = post_data['link']
        typ = post_data['type']

        base_url = re.sub(r'(http(s)?:\/\/)|(\/.*){1}', '', link)

        if typ == 'get':
            # return the amount of votes in that category
            votes = getVotes(title)
            title_pred = predict_title([title])[1]
            content_pred = predict_content([content])[1]
            ret = json.dumps( {'pos': votes[0], 'neg': votes[1],
                               'may': votes[1], 'title_prob': title_pred,
                               'content_prob': content_pred}
                               )
        elif typ == 'pos':
            # add a positive vote
            incVotes(title, (1,0,0))
        elif typ == 'neg':
            # add a negative vote
            incVotes(title, (0,1,0))
        elif typ == 'may':
            # add an unsure vote
            incVotes(title, (0,0,1))
        elif typ == 'getScrape':
            tmp = get_scrape_score(title, link, base_url, content)
            ret = json.dumps( {'scrape_rating': tmp })


        self._set_headers()
        self.wfile.write(ret)


port = 80
server_address = ('', port)
httpd = HTTPServer(server_address, Service)
try:
    print('starting server')
    httpd.serve_forever()
except KeyboardInterrupt:
    print('\n^C pressed. Killing HTTP server...')
    httpd.server_close()
