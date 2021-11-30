from textblob import TextBlob
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import pandas as pd
import string
import re


class FeaturesCreator():
    def __init__(self):
        pass

    def vocab_richness(self, text):
        tokens = word_tokenize(text)
        total_length = len(tokens)
        unique_words = set(tokens)
        unique_word_length = len(unique_words)
        return unique_word_length / total_length

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        data = X['posts'].apply(self.vocab_richness)
        #data = self.dichotomies(X)
        return data

class SentimentAnalysis():
    def __init__(self):
        pass

    def get_subjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity

    #Create a function to get the polarity
    def get_polarity(self, text):
        return TextBlob(text).sentiment.polarity

    def get_analysis(self, score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def transform(self, data):
        #Create two new columns ‘Subjectivity’ & ‘Polarity’
        data['TextBlob_Subjectivity'] = data['clean_text'].apply(
            self.get_subjectivity)
        data['TextBlob_Polarity'] = data['clean_text'].apply(self.get_polarity)
        data['TextBlob_Analysis'] = data['TextBlob_Polarity'].apply(
            self.get_analysis)
        return data

class TextCleaner():
    def __init__(self):
        pass

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

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        return X.apply(self.clean)
