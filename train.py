'''
file for training model off of dataset
'''
import os.path

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib


def load():
    # news database is in data folder in cur directory
    data_file = './data/fake_or_real_news.csv'
    
    # read in four columns 
    # labels are FAKE or REAL
    # columns are   <blank>, title, text, label
    data = pd.read_csv(data_file)


def learn():
    if os.path.isfile('news_estimator.pkl'):
        gs_clf = joblib.load('news_estimator.pkl')
    else:
        # creates feature dictionary and processes stop-words
        text_clf = Pipeline([ ('vect', CountVectorizer()),
                              ('tfidf', TfidfTransformer()),
                              ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                    alpha=1e-3, random_state=42))
                              ])
        
        parameters = {'vect__ngram_range': [(1,1), (1,2)],
                      'tfidf__use_idf': (True, False),
                      'clf__alpha': (1e-2, 1e-3),
                      }
        gs_clf = GridSearchCV(text_clf, parameters, cv=5, iid=False, n_jobs=-1)
        gs_clf.fit(data['text'], data['label'])
        
        # save to pkl file
        joblib.dump(gs_clf.best_estimator_, 'news_estimator.pkl')


def predict(x):
    if gs_clf is None:
        gs_clf = joblib.load('news_estimator.pkl')
    return text_clf.predict(x)

