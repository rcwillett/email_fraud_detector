# ContentTransformer.py Module
# ---------------------------------------------------------------
# This module has been built to accept a text input and
# tranform it into a data frame which can be accepted by
# simple models as input to predict whether the content is
# fraudulent

# Import matrix manipulation libraries
import pandas as pd
import numpy as np
# Import processing libraries
from sklearn.compose import ColumnTransformer
# Import count vectorizer
from sklearn.feature_extraction.text import CountVectorizer
# Import pickler
import pickle
# Import regex
import re
# Import custom text transformers
from TextTransformers import extract_HTML_text, get_word_count, extract_text_content
# Import custom tokenizer for column vectorizer
from Tokenizer import custom_tokenizer

# Load column transformer model to use text to input vector function
with open('./models/count_vec_col_transf.pkl', 'rb') as handle:
    column_transformer = pickle.load(handle)

# Define text to input transformer so text data can be fed into simple models
def Transform_Text_To_Input_Vector (text):
    '''
    Accepts a string and returns a data frame with content formatted for input into a trained model
    
    Parameters
    ----------
    text: A string which needs to be transformed into a format consumable by a model
    
    Returns
    ----------
    Ret: A pandas data frame which can be passed into a trained model for consumption
    '''
    # Ensure input is text
    assert type(text) == str, 'Input must be a string'
    # Count insecure links
    insecure_link_count = text.count('http://')
    # Count secure links
    secure_link_count = text.count('https://')
    # Check if content contains telltale html characters
    if '</' in text:
        # Exract text content from HTML
        text = extract_HTML_text(text)
    # Get number count
    number_count = len(re.findall(r'\d+', text))
    # Get english words only from text
    english_only_text = extract_text_content(text)
    # Get word count
    word_count = len(english_only_text.split(' '))
    # Initialize pandas data frame
    result_df = pd.DataFrame({
        'content': [english_only_text],
        'unsecure_link_count': [insecure_link_count],
        'secure_link_count': [secure_link_count],
        'numbers_count': [number_count],
        'word_count': [word_count],
    })

    # Return count vectorized data frame
    return column_transformer.transform(result_df)