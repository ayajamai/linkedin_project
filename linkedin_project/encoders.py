from textblob import TextBlob
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import numpy as np
import string
import re


class VocabReachness(TransformerMixin, BaseEstimator):
    '''
    Creates a new feature based on the variety of words used by each post
    Returns a DataFrame with a single column called "vocab_richness"
    '''
    def __init__(self, column):
        self.column = column

    def vocab_richness(self, text):
        tokens = word_tokenize(text)
        total_length = len(tokens)
        unique_words = set(tokens)
        unique_word_length = len(unique_words)
        return unique_word_length / total_length

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X[self.column]
        data = X.apply(self.vocab_richness)
        return pd.DataFrame({'vocab_richness': data})


class SentimentAnalysis(TransformerMixin, BaseEstimator):
    '''
    Creates a three new features that computes sentiment analysis bases in subjectivity, polarity and a encoder
    if they are "negative = 0", "neutral = 0.5" and "positive = 1"
    Returns a DataFrame with trhee columns called "textblob_subjectivity", "textblob_polarity", "textblob_analysis".
    '''
    def __init__(self, column):
        self.column = column

    def get_subjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity

    #Create a function to get the polarity
    def get_polarity(self, text):
        return TextBlob(text).sentiment.polarity

    def get_analysis(self, score):
        if score < 0:
            return 0
        elif score == 0:
            return 0.5
        else:
            return 1

    def fit(self, X, y=None):
        # Store here what needs to be stored during .fit(X_train) as instance attributes.
        # Return "self" to allow chaining .fit().transform()
        return self

    def transform(self, X, y=None):
        X = X[self.column]
        subjectivity = X.apply(self.get_subjectivity)
        polarity = X.apply(self.get_polarity)
        analysis = polarity.apply(self.get_analysis)
        return pd.DataFrame({
            'textblob_subjectivity': subjectivity,
            'textblob_polarity': polarity,
            'textblob_analysis': analysis
        })


class TextCleaner(TransformerMixin, BaseEstimator):
    '''
    Cleans and vectorize the data to NLProcessing
    Returns a DataFrame with a single column called "clean_text"
    '''
    def __init__(self, column):
        self.column = column
        self.vectorizer = None

    def clean(self, text):
        sentence = re.sub('https?://[^\s<>"]+|www\.[^\s<>"]+', ' ',
                          text)  # Remove links
        for punctuation in string.punctuation:
            sentence = sentence.replace(punctuation, ' ')  # Remove Punctuation
        lowercased = sentence.lower()  # Lower Case
        tokenized = word_tokenize(lowercased)  # Tokenize
        words_only = [word for word in tokenized
                      if word.isalpha()]  # Remove numbers
        stop_words = set(stopwords.words('english'))  # Make stopword list
        without_stopwords = [
            word for word in words_only if not word in stop_words
        ]  # Remove Stop Words
        lemma = WordNetLemmatizer()  # Initiate Lemmatizer
        lemmatized = [lemma.lemmatize(word)
                      for word in without_stopwords]  # Lemmatize
        return " ".join(lemmatized)  # Return as one string for post

    def fit(self, X, y=None):
        X = X[self.column]
        cleaned = X.apply(self.clean)
        self.vectorizer = TfidfVectorizer(ngram_range=(3, 3),
                                          min_df=0,
                                          max_df=0.9,
                                          max_features=5000)
        X_bow = self.vectorizer.fit(cleaned)
        return self

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        X = X[self.column]
        cleaned = X.apply(self.clean)
        X_bow = self.vectorizer.transform(cleaned)
        data = pd.DataFrame(X_bow.toarray())
        return data

def links_counts(column):
    '''
    A simples function to count the number of links in each post
    Returns a DataFrame with a single column called 'links_counts'
    '''
    counted = column['posts'].str.count('https?://[^\s<>"]+|www\.[^\s<>"]+')
    return pd.DataFrame({'links_counts': counted})
