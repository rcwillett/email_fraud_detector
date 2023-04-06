# Import regex library
import re
# Import NLTK for natural language processing
import nltk
# import the nltk stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords 

# Import english stopwords to use in tokenizer
ENGLISH_STOP_WORDS = stopwords.words('english')
stemmer = nltk.stem.PorterStemmer()

# Custom tokenizer function
def custom_tokenizer(text):
    '''
    Accepts a string and returns a list of stemmed words filtered of english stop words
    
    Parameters
    ----------
    text: A string which contains words to be stemmed and filtered of stop words
    
    Returns
    ----------
    Ret: An array of strings containing the stemmed and filtered words
    
    Example
    ----------
    >>>> custom_tokenizer('Going to the park for a run!')
    ['go','park', 'run']
    '''
    # allow alphabetical characters and spaces only
    processed_text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Filter out additional spaces
    processed_text = re.sub(r'\s\s*', ' ', processed_text)
    # Split sentence into words
    listofwords = processed_text.split(' ')
    # Initialize the list to store the stemmed words in
    listofstemmed_words = []
    # Iterate over each word in the content
    for word in listofwords:
        # Remove stopwords and any tokens that are just empty strings
        if (not word in ENGLISH_STOP_WORDS) and (word!=''):
            # Stem the word
            stemmed_word = stemmer.stem(word)
            # Add the stemmed word to the list of words
            listofstemmed_words.append(stemmed_word)
    # Returned the stemmed list of words
    return listofstemmed_words
