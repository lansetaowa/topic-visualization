# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 21:44:04 2024

@author: elisa
"""

import pandas as pd

from topic_visualization.preprocess import preprocess
from topic_visualization.count_word import list_all_words, sort_freq

data_dir = 'sample\sample_input'
output_dir = 'sample\sample_output'
data_name = 'probiotics posts by brand.xlsx'
output_name = 'probiotics word cut.xlsx'

# read in data and rename columns
df = pd.read_excel(data_dir + '\\'+ data_name)
df.columns = ['brand', 'content']

# Apply the replace_separators function to the 'text' column
df['content_processed'] = df['content'].apply(preprocess)

# all words after word cut process
all_words = list_all_words(df, 'content_processed') # this step might be slow

# word cut final results with freq, doc freq and word property
sorted_frequency = sort_freq(all_words, 
                             df['content_processed'])

# this step of flagging interesting words is done manually with business consulting sense
# just for illustration purpose, I'll just flag the words that have been selected
selection = [
    "益生菌",
"维生素",
"便秘",
"孕期",
"减肥",
"肠道",
"营养",
"乳酸菌",
"饮食",
"皮肤",
"孕妇",
"调理",
"医生",
"熬夜",
"早餐",
"解酒",
"怀孕",
"胀气",
"活性",
"脂肪",
"胶囊",
"酸奶",
"腹泻",
"排便",
"备孕",
"蔬菜",
"养胃",
"智商",
"过敏",
"美白",
"饭后",
"平衡",
"软糖",
"压力",
"饮料",
"敏感",
"酵素",
"气色",
"抗氧化",
"脾胃",
"修复",
"哺乳期",
"发育",
"感冒",
"蛋白质",
"排毒",
"碳水",
"发酵",
"鼻炎",
"抗老",
"情绪",
"炎症",
"失眠",
"掉秤",
"抗炎",
"即食",
"腹胀",
"激素",
"咳嗽",
"口臭"
]

sorted_frequency['flag'] = sorted_frequency['word'].apply(lambda x: 1 if x in selection else 0)

# output word cut results for review 
# this is also the input for next step correspondence analysis
sorted_frequency.to_excel(output_dir + '\\' + output_name, index=False)

