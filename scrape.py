import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib2
from urlparse import urlparse
from HTMLParser import HTMLParser
from difflib import SequenceMatcher

#Not sure what this function does; works with the one below it
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta' '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

#Gets the pure text from the articles' bodies
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
    
    #gets all of the URL's of the articles on the Google search page
    for l in search_content.find_all(class_='g'):
        for x in l.find_all('a'):
            g = x.get('href')
            g = g.replace('/url?q=','')
            g = g.replace('/search?=','')
            #Takes out the articles that contain these elements; does not append to alinks
            if g.startswith("http://webcache.googleusercontent.com"):
                continue
            elif g.startswith("/search?q="):
                continue
            alinks.append(g)
    #Words that need to be taken out in order to highlight key words
    stop_words= ['a', 'above','the', 'again', 'all', 'an', 'any', 'as', 'be', 'been', 'being', 'between', 'but', 'could', 'do', 'doing', 'during', 'few', 'from', 'had', 'have', 'he', 'her', "here's", "he'll", "herself", "himself", "how", "I", "I'll", "I've", "in", "is", "it's", "itself", "me", 'most', 'myself', 'of', 'once', 'or', 'ought', 'ours', 'out', 'own', "she'll", 'she', 'should', 'some', 'than', "that's", "their", 'them', "there's", "they'll", "they've", 'those', 'to', 'under', 'up', 'was', "we'd", "we're", 'were', "what's", "when's", "where's", "while", "who's", 'why', 'with', 'you', "you'll", "you've", 'yours', 'yourselves', 'about', 'after', 'against', 'am', 'and', 'are', 'at', 'because', 'before', 'both', 'by', 'did', 'does', 'down', 'each', 'for', 'further', 'has', 'having', "he'd", "he's", 'here', 'hers', 'him', 'his', "how's", "I'd", "I'm", 'if', 'into', 'it', 'its', "let's", 'more', 'my', 'nor', 'on', 'only', 'other', 'our', 'ourselves', 'over', 'same', "she'd", "she's", 'so', 'such', 'that', 'theirs', 'themselves', 'there', 'these', "they'd", "they're", 'this', 'through', 'too', 'until', 'very', 'we', "we'll", "we've", 'what', 'when', 'where', 'which', 'who', 'whom', "why's", 'would', "you'd", "you're", 'your', 'yourself']

    #Initializing list for articles to compare to original
    comparison_articles = []

    #Goes through the links of articles from Google page to get article content out of the body of the html
    for i in range(0, len(alinks)):

        #If the link can be accessed from the Google page, continue to find body
        try:
            alink_url = alinks[i] 
            request = urllib2.Request(alink_url, None, {'User-Agent': 'Mozilla/5.0'})
            alink_response = urllib2.urlopen(request).read()
            #alink_content = BeautifulSoup(alink_response, "html.parser")
        except:
            continue

        #Finds the body of alink_content
        alink_content = text_from_html(alink_response)

        #Takes out the stop words in the content of each article
        for word in stop_words:
            filtered_content = alink_content.replace(' ' + word + ' ', ' ')
        
        #Appends the filtered content to list comparison_articles 
        comparison_articles.append(filtered_content)
    
    #Take out stop words in original given content
    for word in stop_words:
        content = content.replace(' ' + word + ' ', ' ')

    
    #Dictionary to store all of the occurences of each word
    content_dict = {}

    #This is the list of the words in content
    split_content = content.split()

    #(total other articles)
    total_oa = 0
    print('beginning word hunt')
    #iterating through split_content to check each word individually
    for word in split_content:
        inDict = word not in content_dict
        #for (article content); to check through the list of comparison articles to get each out 
        for ac in comparison_articles:
            total_oa += ac.count(' ')+1
            #Seeing if any of the words are in the comparison article
            if inDict:
                content_dict[word] = ac.count(word)
            #If it is in the dictionary, increment the occurence in this article
            else:
                content_dict[word] += ac.count(word)
    
    total_content = 0

    #Sum all of the occurences of the words altogether
    for key in content_dict:
        total_content += content_dict[key]

    return ((1.0 * total_content * len(split_content)) /(1.0 * total_oa))

