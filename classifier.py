#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 08:31:45 2019

@author: hxs1943
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn import tree
from sklearn.utils import resample
from sklearn.metrics import precision_score, recall_score, f1_score
import csv

if __name__=="__main__":
    
    data_path = ""
    data = pd.read_csv("PR_trust_rep_avg.csv")
    data = data.drop(data.index[7057])
    df_majority = data[data.status==True]
    df_minority = data[data.status==False]
    df_minority_upsampled = resample(df_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=df_majority.shape[0],    # to match majority class
                                 random_state=123) # reproducible results
    
    df_upsampled = pd.concat([df_majority, df_minority_upsampled])
    data = df_upsampled
    data = data.sample(frac=1).reset_index(drop=True)
    
    """features are the features to be considered for the model
        features = ['acc_pr_hist', 'rej_pr_hist'] for the History model
        features = ['belief', 'disbelief', 'uncertainty'] for the Trust model
        features = ['acc_pr_hist', 'rej_pr_hist', 'belief', 'disbelief', 'uncertainty'] for the Hybrid model
        By default features for Hybrid model
    """
        
    features = ['acc_pr_hist', 'rej_pr_hist', 'belief', 'disbelief', 'uncertainty']
    X = data[features].values
    Y = data['status'].values
    no_class_map = { 0: 'DecisionTree'}
    
    """Name of the file where data is stored:
       1. accuracy_pr_hist.csv for History model
       2. accuracy_trust_metrics.csv for Trust model
       3. accuracy_trust_pr_hist.csv for Hybrid model 
       """
       
    file = open(data_path+"accuracy_trust_pr_hist.csv", "w")
    writer = csv.writer(file)
    fields = [['classifier', 'rep_no', 'precision', 'recall', 'fscore', 'TP', 'TN', 'FP', 'FN']]
    writer.writerows(fields)
    precisions = []
    recalls = []
    fscores = []
    confusion_TP =[]
    confusion_TN =[]
    confusion_FP =[]
    confusion_FN = []
    print("________________________")
    
    for i in range(0, 30):
            print("Wokring on the replica:", i)
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
            classifiers = [tree.DecisionTreeClassifier() ]
            
            
            for j, clf in enumerate(classifiers):
                
                print("_____Working on classifier______", clf)
                y_pred = clf.fit(X_train, y_train).predict(X_test)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f_score = f1_score(y_test, y_pred)
               
                precisions.append(precision)
                recalls.append(recall)
                fscores.append(f_score)
                tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
                fields = [[no_class_map[j], i+1, precision, recall, f_score, tp, tn, fp, fn]]
                writer.writerows(fields)
                confusion_TP.append(tp)
                confusion_TN.append(tn)
                confusion_FP.append(fp)
                confusion_FN.append(fn)
                
                
    print("Average Precision", np.mean(precisions))
    print("Average Recall", np.mean(recalls))
    print("Average Fscore", np.mean(fscores))
    print("Average TP", np.mean(confusion_TP))
    print("Average TN", np.mean(confusion_TN))
    print("Average FP", np.mean(confusion_FP))
    print("Average FN", np.mean(confusion_FN))
                
            
                
        
