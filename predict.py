# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:17:47 2018

@author: hiteshsapkota
"""
"""
    Takes a trained model and makes prediction for the rest of the comments. Prediction is going to have a continous value between 1-5 with 1 as strongly negative to 5 as a strongly positive.
    Stores resultant predicted file as a raw_dev_inter_type.json
"""

import json
import pickle
import numpy as np
import pandas as pd



role_feat_map={'NONE':0, 'FIRST_TIME_CONTRIBUTOR':1, 'FIRST_TIMER':2, 'CONTRIBUTOR':3, 'COLLABORATOR':4, 'MEMBER':5, 'OWNER':6}

data_path="Dataset/Generated/"
filename = data_path+"finalized_model.sav"
regressor=pickle.load(open(filename, 'rb'))
construct_date = "2016-11-24T19:23:30Z"

with open(data_path+"preprocomm.json") as outfile:
    train_preprocomm=json.load(outfile)
    
with open(data_path+"all_pro_sent_features.json") as outfile:
    sent_features=json.load(outfile)

with open(data_path+"statusfollow.json") as outfile:
    follow_data=json.load(outfile)

with open(data_path+"pr_specific_feat.json") as outfile:
    pr_specific_data=json.load(outfile)
  
with open(data_path+"/pr_acceptance_hist.json") as outfile:
    pr_acceptance_hist = json.load(outfile)    
    
    
filter_sent_feat=[]
filter_follow_feat=[]
filter_pr_spec_feat=[]
 
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

mapping_func={}  
i=0 

filter_pr_acc_hist = []

remove_project_list=['flask-admin', 'django-filer', 'zds-site']


print("I am working on a filtering process.........")
for project, project_data in train_preprocomm.items(): 
    if project in remove_project_list:
        continue
    for pr_id in project_data:
        if train_preprocomm[project][pr_id][1]>construct_date:
            continue
        commenters_data= train_preprocomm[project][pr_id]
        generator=train_preprocomm[project][pr_id][0]
        commenters_data=[k for k,v in  train_preprocomm[project][pr_id][2].items()]
        for commenter in commenters_data:
            filter_sent_feat.append(mapped_sent(sent_features[project][pr_id][commenter]))
            try:
                filter_pr_acc_hist.append(pr_acceptance_hist[project][pr_id][2][commenter])
            except KeyError:
                filter_pr_acc_hist.append([0, 0])
            filter_follow_feat.append(mapped_follow(follow_data[project][pr_id][1][commenter]))
            filter_pr_spec_feat.append(mapped_pr_spec(pr_specific_data, commenter, project, pr_id))
            mapping_func[i]=[project, pr_id, generator, commenter]
            i+=1
            
            
            
            
print("I am working on a matrix construction process.........")    

collection_features = [filter_pr_spec_feat, filter_pr_acc_hist, filter_sent_feat, filter_follow_feat]

no_features = len(filter_pr_spec_feat[0])+len(filter_pr_acc_hist[0])+len(filter_sent_feat[0])+len(filter_follow_feat[0])

dataset = np.zeros((len(filter_sent_feat),no_features))

for i in range(0, len(dataset)):
    k=0
    for collection_feature in collection_features:
        for j in range(0, len(collection_feature[i])):
            dataset[i, k] = collection_feature[i][j]
            k=k+1
            
            
    


dataset = np.asarray(dataset)

feature_names = ['Mean time diff', 'Median Time diff', 'Min Time diff', 'Max Time diff', 'Total Time diff', 'SD Time diff', \
                 'No files changed', 'No commits', 'No added lines', 'No deleted lines', 'Total comments', 'Min comm len', \
                 'Max comm len', 'Mean comm len', 'Med comm len', 'SD comm len', 'Coll role', 'Accepted PR', 'Rejected PR', \
                 'Pos Sent', 'Neg Sent', 'Gen follow Comm', 'Comm follow Gen']

dataset = pd.DataFrame(data=dataset, columns = feature_names)


with open(data_path+'/useful_features.json') as outfile:
    useful_features = json.load(outfile)
    
dataset = dataset[useful_features]

    
print("I am working on a prediction process.........")  
          
dataset_labels=regressor.predict(dataset)
dataset_labels=np.ndarray.tolist(dataset_labels)
all_dev_inter_type={}
print("I am working on a storing process.........")   
for k,v in mapping_func.items():
    all_dev_inter_type[k]=[v[0], v[1], v[2], v[3], dataset_labels[k]]
    
with open(data_path+"/raw_dev_inter_type.json", "w") as infile:
    json.dump(all_dev_inter_type, infile)


            
            
            
