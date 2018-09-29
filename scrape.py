import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib2
from urlparse import urlparse
from HTMLParser import HTMLParser

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta' '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.find_all(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

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

    stop_words= ['a', 'above', 'again', 'all', 'an', 'any', 'as', 'be', 'been', 'being', 'between', 'but', 'could', 'do', 'doing', 'during', 'few', 'from', 'had', 'have', 'he', 'her', "here's", "he'll", "herself", "himself", "how", "I", "I'll", "I've", "in", "is", "it's", "itself", "me", 'most', 'myself', 'of', 'once', 'or', 'ought', 'ours', 'out', 'own', "she'll", 'she', 'should', 'some', 'than', "that's", "their", 'them', "there's", "they'll", "they've", 'those', 'to', 'under', 'up', 'was', "we'd", "we're", 'were', "what's", "when's", "where's", "while", "who's", 'why', 'with', 'you', "you'll", "you've", 'yours', 'yourselves', 'about', 'after', 'against', 'am', 'and', 'are', 'at', 'because', 'before', 'both', 'by', 'did', 'does', 'down', 'each', 'for' 'further', 'has', 'having', "he'd", "he's", 'here', 'hers', 'him', 'his', "how's", "I'd", "I'm", 'if', 'into', 'it', 'its', "let's", 'more', 'my', 'nor', 'on', 'only', 'other', 'our', 'ourselves', 'over', 'same', "she'd", "she's", 'so', 'such', 'that', 'theirs', 'themselves', 'there', 'these', "they'd", "they're", 'this', 'through', 'too', 'until', 'very', 'we', "we'll", "we've", 'what', 'when', 'where', 'which', 'who', 'whom', "why's", 'would', "you'd", "you're", 'your', 'yourself']
    comparison_articles = []
    for i in range(0, len(alinks)):
        try:
            alink_url = alinks[i] 
            request = urllib2.Request(alink_url, None, {'User-Agent': 'Mozilla/5.0'})
            alink_response = urllib2.urlopen(request).read()
            alink_content = BeautifulSoup(alink_response, "html.parser")
        except:
            continue

        #Finds the body of alink_content
        alink_content = text_from_html(alink_response)

        for word in stop_words:
            alink_content.replace(word, '')

        comparison_articles.append(alink_content)
            
    return alink_content

