# Import data science libraries
import pandas as pd
import numpy as np
# Import regex library
import re
# Import BeautifulSoup for HTML parsing and handling
from bs4 import BeautifulSoup
# Import NLTK for natural language processing
import nltk
# Import processing libraries
from sklearn.compose import ColumnTransformer
# Import count vectorizer
from sklearn.feature_extraction.text import CountVectorizer
# Import pickler
import pickle
# Import tokenizer
from Tokenizer import custom_tokenizer


# Download the NLTK punctuation package
nltk.download('punkt')
# Download the NLTK english words package
nltk.download('words')
# Create a set containing all the english words from the NLTK corpus
nltk_eng_words = set(nltk.corpus.words.words())

# Defines a function to extract text content from strings with HTML
def extract_HTML_text(html):
    '''
    Accepts text content containing HTML and returns only the text content of the HMTML
    
    Parameters
    ----------
    html: A string which contains HTML encoded content
    
    Returns
    ----------
    Ret: A string which contains only the text from the HTML encoded content
    
    Example
    ----------
    >>>> extract_HTML_text('<div>Text</div>')
    Text
    '''
    # Instantiate a BeautifulSoup object from the html string using BeautifulSoup
    soup = BeautifulSoup(html, features="html.parser")
    # Return the text content of the soupified html content
    return soup.get_text()

# Instantiate function to get word count in a string
def get_word_count(text):
    '''
    Accepts a string and returns the number of words contained in that string
    
    Parameters
    ----------
    text: A string which contains words to be counted
    
    Returns
    ----------
    Ret: An integer of the number of words contained in that string
    
    Example
    ----------
    >>>> get_word_count('goodbye cruel world')
    3
    '''
    # Filter string to alphabetical characters and spaces only
    alpha_only_text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove any instances of repeated spaces
    no_space_alpha_text = re.sub(r'\s\s+', ' ', text)
    # split sentence into words by splitting on spaces
    listofwords = alpha_only_text.split(' ')
    # Return the length of the resulting word list
    return len(listofwords)

# Instantiate a function to clean the text content of emails
def extract_text_content (text):
    '''
    Accepts a string, filters non-alphabetical characters and non-english words and returns the resulting string
    
    Parameters
    ----------
    text: A string which needs to be filtered
    
    Returns
    ----------
    Ret: A string which contains only english words
    
    Example
    ----------
    >>>> extract_text_content('asjudehr hello_ 712753^!@54318 world!')
    hello world
    '''
    # Removes any '=2C' strings from the text (This appears in certain text encodings between words)
    filteredText = text.replace('=2C', '')
    # Filters out any non-alphabetical or space characters from the text
    characterFilteredText = re.sub(r'[^a-zA-Z\s]', ' ', filteredText)
    # Instantiates an array to contain the english words
    englishWordOnlyTextArr = []
    # Iterate over every word in the string picked up by the NLTK tokenizer
    for word in nltk.word_tokenize(characterFilteredText):
        # Set the word to lower case
        lower_word = word.lower()
        # Check if the word exists in the set of english words and has a length > 1
        # And append the word the english word array if so
        if lower_word in nltk_eng_words and len(word) > 1:
            englishWordOnlyTextArr.append(word)
        # If the word is only one character check if it is one of the two english words of one character
        # If so, append the word to the english word array
        elif lower_word == 'i' or lower_word == 'a':
            englishWordOnlyTextArr.append(word)
    # Return the english word arrray of the content joined by spaces
    return ' '.join(englishWordOnlyTextArr)

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
    # Count insecure links
    insecure_link_count = text.count('http://')
    # Count secure links
    secure_link_count = text.count('https://')
    # Get number count
    number_count = len(re.findall(r'\d+', text))
    # Get english words only from text
    english_only_text = extract_text_content(text)
    # Get word count
    word_count = len(english_only_text.split(' '))
    # Initialize pandas data frame
    result_df = pd.DataFrame({
        'content': english_only_text,
        'unsecure_link_count': insecure_link_count,
        'secure_link_count': secure_link_count,
        'numbers_count': number_count,
        'word_count': word_count,
    },
    index=[0])

    # Return count vectorized data frame
    return column_transformer.transform(result_df)