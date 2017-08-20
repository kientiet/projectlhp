import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from helpers.function.read import read_many_file, read_reactions
from numpy import append, array, reshape
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.cluster import KMeans
from gensim.models import Doc2Vec

if __name__ == "__main__":

    print(">> Reading reactions from file")
    reactions = read_reactions()
    print(">> Total interactions: %d" % len(reactions))

    # Get person has most interaction
    user_id = reactions.drop_duplicates(['author_id'], keep = 'last').drop(['status_id', 'reaction_status'], axis = 1)
    print(">> Number of people liked page: %d" % len(user_id))

    count = reactions.groupby(['author_id'], as_index=False).size().reset_index().rename(columns={0:'count'})['count'].tolist()
    user_id = user_id.assign(num_reactions = count)
    print(user_id)

    user_id.to_excel("Reactions.xlsx")

    # print(">> Reading from file")
    # posts = read_many_file(["lhpconfessions", "NthersConfessions", "PtnkConfession", "rmitvnconf"], 'raw_input/Confessions')

    # model = Doc2Vec.load("gensim.txt")
    
    # X = array([])
    # count = 0
    # for vec in model.docvecs:
    #     count += 1
    #     if count == 1:
    #         print(vec)
    #     if count % 100 == 0:
    #         sys.stdout.flush()
    #         sys.stdout.write("\r>> process to %d over %d" % (count, len(model.docvecs)))
    #     X = append(X, vec)
    # X = X.reshape(len(model.docvecs), 100)
    # print(X.shape)

    # print(">> Running KMeans")
    # kmeans = KMeans(n_clusters=8, random_state=0).fit(X)

    # data = pd.DataFrame()
    # data['content'] = posts['status_message'].dropna(how='any')
    # data = data.assign(label=kmeans.labels_)

    # data = data.sort('label', ascending=True)
    # print(data)

    # writer = pd.ExcelWriter('output.xlsx')
    # data.to_excel(writer, 'Sheet 1')
    # writer.save()

    # print(">> Learning iPCA")
    # n_components = 2
    # ipca = IncrementalPCA(n_components=n_components, batch_size=10)
    # X_ipca = ipca.fit_transform(X)

    # print(">> Running KMeans")
    # kmeans = KMeans(n_clusters=8, random_state=0).fit(X_ipca)

    # print(">> Start plotting")
    # colors = ['red', 'yellow', 'green','turquoise', 'black', 'blue', 'orange', 'violet']
    # plt.figure(figsize=(8, 8))
    # count = -1
    # for X_transformed, Y_transformed in X_ipca:
    #     count += 1
    #     if count % 100 == 0:
    #         sys.stdout.flush()
    #         sys.stdout.write("\r>> add to plt %d over %d" % (count, len(X_ipca)))
    #     color = colors[kmeans.labels_[count]]
    #     plt.scatter(X_transformed, Y_transformed, color=color, lw=1)

    # plt.legend(loc="best", shadow=False, scatterpoints=1)
    # plt.axis([-10, 10, -10, 10])

    # plt.savefig('PCA_KMeans.png')
    # plt.show()
