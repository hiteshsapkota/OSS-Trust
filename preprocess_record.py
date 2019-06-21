#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 19:12:56 2018

@author: hiteshsapkota
"""
"""
    Changes the continousvalue rating between 1-5 to -1 to 1
    Reads raw_dev_inter_type and process it and stores to the file dev_inter_type.
   raw_dev_inter_type has a form of {0=[], 1=[]}, where [] is a list with following attributes
    list[0]=project name
    list[1]=
    list[2]=PR generator name
    list[3]=Commenter name
    list[4]=interaction score (0-5)
    
    """
import json
data_path="Dataset/Generated"
with open(data_path+"/raw_dev_inter_type.json") as outfile:
    all_dev_inter=json.load(outfile)

developer_interaction_record={}    
for k,v in all_dev_inter.items():
    generator=v[2]
    commenter=v[3]
    interaction_score=v[4]
    interaction_score=interaction_score-3
    existing_dev=[dev for dev, data in developer_interaction_record.items()]
    if generator in existing_dev:
        exist_commenters=[comm for comm, data in developer_interaction_record[generator].items()]
        if commenter in exist_commenters:
           developer_interaction_record[generator][commenter].append(interaction_score)
        else:
              developer_interaction_record[generator][commenter]=[]
              developer_interaction_record[generator][commenter].append(interaction_score)
    else:
         developer_interaction_record[generator]={}
         developer_interaction_record[generator][commenter]=[]
         developer_interaction_record[generator][commenter].append(interaction_score)
         
with open(data_path+"/dev_inter_type.json", "w") as infile:
    json.dump(developer_interaction_record, infile)
    
