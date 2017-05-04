from helpers.read import read_data
from helpers.preprocessing_content import cleaning_posts
import gensim, logging

def cleaning_tokenize(post):
    each_post = each_post.replace('?', '').replace('.', '').replace('!', '').replace('\n', ' ')    

def training(posts):
    # split sentences
    print(">> Split sentences")
    posts.apply(cleaning_tokenize)
    sentences = []
    for raw_post in posts:
        if len(raw_post) > 0:
            sentences.append(raw_post.split(' '))

    print(len(sentences))
    print(sentences[0])

    # start training
    # model = gensim.model.Word2Vec(iter = 1500)
    # model.build_vocab()

if __name__ == '__main__':
    posts, reactions = read_data()
    posts = cleaning_posts(posts)

    training(posts)
