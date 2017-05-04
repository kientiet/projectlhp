import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

import math
import pandas as pd
import numpy as np
from helpers.cleaning.valid_token import eliminate_unmeaning
from helpers.mongodb.query import *

# Problem: ObjectId undefined
def term_corpus(term, term_id):
    corpus = find(collection = "corpus")
    term = term.lower().strip()

    total_appear = corpus_appear = LHP_corpus_appear = LHP_time_appear = 0
    rate = LHP_rate = 0.0

    for document in corpus:
        content = document['content'].lower().strip()
        total = content.count(term)
        if total > 0:
            total_appear += total
            # print(document['_id'])
            print(insert(collection = "term_corpus", \
                 key = ['term_id', 'term', 'corpus_id', 'corpus', 'frequency', 'type'], \
                value = [term_id, term.strip(), document['_id'], document['content'], total, 'term_corpus']))

            corpus_appear += 1
            if document['from_school'] == 'Le Hong Phong':
                LHP_corpus_appear += 1
                LHP_time_appear += total
    
    if total_appear > 0:
        rate = corpus_appear * 1.0 / total_appear
    if LHP_time_appear > 0:
        LHP_rate = LHP_corpus_appear * 1.0 / LHP_time_appear
    
    update(collection = "term_corpus", \
            selector_key = ["_id"], selector_value = [term_id], \
            update_key = ['total_appear', 'corpus_appear', 'LHP_corpus_appear', 'ranking_corpus', 'ranking_LHP'], \
            update_value = [total_appear, corpus_appear, LHP_corpus_appear, rate, LHP_rate])

def count_appear(runAfterClean = False):
    """
        Function is used to count frequency of term

        TODO:
        - Get term 
        - Count total appear in all corpus
        - Count number of corpus it appear
        - Count number of corpus it appear in LHP only
        - Push those value to mongo

    """

    print(">> Calculate frequency")
    if runAfterClean:
        terms = fetch(collection_name = 'term_corpus', key = ['type'], value = ['term'])
        for term in terms:
            term_corpus(term = term['term'], term_id = term['_id'])
    else:
        listOfWords = eliminate_unmeaning()
        for index, row in listOfWords.iterrows():
            word = row['word']
            term_id = insert(collection_name = "term_corpus", key = ['term'], value = [word])
            term_corpus(term = word, term_id = term_id)

def tf(term_id, corpus_id, max_frequency):
    query = get_value(collection = "term_corpus", \
            key = ["term_id", "corpus_id", "type"], \
            value = [term_id, corpus_id, "term_corpus"], require = ["frequency"]) 

    if query:
        return query["frequency"] * 1.0 / max_frequency
    else:
        return 0

def idf(term_id, corpus_id, total_appear, number_of_corpus):
    return math.log(number_of_corpus / total_appear)

def tf_idf():
    all_terms = find(collection = "term_corpus", key = ["type"], value = ["term"])
    documents = get_arr_value(collection = "corpus", require = ["content", "_id"])

    list_terms = pd.DataFrame(list(all_terms))
    print(">> Here")
    for doc in documents:
        corpus_id = doc["_id"]
        max_frequency = get_max(collection = "term_corpus", max_key = "frequency", key = ["corpus_id"], value = [doc["_id"]])
        if max_frequency:
            terms = get_arr_value(collection = "term_corpus", key = ["corpus_id"], value = [ObjectId(corpus_id)], require = ["term_id"])
            for term in terms:
                print("====================================")
                print("Calculating tf_idf between doc " + str(doc["_id"]) + " and term " + str(term["term_id"]) + " ...")

                temp = list_terms[list_terms._id == term["term_id"]]

                term_id = term["term_id"]
                corpus_id = doc["_id"]
                total_appear = temp["total_appear"]
                number_of_corpus = temp["corpus_appear"]

                frequency = tf(term_id, corpus_id, max_frequency)
                if (number_of_corpus != 0).bool() and (frequency != 0):
                    inverse = idf(term_id, corpus_id, total_appear, number_of_corpus)
                    update(collection = "term_corpus", 
                            selector_key = ["term_id", "corpus_id"], selector_value = [term_id, corpus_id], \
                            update_key = ["tf_idf"], update_value = [frequency * inverse])
                    print("The frequency score is: " + str(frequency))
                    print("The inverse score is: " + str(inverse))
                    print("The tf_idf score is: " + str(frequency * inverse))
                    print("====================================")
                else:
                    print("Word does")
                    print("====================================")

if __name__ == '__main__':
    # count_appear(runAfterClean = True)
    term_corpus(term = "an tâm", term_id = "58f3c82b1827ef343cb5b3f0")
    # tf_idf()