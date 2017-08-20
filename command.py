import sys
import logging
import pandas as pd
import numpy as np

from numpy import square, dot, matmul, sqrt
from sklearn.model_selection import train_test_split
from helpers.function.read import read_full_data, read_reactions, read_many_file
from model.mf import MatrixFactorize
from model.pmf import PMF

def initialize(reactions):
    '''
        DONE: return dictionary user, status, emotion 
    '''
    # Divide train, cros, test
    user_id = reactions.drop_duplicates(['author_id'], keep = 'last')
    status_id = reactions.drop_duplicates(['status_id'], keep = 'last')

    # Create dictionary with user_id
    user = {}
    count = -1
    for key, row in user_id.iterrows():
        if count % 100:
            sys.stdout.flush()
            sys.stdout.write("\r>> Add user %d over %d" % (count, len(user_id)))
        if not row['author_id'] in user:
            count += 1
            user[row['author_id']] = count
    print(">> Number people in dictionay: %d" % len(user))

    # Create dictionary with status_id
    status = {}
    count = -1
    for key, row in status_id.iterrows():
        if count % 100:
            sys.stdout.flush()
            sys.stdout.write("\r>> Add status %d over %d" % (count, len(status_id)))
        if not row['status_id'] in status:
            count += 1
            status[row['status_id']] = count
    print(">> Number status in dictionay: %d" % len(status))

    # Add new column to pandas
    '''
        Like: 1
        Love: 2
        Haha: 3
        Angry: 4
        Sad: 5
        Wow: 6
    '''
    emotion = {
        'like': 1, 'love': 2, 'haha': 3, 'angry': 4, 'sad': 5, 'wow': 6
    }

    return user, status, emotion

def training(train, cros, test, user, status, emotion):
    '''
        TODO: Fix structure for Matrix Factorize 
        - Initialize matrix function
        - Pass the user, status, emotion => matrix as tradition R

        * Further: Change ALS to SGD
    '''
    train = train.append(cros)
    temp = np.array(train.as_matrix(columns=['author_id', 'status_id', 'reaction_status']))

    train = np.ndarray(shape=temp.shape)
    print(">> Start convert to batch")
    for iter in range(temp.shape[0]):
        train[iter, 0] = user[temp[iter, 0]]
        train[iter, 1] = status[temp[iter, 1]]
        train[iter, 2] = emotion[temp[iter, 2].lower()]
    
    print(">> %d row in train set" % train.shape[0])
    model = PMF(n_users = len(user), n_items = len(status), max = 5, \
                batch_size = 10000, learning_rate = 5., _lambdaU = 0.002, _lambdaI = 0.002)
    model.fit(train)

    temp = np.array(test.as_matrix(columns=['author_id', 'status_id', 'reaction_status']))
    print(">> Start convert test set to batch")
    test = np.ndarray(shape=temp.shape)
    for iter in range(temp.shape[0]):
        test[iter, 0] = user[temp[iter, 0]]
        test[iter, 1] = status[temp[iter, 1]]
        test[iter, 2] = emotion[temp[iter, 2].lower()]

    test = test.astype(int)
    print(">> %d test in test set" % test.shape[0])
    u_features = model.users_features.take(test[:, 0], axis=0)
    i_features = model.items_features.take(test[:, 1], axis=0)
    users_bias = model.users_bias.take(test[:, 0], axis=0)
    items_bias = model.items_bias.take(test[:, 1], axis=0)        
    prediction = np.sum(u_features * i_features, 1) + users_bias + items_bias
    RMSE = 0.0
    RMSE = sqrt(sum(square(test[:, 2] - prediction - model.mean_rating)) / test.shape[0])
    print("\n>> The RMSE is %.12f\n" % (RMSE))
    

    # mf = MatrixFactorize()
    # print(">> Init model")
    # mf.init(train, user, status, emotion)
    # print(">> Training model")
    # U, M, RMSE = mf.fit()

    # print(">> Test model")
    # n = len(test)
    # print(">> Number of test is %d" % n)
    # Rnew = matmul(U.T, M)
    # RMSE_test = 0.0
    # count = 0
    # for index, row in test.iterrows():
    #     count += 1
    #     if count % 100:
    #         sys.stdout.flush()
    #         sys.stdout.write("\r>> Testing %d over %d" % (count, n))
    #     user_hash = user[row['author_id']]
    #     status_hash = status[row['status_id']]
    #     emotion_hash = emotion[row['reaction_status'].lower()]
    #     RMSE_test += square(emotion_hash - Rnew[user_hash, status_hash])
    
    # RMSE_test = sqrt(RMSE_test / n)
    # print("\n>> RMSE on test set is: %.12f" % RMSE_test)


def cros_valid(cros, user, status, emotion):
    '''
        TODO: Add iter so it can run through many lamba
        - Factors cros too
        - Test condition run iter = 25, 30, ...
    '''

    # 0.065 = 0.270922731560

    n_lambda = [0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095]
    mf = MatrixFactorize()
    print(">> Init model")
    mf.init(cros, user, status, emotion)

    RMSE = []
    for t_lambda in n_lambda:
        mf.changeLambda(t_lambda)
        _, _, temp = mf.fit()
        RMSE.append(temp)
    
    for i in range(len(n_lambda)):
        print(">> With lambda %.4f, RMSE is %.12f" % (n_lambda[i], RMSE[i]))        

def testing(test, user, status, emotion):
    '''
        TODO: RMSE test
        - Plot model after training
        - Expect: plot will show user-neighbor and item-neighbor
    '''
    # Load model
    print("hello")

if __name__ == "__main__":

    # Weird error


    # Read train, cros, test
    print(">> Reading full data for train, cros and test")
    train, cros, test = read_full_data("data/proceed/mf_data.xlsx")
    print(">> Len of train set: %d" % len(train))
    print(">> Len of cros set: %d" % len(cros))
    print(">> Len of test set: %d" % len(test))

    # Organize dictionary
    print(">> Reading from file")
    posts = read_many_file(["lhpconfessions"], 'data/raw')
    print(">> Len before eliminate %d" % len(posts))

    posts = posts[posts['num_reactions'] - posts['num_likes'] > 0]
    print(">> Len after eliminate %d" % len(posts))

    print(">> Reading reactions from file")
    reactions = read_reactions('data/raw')
    print(">> Total interactions: %d" % len(reactions))

    status_id = posts['status_id'].tolist()
    reactions = reactions[reactions['status_id'].isin(status_id)]
    print(">> Total reactions in the time: %d" % len(reactions))

    # Create dictionary
    print(">> Creating dictionary")
    user, status, emotion = initialize(reactions)
    

    print("\n>> Start training")
    training(train, cros, test, user, status, emotion)

    # print("\n>> Start cross-validation")
    # cros_valid(cros, user, status, emotion)