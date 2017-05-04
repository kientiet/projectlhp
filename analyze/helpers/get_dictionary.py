import pandas as pd
import numpy as np
import os
import re
import nltk

english_vocab = set(w.lower() for w in nltk.corpus.words.words())

# eleminet noise in dictionary
def keepConditions(term, frequency):
    condition1 = 100 <= frequency <= 500
    condition2 = len(term) <= 14
    condition3 = True # not " " in term

    condition4 = not term in english_vocab
    condition5 = not term.isdigit()

    return condition1 and condition2 and condition3 and condition4 and condition5

# Print frequency and vocab list to filename
def vocabAndFrequencyToFile(frequency, vocab, filename):
    export_element = pd.DataFrame(columns=['word', 'frequency_count', 'word_length'])
    frequency = np.array(frequency)
    frequency = np.sum(frequency, axis=0)

    print(">> Exporting excel file ...")
    # print(frequency)
    for iteral in range(0, len(vocab)):
        num_word = len(vocab[iteral])
        if keepConditions(vocab[iteral], frequency[iteral]):
            export_element = export_element.append(pd.Series([vocab[iteral], frequency[iteral], num_word], index=['word', 'frequency_count', 'word_length']), ignore_index = True)

    export_element = export_element.sort(['frequency_count'], ascending=[False], kind='quicksort')
    export_element.to_excel(filename)


# def counting_tf(posts):
#     # posts = ['the apple is red', 'red is not blue', 'the organe is organe', 'that shirt is yellow']
#     count_vect = CountVectorizer(ngram_range=(2, 6))
#     # message = ['the apple is red', 'red is not blue', 'the organe is organe', 'that shirt is yellow']
#     # print(message)
#     frequency_trans = count_vect.fit_transform(posts)
#
#     frequency = count_vect.fit_transform(posts).toarray()
#     vocab = count_vect.get_feature_names()
#
#     transform = TfidfTransformer()
#     tf_idf = transform.fit_transform(frequency_trans).toarray()
#     return count_vect, frequency, vocab, tf_idf
#
# def tf_to_excel(count_vect, frequency, vocab, directory):
#     export_element = pd.DataFrame(columns=['word', 'frequency_count', 'word_length'])
#     frequency = np.array(frequency)
#     frequency = np.sum(frequency, axis=0)
#     # print(frequency)
#     for iteral in range(0, len(vocab)):
#         count = count_vect.vocabulary_.get(vocab[iteral])
#         # export_element = export_element.append(pd.Series([vocab[iteral], frequency[count]], index=['word', 'frequency_count']), ignore_index = True)
#         if (frequency[count] > 10):
#             num_word = len(vocab[iteral].split(' '))
#             export_element = export_element.append(pd.Series([vocab[iteral], frequency[count], num_word], index=['word', 'frequency_count', 'word_length']), ignore_index = True)
#
#     export_element = export_element.sort(['frequency_count'], ascending=[False], kind='quicksort')
#     export_element.to_excel(os.path.join(os.path.dirname(__file__), directory))
