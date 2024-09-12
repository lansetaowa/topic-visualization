# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:31:20 2024

@author: elisa
"""

import jieba
from collections import Counter
import pandas as pd
import jieba.posseg as posseg
import numpy as np
import re
import string

# get a list of all cut words from original text
def list_all_words(df, text_col):
    
    cut = df[text_col].apply(lambda x: jieba.cut(x))
    
    # Generate all_words list using list comprehension
    all_words = [word for words in cut for word in words]
    
    # remove blanks
    pattern = '[\u4e00-\u9fa5a-zA-Z]+'
    all_words = [x for x in all_words if bool(re.search(pattern, str(x)))]
    
    return all_words

# generate frequency count, doc count and word property for each in all_word list
# returns a dataframe
def sort_freq(words_list, documents):
    
    sorted_frequency = sorted(Counter(words_list).items(), 
                              key=lambda x: x[1], 
                              reverse=True)
    
    sorted_frequency = pd.DataFrame(sorted_frequency, 
                                    columns=['word', 'term_freq'])
    
    sorted_frequency.dropna(inplace=True)

    # Convert documents to sets of words
    document_sets = [set(jieba.cut(doc)) for doc in documents]

    # Add document frequency column
    sorted_frequency['doc_freq'] = sorted_frequency['word'].apply(lambda x: sum(x in doc_set for doc_set in document_sets))

    # Add word property
    sorted_frequency['tag'] = sorted_frequency['word'].apply(lambda x: list(posseg.cut(x))[0].flag)
    
    return sorted_frequency

# generate frequency for each keyword once keywords are selected from word cut results
def count_keywords(text, keywords):
    
    counts = {keyword: text.count(keyword) for keyword in keywords}
    
    return pd.Series(counts)