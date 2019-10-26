import nltk
from nltk.lm import MLE
from nltk.util import ngrams
from nltk.lm.preprocessing import padded_everygram_pipeline

from nltk import word_tokenize, sent_tokenize

class BidirectionalPredictor:

    def __init__(self):
        self.forward_model = MLE(2)
        self.backward_model = MLE(2)

    #accepts a list of sentences
    def fit(self, text):
        # Tokenize the text.
        tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                          for sent in sent_tokenize(text)]

        # Preprocess the tokenized text for 3-grams language modelling
        n = 3
        train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)
        self.forward_model.fit(train_data, padded_sents)

        reverse = ""
        for word in text.split():
            reverse = " ".join((word, reverse))

        reverse_tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                          for sent in sent_tokenize(reverse)]

        # Preprocess the tokenized text for 3-grams language modelling
        n = 3
        train_data, padded_sents = padded_everygram_pipeline(n, reverse_tokenized_text)
        self.backward_model.fit(train_data, padded_sents)

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



