# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:45:09 2024

@author: elisa

Content: 
    1. read in and process original data and selected keywords
    2. fit correspondence analysis to keywords and dimension
    3. visualize the results from correspondence analysis
    
"""

import pandas as pd

from topic_visualization.preprocess import preprocess
from topic_visualization.count_word import count_keywords
from topic_visualization.correspondence_method import Correspondence_Viz
from topic_visualization.keywords_translation import *

import sys

data_dir = 'sample\sample_input'
output_dir = 'sample\sample_output'
data_name = 'probiotics posts by brand.xlsx'
selected_name = 'probiotics word cut.xlsx'

dim = 'brand'
value = 'keywords'

# read in data and rename columns
df = pd.read_excel(data_dir + '\\'+ data_name)
df.columns = [dim, 'content']

# read in selected key words, indicated by "flag=1"
# selected words are output from the word count step
selected = pd.read_excel(output_dir + '\\'+selected_name)
selected_words = selected[(selected['flag']==1)&(selected['term_freq']>=100)&(selected['doc_freq']>=100)]['word'].to_list()

# preprocess content column
df['content_processed'] = df['content'].apply(preprocess)


# Apply the function to the text_column and join the resulting counts to the dataframe
counts = df['content_processed'].apply(count_keywords, 
                                       keywords = selected_words)

counts = pd.concat([counts, df[dim]], 
                   axis=1)

# pvt is the table ready for CA analysis
pvt = counts.groupby(dim).sum()

# translate Chinese columns into English for better understanding
pvt.rename(columns = keywords_trans, inplace=True)

# initialize the class for correspondence analysis
ca_viz = Correspondence_Viz(value_var = 'keywords',
                                      dim_var = 'brand',
                                      input_df = pvt)

table_for_ca = ca_viz.table_for_ca(pvt)

# fit Correspondence Analysis
ca_results = ca_viz.fit_ca(table_for_ca)
ca_results.to_excel(output_dir + '\\' + 'ca_coord.xlsx', index=False)

# visualize results and output images
ca_viz.visualize_ca(ca_results, 
                    chart_title = 'keywords by probiotic brands', 
                    output_dir = output_dir, 
                    output_name = 'Correspondence Analysis - probiotic by brands')




