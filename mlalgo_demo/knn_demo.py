# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2022/1/7
description:knn算法实现
'''

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split


class KNNClassifier:
    def __init__(self, k):
        self.k = k
        self._x_train = None
        self._y_train = None

    def fit(self, x_train, y_train):
        '''

        Args:
            x_train: 训练数据x
            y_train: 训练数据y
        Returns:
            None
        '''
        self._x_train = x_train
        self._y_train = y_train

    def _predict(self, x):
        d = [np.sqrt(np.sum((x_i - x) ** 2)) for x_i in self._x_train]
        pair = []
        x = 0
        for distance in d:
            pair.append((x, distance))
            x += 1
        pair.sort(key=lambda x: x[1])
        top_k = [self._y_train[i[0]] for i in pair[:self.k]]
        votes = self.count_times(top_k)
        return self.get_max_appear(votes)

    def predict(self, x):
        '''
            预测数据
        Args:
            x: 测试数据
        Returns:
            np.array
        '''
        y_predict = [self._predict(x1) for x1 in x]
        return np.array(y_predict)

    def score(self, x_test, y_test):
        '''
            评估方法
        Args:
            x_test: 测试数据集
            y_test: 测试集
        Returns:
            float
        '''
        y_predict = self.predict(x_test)
        return sum(y_predict == y_test) / len(x_test)

    def count_times(self, top_k):
        '''
            把字符转成map
        Args:
            top_k: 前面k个数
        Returns:
            map
        '''
        times = {}
        for k in top_k:
            if k in times:
                times[k] += 1
            else:
                times[k] = 1
        return times

    def get_max_appear(self, d):
        '''
            找出最大出现次数
        Args:
            d: 字典
        Returns:
            出现最大次数的
        '''
        if d is None:
            return None
        max_times = 0
        for k in d:
            max_times = max(d[k], max_times)
        for k in d:
            if d[k] == max_times:
                return k
        return k


if __name__ == '__main__':
    iris = datasets.load_iris()
    x, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(x, y)
    my_knn = KNNClassifier(k=6)
    my_knn.fit(X_train, y_train)
    y_predict = my_knn.predict(X_test)
    print(y_predict)
    score = my_knn.score(X_test, y_test)
    print(score)
