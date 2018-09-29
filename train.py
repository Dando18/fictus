'''
file for training model off of dataset
'''
import os.path

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib


'''
    Takes an input array of strings. It will predict FAKE or REAL for each text input.
    returns  array or FAKE/REAL's
'''
def predict_content(x):
    if os.path.isfile('./data/content_estimator.pkl'):
        gs_clf = joblib.load('./data/content_estimator.pkl')
    else:
        # news database is in data folder in cur directory
        data_file = './data/fake_or_real_news.csv'
        
        # read in four columns 
        # labels are FAKE or REAL
        # columns are   <blank>, title, text, label
        data = pd.read_csv(data_file)
        # creates feature dictionary and processes stop-words
        text_clf = Pipeline([ ('vect', CountVectorizer()),
                              ('tfidf', TfidfTransformer()),
                              ('clf', SGDClassifier(loss='log', penalty='l2',
                                                    alpha=1e-3, random_state=42,
                                                    max_iter=50, tol=None))
                              ])
        
        parameters = {'vect__ngram_range': [(1,1), (1,2)],
                'tfidf__use_idf': (True, False),
                      'clf__alpha': (1e-2, 1e-3),
                      }
        gs_clf = GridSearchCV(text_clf, parameters, cv=5, iid=False, n_jobs=-1)
        gs_clf.fit(data['text'], data['label'])
        
        # save to pkl file
        joblib.dump(gs_clf.best_estimator_, './data/content_estimator.pkl')

    prob = gs_clf.predict_proba(x)[0]
    return (prob[0], prob[1])


''' 
    predicts the based on the article title
'''
def predict_title(x):
    if os.path.isfile('./data/title_estimator.pkl'):
        gs_clf = joblib.load('./data/title_estimator.pkl')
    else:
        # path to data
        data_file = './data/fake_or_real_news.csv'

        # read in <blank>, title, text, label shaped csv
        data = pd.read_csv(data_file)
        text_clf = Pipeline([ ('vect', CountVectorizer()),
                              ('tfidf', TfidfTransformer()),
                              ('clf', SGDClassifier(loss='log', penalty='l2',
                                                    alpha=1e-3, random_state=42,
                                                    max_iter=1000, tol=None))
                              ])

        parameters = {'vect__ngram_range': [(1,1), (1,2)],
                      'tfidf__use_idf': (True, False),
                      'clf__alpha': (1e-2, 1e-3),
                      }
        gs_clf = GridSearchCV(text_clf, parameters, cv=5, iid=False, n_jobs=-1)
        gs_clf.fit(data['title'], data['label'])

        joblib.dump(gs_clf.best_estimator_, './data/title_estimator.pkl')
    
    prob = gs_clf.predict_proba(x)[0]
    return (prob[0], prob[1])

