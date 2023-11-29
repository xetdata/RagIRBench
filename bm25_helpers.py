import nltk.tokenize
from rank_bm25 import BM25Okapi
import numpy as np

def tokenize(sentence):
    words = nltk.tokenize.word_tokenize(sentence)
    return [word.lower() for word in words if word.isalpha()]
def get_bm25_top_10(bm25, sentence):
    z = bm25.get_scores(tokenize(sentence))
    return np.argsort(-z)[:10].copy()
def get_bm25_top_10_batch(bm25, sentence_list):
    return [get_bm25_top_10(bm25, sentence) for sentence in sentence_list]


def get_bm25_top_10_augmented(bm25, sentence, augment):
    tok = tokenize(sentence)
    augment = [word.lower() for word in augment]
    z = bm25.get_scores(tok + augment)
    return np.argsort(-z)[:10].copy()

def get_bm25_top_10_batch_augmented(bm25, sentence_list, augment_list):
    return [get_bm25_top_10_augmented(bm25, sentence, augment) for sentence, augment in zip(sentence_list, augment_list)]
