import numpy as np
import pandas as pd
import lda
from helpers.read import read_batch_words, read_data
from helpers.terms_corpus import countAppearanceTime
from helpers.preprocessing_content import cleaning_posts

# Function for get topic of posts based on LDA algorithm
# parameters: train - collection of posts
#             vocab - collection of important words
# return: K - topic with n top words
def get_topic(train, vocab, nTopWords, kTopic, nIter):
    X = countAppearanceTime(train, vocab.tolist(), left = 1, right = 2)
    print(X)

    print(">> Initial model")
    model = lda.LDA(n_topics=kTopic, n_iter=nIter, random_state=1)

    print(">> Training model")
    model.fit(X)

    print(">> get topic")
    topic_word = model.topic_word_

    n_top_words = nTopWords

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    for i in range(10):
        print("{} (top topic: {})".format(posts[i], doc_topic[i].argmax()))

# Function for experiment with different top words, topic and iter
def experiment(train, vocab):
    get_topic(train, vocab, nTopWords = 20, kTopic = 10, nIter = 1500)

if __name__ == "__main__":
    posts, reactions = read_data()
    posts = cleaning_posts(posts)

    # for i in range(10):
    #     print(posts[i])

    vocab = read_batch_words()
    vocab = vocab['word'].dropna(how='all')
    # print(vocab)
    experiment(posts, vocab)
