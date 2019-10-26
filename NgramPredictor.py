import nltk
from nltk.lm import MLE
from nltk.util import everygrams
from nltk.lm.preprocessing import padded_everygram_pipeline
from itertools import chain
import dill as pickle

from nltk import word_tokenize, sent_tokenize

class BidirectionalPredictor:

    def __init__(self):
        self.forward_model = MLE(2)
        self.backward_model = MLE(2)

    #accepts a list of sentences
    def fit(self, text):
        print("Training bidirectional ngram predictor...")
        # Tokenize the text.
        tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                          for sent in sent_tokenize(text)]

        # Preprocess the tokenized text for 3-grams language modelling
        n = 3
        print("flattening")
        flatten = chain.from_iterable
        print("finding ngrams")
        train_data = everygrams(tokenized_text, n)
        #padded_sents = flatten(tokenized_text)
        padded_sents = flatten(tokenized_text)
        #train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)
        print("fitting")
        self.forward_model.fit(train_data, padded_sents)

        print("reversing")
        reverse = ""
        for word in text.split():
            reverse = " ".join((word, reverse))

        reverse_tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                          for sent in sent_tokenize(reverse)]

        # Preprocess the tokenized text for 3-grams language modelling
        n = 3
        print("ngrams")
        train_data = everygrams(reverse_tokenized_text, n)
        print("flatten")
        padded_sents = flatten(reverse_tokenized_text)
        #train_data, padded_sents = padded_everygram_pipeline(n, reverse_tokenized_text)
        print("fit")
        self.backward_model.fit(train_data, padded_sents)
        print("done.")

    def generate_forward(self, word=None, n=1):
        return self.forward_model.generate(text_seed=word, num_words=n)

    def generate_backward(self, word=None, n=1):
        return self.backward_model.generate(text_seed=word, num_words=n)

    def gen10_forward(self, word=None, n=1):
        result = []
        for i in range(10):
            result.append(self.generate_forward(word, n))
        return result
    
    def gen10_backward(self, word=None, n=1):
        result = []
        for i in range(10):
            result.append(self.generate_backward(word, n))
        return result



