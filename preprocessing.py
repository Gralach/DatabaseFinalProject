import re
import string
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

# ---------- TEXT CLEANSING

def case_folding(text):
    return text.lower()

def padding_punc(text):
    # padding before and after each punctuation
    s = re.sub(f'([{string.punctuation}])', r' \1 ', text)

    # strip extra whitespace
    s = re.sub('\s{2,}', ' ', s)
    
    # - and -- are two different operations in sql
    s = re.sub('- -', '--', s)
    
    return s.strip()

def mapping_numeric(text):
    # map chr(0-255) or char(0-255) to <ASCII_DEC>
    s = re.sub('(chr|char) \( ([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]) \)', 'chr ( <ASCII_DEC> )', text)
    
    # map all numeric to <NUM>
    s = re.sub(r'\b\d+\b', '<NUM>', s)
    
    # map to <HEX>
    s = re.sub(r'\b(0x)?[0-9a-fA-F]+\b', '<HEX>', s)
    
    return s

# Adapted from https://ryan-cranfill.github.io/sentiment-pipeline-sklearn-3/
def list_comprehend_a_function(list_or_series, function, active=True):
    if active:
        return [function(i) for i in list_or_series]
    else: # if it's not active, just pass it right back
        return list_or_series

def pipelinize(function, active=True):
    return FunctionTransformer(list_comprehend_a_function, validate=False, kw_args={'function': function, 'active': active})

# ---------- KERAS PREPROCESSING

class TokenizerTransformer(BaseEstimator, TransformerMixin, Tokenizer):

    def __init__(self, **tokenizer_params):
        Tokenizer.__init__(self, **tokenizer_params)

    def fit(self, X, y=None):
        self.fit_on_texts(X)
        return self

    def transform(self, X, y=None):
        X_transformed = self.texts_to_sequences(X)
        return X_transformed

class PadSequencesTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, maxlen, padding='pre', truncating='pre'):
        self.maxlen = maxlen
        self.padding = padding
        self.truncating = truncating

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_padded = pad_sequences(X, maxlen=self.maxlen, padding=self.padding, truncating=self.truncating)
        return X_padded