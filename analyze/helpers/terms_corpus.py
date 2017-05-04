import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# get the frequentcy of vocab (n - dimension) in posts (m - dimension)
# ngram = (left, right)
# Return matrix result(m x n), where result[i][j] is how many times the word i appears in document j
def countAppearanceTime(posts, vocab, left = 2, right = 6):
    # posts = ['the apple is red', 'red is not blue', 'the organe is organe', 'that shirt is yellow']
    count_vect = CountVectorizer(vocabulary = vocab, ngram_range=(left, right))
    # message = ['the apple is red', 'red is not blue', 'the organe is organe', 'that shirt is yellow']
    # print(message)

    print(">> get frequency")
    frequency = count_vect.fit_transform(posts).toarray()

    return frequency

# Explore the frequency without any given vocab
# n_gram = (left, right)
# Return matrix show frequency
def countAppearanceTimeWithoutVocab(posts, left, right):
    count_vect = CountVectorizer(vocabulary = vocab, ngram_range=(left, right))
    print(">> get frequency without dictionary")
    frequency = count_vect.fit_transform(posts).toarray()

    return frequency

# Get terms appear in coprus
# n_grams = (left, right)
# Return matrix one dimension includes all vocabulary
def getAttributeFromFrequencyMatrix(posts, left, right):
    # posts = ['the apple is red', 'red is not blue', 'the organe is organe', 'that shirt is yellow']
    count_vect = CountVectorizer(ngram_range=(left, right))

    print(">> get dictionary without dictionary")
    frequency = count_vect.fit_transform(posts).toarray()
    vocab = count_vect.get_feature_names()

    return vocab
