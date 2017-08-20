import sys
import pandas as pd
import numpy as np
from helpers.function.evaluation import RMSE

from six.moves import xrange
from numpy import random, zeros, dot, sum, tile, square, sqrt, mean, append
from numpy import linalg as LA

def normalize(rating, max_rating):
    return (rating - 1) / (max_rating - 1)

def shuffles_rows(arr, rows):
    random.shuffle(arr[rows[0]:rows[1]+1])

class PMF(object):
    def __init__(self, n_users, n_items, n_features = 40, _momentum = 0.8, \
        learning_rate = 50.0, learning_bias = 0.001, _lambdaBias = 0.001, \
        _lambdaU = 0.001, _lambdaI = 0.001, _lambdaBiasU = 10, _lambdaBiasI = 25, \
        batch_size = 100000, max = None, _iter = 50, uncontrained = False):

        self.n_features = n_features
        self.n_users = n_users
        self.n_items = n_items
        self._lambdaU = _lambdaU
        self._lambdaI = _lambdaI
        self._lambdaBiasI = _lambdaBiasI
        self._lambdaBiasU = _lambdaBiasU
        self.learning_rate = learning_rate
        self.learning_bias = learning_bias
        self._lambdaBias = _lambdaBias

        self._momentum = _momentum
        self.batch_size = batch_size
        self.max_rating = max
        self._iter = _iter

        self.uncontrained = uncontrained
    
    def init_matrix(self):
        # Init users and items features
        self.users_features = 0.1 * random.uniform(0, 1, [self.n_users, self.n_features])
        self.items_features = 0.1 * random.uniform(0, 1, [self.n_items, self.n_features])

        # Init momentum for gradient descent
        self.users_momentum = zeros(shape=(self.n_users, self.n_features))
        self.items_momentum = zeros(shape=(self.n_items, self.n_features))

        # Init users and items bias
        self.users_bias = zeros(self.n_users)
        self.items_bias = zeros(self.n_items)

    def init_bias(self, column, n_):
        for iter in range(n_):
            if iter % 200 == 0:
                sys.stdout.flush()
                sys.stdout.write("\r>> Calculate bias for iter %d over %d" % (iter, n_))
            ratings = self.data[self.data[:, column] == iter]
            ratings = np.float64(ratings[:, 2]) - self.mean_rating
            if column == 0:
                self.users_bias[iter] = sum(ratings) / (self._lambdaBiasU + len(ratings))
            else:
                self.items_bias[iter] = sum(ratings) / (self._lambdaBiasI + len(ratings.shape))

    def fit(self, train):
        # Init matrix
        self.init_matrix()
        train = train.astype(int)
        self.data = train
        shuffles_rows(train, [0, train.shape[0]])
        total_batch = int(train.shape[0] / self.batch_size)

        # Init bias
        self.mean_rating = mean(train[:, 2])
        self.init_bias(0, self.n_users)
        self.init_bias(1, self.n_items)

        print("\n>> Start training with %d users, %d items and %d features with %.8f mean" % \
            (self.n_users, self.n_items, self.n_features, self.mean_rating))

        for iter in range(self._iter):

            for batch in range(total_batch):
                sys.stdout.flush()
                sys.stdout.write("\r>> Update to batch %d over %d" % (batch, total_batch))

                start = batch * self.batch_size
                end = (batch + 1) * self.batch_size

                sub_data = train[start:end]

                self.gradient_update(sub_data)

            # Calculate RMSE
            u_features = self.users_features.take(train[:, 0], axis=0)
            i_features = self.items_features.take(train[:, 1], axis=0)
            users_bias = self.users_bias.take(train[:, 0])
            items_bias = self.items_bias.take(train[:, 1])
            prediction = sum(u_features * i_features, 1) + self.mean_rating + users_bias + items_bias
            rmse = RMSE(prediction, train[:, 2])
            print("\n>> At epcho %d, the RMSE is %.12f\n" % (iter, rmse))

        return self

    def online_update(self, batch_update):
        for row in batch_update:
            if row[0] > self.n_users:
                temp = 0.1 * random.uniform(0, 1, [row[0] - self.n_users, self.n_features])
                self.users_features = append(self.users_features, temp, axis=0)
            
            if row[1] > self.n_items:
                temp = 0.1 * random.uniform(0, 1, [row[1] - self.n_items, self.n_features])
                self.items_features = append(self.items_features, temp, axis=0)
            
        if batch_update.shape[0] < self.batch_size:
            shuffles_rows(self.data, [0, self.data.shape[0]])
            temp = self.data[0:self.data.shape[0] - batch_update.shape[0] - 1]
            batch_update = append(batch_update, temp, axis = 0)
        
        self.gradient_update(batch_update)

    def gradient_update(self, batch_update, momentum = True):
        # Get users and items features
        batch_users_features = self.users_features.take(batch_update[:, 0], axis=0)
        batch_items_features = self.items_features.take(batch_update[:, 1], axis = 0)
        batch_users_bias = self.users_bias.take(batch_update[:, 0], axis=0)
        batch_items_bias = self.items_bias.take(batch_update[:, 1], axis=0)

        # Loss function
        prediction = sum(batch_users_features * batch_items_features, 1) + \
                            batch_users_bias + batch_items_bias

        loss = prediction - (batch_update.take(2, axis=1)) + self.mean_rating

        # Calculate gradiant
        batch_users_bias_grad = self.learning_bias * (loss + self._lambdaBias * batch_users_bias)
        batch_items_bias_grad = self.learning_bias * (loss + self._lambdaBias * batch_items_bias)

        # Calculate gradiant
        loss = tile(loss, (self.n_features, 1)).T
        batch_users_grad = loss * batch_items_features + self._lambdaU * batch_users_features
        batch_items_grad = loss * batch_users_features + self._lambdaI * batch_items_features

        # Calculate update
        batch_users_update = zeros(shape=(self.n_users, self.n_features))
        batch_items_update = zeros(shape=(self.n_items, self.n_features))
        batch_users_bias_update = zeros(shape=(self.n_users))
        batch_items_bias_update = zeros(shape=(self.n_items))
        for i in range(len(batch_update)):
            row = batch_update[i]
            batch_users_update[row[0], :] += batch_users_grad[i, :]
            batch_items_update[row[1], :] += batch_items_grad[i, :]
            batch_users_bias_update[row[0]] += batch_users_bias_grad[i]
            batch_items_bias_update[row[1]] += batch_items_bias_grad[i]


        if momentum:
            # Gradient Descent with mini-batch momentum 
            # Update momentum
            self.users_momentum = self._momentum * self.users_momentum + \
                        (self.learning_rate / batch_update.shape[0]) * batch_users_update
            
            self.items_momentum = self._momentum * self.items_momentum + \
                        (self.learning_rate / batch_update.shape[0]) * batch_items_update

            # Update features
            self.users_features -= self.users_momentum
            self.items_features -= self.items_momentum

            # Update Bias
            self.users_bias -= batch_users_bias_update
            self.items_bias -= batch_items_bias_update

        else:
            # Stochastic Gradient Descent 
            self.users_features -= batch_users_update
            self.items_features -= batch_items_update