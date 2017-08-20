import sys
import os
import numpy as np
import pandas as pd

from itertools import product
from numpy import matmul, sum, dot, transpose, identity, square, sqrt
from numpy.linalg import inv

class MatrixFactorize(object):
    def __init__(self, _lambda = 0.065, _factors = 100, _iter = 25):
        self._lambda = _lambda
        self._factors = _factors
        self._iter = _iter
    
    def changeLambda(self, _lambda):
        self._lambda = _lambda
        print(">> New lambda: %.3f" % self._lambda)

    def initMatrix(self, n_reactions, n_user, n_status):
        self._users = n_user
        self._items = n_status
        self._rates = n_reactions
        self._R = np.ndarray(shape=(n_user, n_status))
        self._U = np.ndarray(shape=(self._factors, n_user))
        self._M = np.ndarray(shape=(self._factors, n_status))

    def init(self, reactions, user, status, emotion):
        # Init Matrix 
        self.initMatrix(n_reactions = len(reactions), n_user = len(user), n_status = len(status))

        # Data -> Rating matrix
        for index, row in reactions.iterrows():
            # print(">> User_id %d" % row['author_id'])
            # if row['author_id'] == 10154267050401160:
            #     print(index)
            user_hash = user[row['author_id']]
            if user[row['author_id']] == 0:
                print("yes")
            status_hash = status[row['status_id']]
            emotion_hash = emotion[row['reaction_status'].lower()]
            self._R[user_hash, status_hash] = emotion_hash
    
    # def save(self, filename):
    #     directory = os.path.join(os.getcwd(), filename)
    #     with open(directory, 'w') as fo:
    #         fo.write(self._R.shape[0], self._R.shape[1])
    #         fo.write(self._factors)
    #         for user, factor in product(range(self._users), range(self._factors)):
    #             fo.write(self._U[user, factor])

    #         for item, factor in product(range(self._items), range(self._factors)):
    #             fo.write(self._M[item, factor])
    
    # def load(self, filename):
    #     directory = os.path.join(os.getcwd(), filename)
    #     with open(directory, 'r') as fi:
    #         self._R = fi.readline()
    #         self._factors = fi.read()
    #         for user, factor in product(range(self._users), range(self._factors)):
    #             fi.write(self._U[user, factor])

    #         for item, factor in product(range(self._items), range(self._factors)):
    #             fi.write(self._M[item, factor])
            

    def fit(self):
        R = self._R

        [nUsers, nItems] = R.shape
        # print(nUsers, nMovies)

        # Init U and M
        U = np.random.uniform(0, 1, [self._factors, nUsers])
        M = np.random.uniform(0, 1, [self._factors, nItems])

        for i in range(0, nItems):
            M[0, i] = np.sum(R[:, i]) / np.sum(R[:, i] > 0)
        
        RMSE = 0.0
        for iter in range(self._iter):
            # Run Alternative Least Square
            print("\n>> Optimize ALS at %d iteration" % iter)
            U, M = self.alsOptimize(R, U, M)

            # Calculate the regularization
            regu = self.regularization(U, M)

            # Calculate the convergence
            print(">> Calculate the loss at %d iteration" % iter)
            Rnew = matmul(U.T, M)
            count = 0
            loss = 0.0
            for user, item in product(range(self._users), range(self._items)):
                if R[user, item] > 0:
                    # Optimize code by n * regu
                    loss += square(R[user, item] - Rnew[user, item])

            loss = sqrt(loss / self._rates * 1.0)
            RMSE = loss
            print(">> After iteration %d and lambda %.4f, the loss is %.12f" % (iter, self._lambda, loss))

        self._U = U
        self._M = M
        return U, M, RMSE
        
    
    def alsOptimize(self, R, U, M):
        Uprime = self.alsOptimizeU(R, U, M)
        Mprime = self.alsOptimizeM(R, U, M)
        return Uprime, Mprime

    def alsOptimizeU(self, R, U, M):
        #
        # Description: Alternative least square, fixed M to solve U
        #

        nUsers, nItems = self._users, self._items
        E = identity(self._factors)

        Uprime = U

        for user in range(0, nUsers):            
            Mi = M[:, R[user, :] > 0]
            if sum(Mi) == 0: 
                continue
            Nui = Mi.shape[1]
            Ai = matmul(Mi, transpose(Mi)) + (self._lambda * Nui) * E
            Ri = transpose(R[user, R[user, :] > 0].reshape(1, Nui))
            Vi = matmul(Mi, Ri)
            Uprime[:, user] = transpose(matmul(inv(Ai), Vi))
        
        return Uprime

    def alsOptimizeM(self, R, U, M):
        #
        # Description: Alternative least square, fixed M to solve U
        #

        nUsers, nItems = self._users, self._items
        E = np.identity(self._factors)

        Mprime = M

        for item in range(0, nItems):
            Ui = U[:, R[:, item] > 0]       

            if sum(Ui) == 0:
                continue     
            Nui = Ui.shape[1]
            Ai = matmul(Ui, transpose(Ui)) + (self._lambda * Nui) * E
            Ri = transpose(R[R[:, item] > 0, item].reshape(1, Nui))
            Vi = matmul(Ui, Ri)
            Mprime[:, item] = transpose(matmul(inv(Ai), Vi))

        return Mprime

    def regularization(self, U, M):
        nUsers, nMovies = self._users, self._items
        reU = reM = 0
        for user in range(0, nUsers):
            reU = U[:, user].T.dot(U[:, user])
        
        for movie in range(0, nMovies):
            reM = M[:, movie].T.dot(M[:, movie])
        
        return self._lambda * (reU + reM)
