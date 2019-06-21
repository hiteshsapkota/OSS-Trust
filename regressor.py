#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 04:08:11 2018

@author: hiteshsapkota
"""
"""Contains collection of regression techniques"""

from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import RidgeClassifierCV
from sklearn.ensemble import BaggingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn import linear_model
import pickle

data_path="Dataset/Generated"
def AdaBoost(train_features, test_feat, train_labels):
    clf=AdaBoostRegressor()
    clf.fit(train_features, train_labels)
    pred_test_labels=clf.predict(test_feat)
    return [pred_test_labels, clf]

def Bagging(train_features, test_feat, train_labels):
     clf=BaggingRegressor()
     clf.fit(train_features, train_labels)
     pred_test_labels=clf.predict(test_feat)
     return [pred_test_labels, clf]

def XGBoost(train_features, test_feat, train_labels):
     clf=XGBRegressor()
     clf.fit(train_features, train_labels)
     pred_test_labels=clf.predict(test_feat)
     filename = data_path+"/finalized_model.sav"
     pickle.dump(clf, open(filename, 'wb'))
     
     return [pred_test_labels,clf]
 
    
def SupportVec(train_features, test_feat, train_labels, C=1, gamma=1/5):
    
    clf=SVR(C=C, gamma=gamma)
    clf.fit(train_features, train_labels)
    pred_test_labels=clf.predict(test_feat)
    return [pred_test_labels, clf]

def LASSO(train_features, test_feat, train_labels):
    clf = linear_model.Lasso(alpha=0.1)
    clf.fit(train_features, train_labels)
    pred_test_labels=clf.predict(test_feat)
    filename = data_path+"/finalized_model.sav"
    pickle.dump(clf, open(filename, 'wb'))
    return [pred_test_labels, clf]
