# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:07:17 2024

@author: elisa
"""

import re
import string

# replace useless separators and all to lower
def preprocess(text):
    # Define a list of common Chinese separators
    separators = ['，', '。', '！', '？', '、', '；','#','@','?','|']
    
    # Replace each separator with a space
    for sep in separators:
        text = str(text).replace(sep, '')
    
    text = text.lower()
        
    return text

