# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""

from difflib import SequenceMatcher
import pandas as pd
#import numpy as np

data = pd.read_csv('./data/craigslist_ny_listings_cleaned_20171029.csv', encoding='latin-1')

uniqPosters = list(data['Listed By Cleaned'].unique())
uniqPosters = [str(x) for x in uniqPosters]


def determine_similarity_score_list(key,searchList):
    qryList = list([str(x) for x in searchList if x != key])

    sortedTuples = []
    for result in qryList:
        ratio = SequenceMatcher(None, result, key).ratio()
        sortedTuples.append((result, ratio))
    
    return sorted(sortedTuples, key=lambda x: x[1],reverse=True)

def determine_top_match(key,searchList):
    scores = determine_similarity_score_list(key,searchList)
    return scores[0]

def determine_top_match_from_row(row,searchList):
    scores = determine_similarity_score_list(str(row['Listed By Cleaned']),searchList)
    return scores[0]

#testing the functions
determine_similarity_score_list('willhawkins',uniqPosters)
determine_top_match('willhawkins',uniqPosters)


#adding top element to dataframe as column(s)

data['SequenceMatcherResult'] = data.apply(determine_top_match_from_row,searchList=uniqPosters,axis=1)
data[['topMatch', 'score']] = data['SequenceMatcherResult'].apply(pd.Series)
#write to csv
data.to_csv('./data/craigslist_ny_listings_cleaned__Sequence_Match_20171029.csv')
