import re
from bs4 import BeautifulSoup
import urllib2
from urlparse import urlparse
from HTMLParser import HTMLParser

def get_scrape_score(articletitle, link, basesite, content):
    
    articletitle = articletitle.replace(' ', '+')

    search_url = "https://www.google.com/search?q=" + (articletitle) + "+-site%3A" + (basesite)
    request = urllib2.Request(search_url, None, {'User-Agent': 'Mozilla/5.0'})
    search_response = urllib2.urlopen(request).read()

    search_content = BeautifulSoup(search_response, "html.parser")
    
    #For article links
    alinks = []

    for l in search_content.find_all(class_='g'):
        for x in l.find_all('a'):
            g = x.get('href')
            g = g.replace('/url?q=','')
            g = g.replace('/search?=','')
            if "http://webcache.googleusercontent.com" in g:
                continue
            elif "/search?q=" in g:
                continue
            alinks.append(g)
            print (g)
    for i in range(0, len(alinks)):
        try:
            alink_url = alinks[i] 
            request = urllib2.Request(alink_url, None, {'User-Agent': 'Mozilla/5.0'})
            alink_response = urllib2.urlopen(request).read()
            alink_content = BeautifulSoup(alink_response, "html.parser")
            print (alink_content)
        except:
            continue


        
            
    return search_url

