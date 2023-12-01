import spacy
from rank_bm25 import BM25Okapi
import numpy as np
nlp = spacy.load("en_core_web_sm")

def tokenize(sentence):
    words = nlp(sentence)
    return [token.text for token in words]

def get_bm25_top_k(bm25, sentence, k):
    z = bm25.get_scores(tokenize(sentence))
    return np.argsort(-z)[:k].copy()
def get_bm25_top_k_batch(bm25, sentence_list, k):
    return [get_bm25_top_k(bm25, sentence, k) for sentence in sentence_list]


def get_bm25_top_10_augmented(bm25, sentence, augment):
    tok = tokenize(sentence)
    z = bm25.get_scores(tok + augment)
    return np.argsort(-z)[:10].copy()

def get_bm25_top_10_batch_augmented(bm25, sentence_list, augment_list):
    return [get_bm25_top_10_augmented(bm25, sentence, augment) for sentence, augment in zip(sentence_list, augment_list)]
