'''
    this file is responsible for generating a prediction based
    upon prior news data
    it implements the method get_prediction(title, link, base_site, content)
'''
from train import *

def get_prediction(title, content):
    return predict_content(content)
