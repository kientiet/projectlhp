#%%
from nltk import tokenize
import re
import sys
from gensim.models import Word2Vec

listOfCharacters = [u'a', u'ă', u'â', u'b', u'c', u'd', u'đ', u'e', u'ê', u'g', u'h', u'i', 
u'k', u'l', u'm', u'n',
u'o', u'ô', u'ơ', u'p', u'q', u'r', u's', u't', u'u', u'ư', u'v', u'x', u'y',
u'á', u'à', u'ả', u'ạ', u'ã',
u'ắ', u'ằ', u'ẳ', u'ặ', u'ẵ',
u'ấ', u'ầ', u'ẩ', u'ậ', u'ẫ',
u'é', u'è', u'ẻ', u'ẹ', u'ẽ',
u'ế', u'ề', u'ể', u'ệ', u'ễ',
u'ó', u'ò', u'ỏ', u'ọ', u'õ',
u'ố', u'ồ', u'ổ', u'ộ', u'ỗ',
u'ớ', u'ờ', u'ở', u'ợ', u'ỡ',
u'ú', u'ù', u'ủ', u'ụ', u'ũ',
u'ứ', u'ừ', u'ử', u'ự', u'ữ',
u'í', u'ì', u'ỉ', u'ị', u'ĩ',
u'ý', u'ỳ', u'ỷ', u'ỵ', u'ỹ', u'f', u'z', u'j']

def sen2word(sentence):
    sentence = sentence.split(" ")
    words = []
    for word in sentence:
        temp = ""
        for char in word:
            if char in listOfCharacters:
                temp += char
        if len(temp) > 0:
            words.append(temp)
    return words

def Tokenize(paragraphs):
    sentences = []
    for pos, paragraph in enumerate(paragraphs):
        if pos % 100 == 0:
            sys.stdout.flush()
            sys.stdout.write("\r>> process to %d over %d" % (pos, len(paragraphs)))

        temp = tokenize.sent_tokenize(paragraph.lower())
        # print("Post #%d: %s" % (pos, tokenize.sent_tokenize(paragraph)))
        sen = []
        for sentence in temp:
            words = sen2word(sentence)
            # print(words)
            if len(words) > 0:
                sen += words
        sentences.append(sen)
    
    return sentences

class Word_To_Vec(object):
    def __init__(self, filename, iter = 5, workers = 4, min_count = 5, alpha = 0.025, window = 5, sample = 1e3, negative = 5):
        self.iter = iter
        self.workers = workers
        self.min_count = min_count
        self.alpha = 0.025
        self.window = window
        self.sample = sample
        self.negative = negative
        self.filename = filename
    
    def train(self, sentences):
        print(">> Start training")
        self.model = Word2Vec(sentences, iter = self.iter, workers = self.workers,
            min_count = self.min_count, alpha = self.alpha, window = self.window, 
            sample = self.sample, negative = self.negative)
        self.model.save(self.filename)
        print(">> Done training")
    
    def get_vector(self, word):
        self.model = Word2Vec.load(self.filename)
        return self.model[word]

    def similar(self, word1, word2):
        self.model = Word2Vec.load(self.filename)
        print(">> Checking similarity between %s and %s is %.12f " % (word1, word2, self.model.similarity(word1, word2)))
        return self.model.similarity(word1, word2)

    def n_similar(self, word, n_words = 10):
        self.model = Word2Vec.load(self.filename)
        print(self.model.similar_by_word(word, topn = n_words))
        return self.model.similar_by_word(word, topn = n_words)
        