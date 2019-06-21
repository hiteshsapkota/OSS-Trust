#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 04:07:55 2018

@author: hiteshsapkota
"""

"""
Experiments with different models and picks the best one. 
In our experimentation, the best one is XGBoost.
Stores the final model trained on a manually annotated data as finalized_model.sav.
"""
import json
import numpy as np
from sklearn.metrics import f1_score
from ensemblestacking import ordinallogistic
from numpy import interp
from numpy import *
import random
from sklearn.metrics import classification_report
from sklearn.preprocessing import Imputer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from regressor import AdaBoost
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from regressor import Bagging
from regressor import XGBoost
from regressor import SupportVec
from regressor import LASSO
import pickle
from xgboost import plot_importance,XGBClassifier
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor    

sid = SentimentIntensityAnalyzer()

def calculate_vif_(X, thresh=6.0):
    """
    Args:
        X input N*D where N is number of datasets, D is number of variables
    Returns:
        X N*M where M is total number of useful variables
    """
    variables = list(range(X.shape[1]))
    dropped = True
    while dropped:
        dropped = False
        vif = [variance_inflation_factor(X.iloc[:, variables].values, ix)
               for ix in range(X.iloc[:, variables].shape[1])]

        maxloc = vif.index(max(vif))
        if max(vif) > thresh:
            print('dropping \'' + X.iloc[:, variables].columns[maxloc] +
                  '\' at index: ' + str(maxloc))
            del variables[maxloc]
            dropped = True

    print('Remaining variables:')
    print(X.columns[variables])
    return [X.iloc[:, variables], variables]


data_path="Dataset/Generated"
role_feat_map={'NONE':0, 'FIRST_TIME_CONTRIBUTOR':1, 'FIRST_TIMER':2, 'CONTRIBUTOR':3, 'COLLABORATOR':4, 'MEMBER':5, 'OWNER':6}

def mapped_label(label):
    if int(label)>3:
        return 1
    elif int(label)==3:
        return 0
    elif int(label)<3:
        return -1
    
def mapped_sent(scores):
    new_scores=[]
    for score in scores:
        new_scores.append(float(score))
    return new_scores

def mapped_follow(scores):
    new_scores=[]
    for score in scores:
        new_scores.append(int(score))
    return new_scores

def mapped_pr_spec(ml_pr_data, commenter, project, pr_id):
    pr_only_feat=[]
    commenter_spec=[]
    pr_only_data=ml_pr_data[project][pr_id]
    for i in range(1, 12):
        if i==7:
            continue
            
        pr_only_feat.append(float(pr_only_data[i]))
    try:   
        commenter_data=pr_only_data[12][commenter]
        for i in range(0, 7):
            if i==6:
                commenter_spec.append(role_feat_map[commenter_data[i]])
            else:
                commenter_spec.append(float(commenter_data[i]))
    except KeyError:
        
        commenter_spec=[0]*7
        
    return pr_only_feat+commenter_spec
            
def countnooflabel(data_label):
    pos=0
    neg=0
    neu=0
    result=[]
    for each_data in data_label:
        if each_data==1:
            pos+=1
        elif each_data==0:
            neu+=1
        elif each_data==-1:
            neg+=1
    result.append(pos)
    result.append(neg)
    result.append(neu)
    return result

def putdata(newdata, existing_data):
    length=existing_data.shape[0]
    for i in range(0, length):
        newdata[i, :]=existing_data[i, :]
    return newdata
        
def putlabel(new_label, existing_label):
    for i in range(0, len(existing_label)):
        new_label[i]=existing_label[i]
    return new_label


def appendextra(over_indices, train_dataset, oversample_train_dataset, offset):
    for j in range(0, len(over_indices) ):
        oversample_train_dataset[offset+j, :]=train_dataset[over_indices[j], :]
    return oversample_train_dataset



def appendlabel(over_indices, train_label, oversample_train_label, offset):
    for j in range(0, len(over_indices)):
        oversample_train_label[offset+j]=train_label[over_indices[j]]
    return oversample_train_label

def getsentscore(comments):
    all_pos=[]
    all_neg=[]
    all_neu=[]
    all_comp=[]
    for comment in comments:
        ss = sid.polarity_scores(comment)
        all_pos.append(ss['pos'])
        all_neg.append(ss['neg'])
        all_neu.append(ss['neu'])
        all_comp.append(ss['compound'])
    result=[]
    result.append(np.mean(all_pos))
    result.append(np.mean(all_neg))
    result.append(np.mean(all_neu))
    result.append(np.mean(all_comp))
    return result
        
    
    
with open(data_path+"/Train/label_pr_map.json") as outfile:
    label_pr_map=json.load(outfile)
    
with open(data_path+"/preprocomm.json") as outfile:
    prepro_comments=json.load(outfile)
    
with open(data_path+"/Train/sent_features.json") as outfile:
    sent_features=json.load(outfile)

with open(data_path+"/Train//ml_follow_data.json") as outfile:
    ml_follow_data=json.load(outfile)
    
with open(data_path+"/Train/ml_pr_specific.json") as outfile:
    ml_pr_data=json.load(outfile)

with open(data_path+"/Train/status_shared_repo.json") as outfile:
    ml_repo_data=json.load(outfile)
    
with open(data_path+"/Train/status_shared_pr.json") as outfile:
    ml_shared_pr_data=json.load(outfile)
    
with open(data_path+"/Train/prepro_word2vec_feat.json") as outfile:
    word2vec_feat=json.load(outfile)
    
with open(data_path+"/pr_acceptance_hist.json") as outfile:
    pr_acceptance_hist = json.load(outfile)
    
filter_sent_feat=[]
filter_follow_feat=[]
filter_pr_spec_feat=[]
filter_repo_feat=[]
filter_pr_shared_feat=[]
filter_word2vec_feat=[]
filter_pr_acc_hist = []
labels=[]
other_sent_feat=[]
count=0

"""Creates matrix for the training data"""
for project, project_data in label_pr_map.items(): 
    for pr_id in project_data:
        commenters_data=label_pr_map[project][pr_id]
        prepro_commenters=[k for k,v in prepro_comments[project][pr_id][2].items()]
        for commenter, label in commenters_data.items():
            if commenter.strip()  in prepro_commenters:
                commenter=commenter.strip()
                labels.append(label)
                comments=prepro_comments[project][pr_id][2][commenter]
                result=getsentscore(comments)
                other_sent_feat.append(result)
                filter_sent_feat.append(mapped_sent(sent_features[project][pr_id][commenter]))
                try:
                    filter_pr_acc_hist.append(pr_acceptance_hist[project][pr_id][2][commenter])
                except KeyError:
                    filter_pr_acc_hist.append([0, 0])
                    
                    
                try:
                    filter_follow_feat.append(mapped_follow(ml_follow_data[project][pr_id][1][commenter]))
                except KeyError:
                    filter_follow_feat.append([0, 0])
                filter_pr_spec_feat.append(mapped_pr_spec(ml_pr_data, commenter, project, pr_id))
                filter_repo_feat.append(int(ml_repo_data[project][pr_id][1][commenter]))
               
                filter_pr_shared_feat.append(int(ml_shared_pr_data[project][pr_id][1][commenter]))
                
                try:
                    filter_word2vec_feat.append(word2vec_feat[project][pr_id][2][commenter])
                except KeyError:
                    data=[0]*300
                    filter_word2vec_feat.append(data)
                    

filter_word2vec_feat = Imputer().fit_transform(filter_word2vec_feat)
                    

                



collection_features = [filter_pr_spec_feat, filter_pr_acc_hist, filter_sent_feat, filter_follow_feat]

no_features = len(filter_pr_spec_feat[0])+len(filter_pr_acc_hist[0])+len(filter_sent_feat[0])+len(filter_follow_feat[0])

train_dataset = np.zeros((int(np.floor(len(filter_sent_feat)*0.7)),no_features))
test_dataset=np.zeros((len(filter_sent_feat)-int(np.floor(len(filter_sent_feat)*0.7)),no_features))
train_label=[0]*int(np.floor(len(filter_sent_feat)*0.7))

test_label=[0]*(len(filter_sent_feat)-int(np.floor(len(filter_sent_feat)*0.7)))

"""Creates matrix for the testing data"""

for i in range(0, int(np.floor(len(filter_sent_feat)*0.7))):
    k=0
    for collection_feature in collection_features:
        for j in range(0, len(collection_feature[i])):
            train_dataset[i, k] = collection_feature[i][j]
            k=k+1
    train_label[i]=labels[i]

initial_point =  int(np.floor(len(filter_sent_feat)*0.7))
for i in range(initial_point, len(filter_sent_feat)):
    k=0
    for collection_feature in collection_features:
        for j in range(0, len(collection_feature[i])):
            test_dataset[i-initial_point, k] = collection_feature[i][j]
            k=k+1
    test_label[i-initial_point]=labels[i]
    



    
train_dataset = np.asarray(train_dataset)
test_dataset = np.asarray(test_dataset)


feature_names = ['Mean time diff', 'Median Time diff', 'Min Time diff', 'Max Time diff', 'Total Time diff', 'SD Time diff', \
                 'No files changed', 'No commits', 'No added lines', 'No deleted lines', 'Total comments', 'Min comm len', \
                 'Max comm len', 'Mean comm len', 'Med comm len', 'SD comm len', 'Coll role', 'Accepted PR', 'Rejected PR', \
                 'Pos Sent', 'Neg Sent', 'Gen follow Comm', 'Comm follow Gen']

train_df = pd.DataFrame(data=train_dataset, columns = feature_names)
test_df = pd.DataFrame(data=test_dataset, columns = feature_names)

included_features = [feature_names.index('Pos Sent'), feature_names.index('Neg Sent'), feature_names.index('Gen follow Comm'),feature_names.index('Comm follow Gen'),  feature_names.index('Max comm len')]

filter_train_df = train_df.iloc[:, included_features]
filter_test_df = test_df.iloc[:, included_features]

[train_df, rem_features_idx] = calculate_vif_(train_df)
test_df = test_df.iloc[:, rem_features_idx]

"""Trains XGBoost and returns corresponding predicted test labels"""

[result, model] = XGBoost(filter_train_df, filter_test_df, train_label)
features = ['Pos Sent', 'Neg Sent', 'Gen follow Comm', 'Comm follow Gen', 'Max comm len']
with open(data_path+"/useful_features.json", "w") as file:
    json.dump(features, file)
filename = data_path+"/finalized_model.sav"
print("Mean absolute error is:", mean_absolute_error(test_label, result))
print("Mean square error is:", np.sqrt(mean_squared_error(test_label, result)))
features = [feature for feature in feature_names if feature_names.index(feature) in rem_features_idx]

