from helpers import read
from helpers import terms_corpus
from helpers.preprocessing_content import cleaning_posts
from helpers.get_dictionary import vocabAndFrequencyToFile

if __name__ == "__main__":
    posts, reaction = read.read_data()
    posts = cleaning_posts(posts)

    dictionary = terms_corpus.getAttributeFromFrequencyMatrix(posts, left = 1, right = 2)

    posts = cleaning_posts(read.read_many_file(["NthersConfessions", "PtnkConfession", "rmitvnconf"]))

    frequency = terms_corpus.countAppearanceTime(posts, dictionary, left = 1, right = 2)
    vocabAndFrequencyToFile(frequency, dictionary, "experiment_1_1.xlsx")
