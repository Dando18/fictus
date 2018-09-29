#!/usr/bin/env python
'''
    This file runs three different scoring algorithms
    1. linear classification (possibly CNN)
    2. scraping scoring algorithm
    3. user vote

'''
import sys
import re
from scrape import get_scrape_score
from prediction import get_prediction


def main():
    # from input get article title, link, site name, content
    if len(sys.argv) != 4:
        print("expected 3 arguments")
        exit(1)
    
    # initialize vars
    title = sys.argv[1]
    link = sys.argv[2]
    content_filename = sys.argv[3]

    # remove extra parts of link
    base_url = re.sub(r'(http(s)?:\/\/)|(\/.*){1}', '', link)
    print('\nbase_url = ' + base_url + '\n')

    # read content from content_file
    with open(content_filename, 'r') as content_file:
        content = content_file.read().replace('\n', '')


    # generate prediction from predict.py
    #prediction_score = get_prediction(title, link, base_url, content)

    # get score from scraper
    scrape_score = get_scrape_score(title, link, base_url, content)
    
    # get crowd evaluated score
    # crowd_score = get_crowd_score(title, link, content)

    # test print values
    print('scrape_score = ' + scrape_score)


# run main call
main()
