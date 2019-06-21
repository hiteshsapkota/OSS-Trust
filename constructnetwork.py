#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 19:28:51 2018

@author: hiteshsapkota
"""
"""Reads interaction record, creates a directed graph, and stores it
   Ineraction record is a nested dictionary with form {dev1:{dev2=[], dev3=[]}, dev2:{dev3=[], dev4=[]}}
   First key representes the PR generator and keys within that key are commenters. 
   [] contains all interactions (>0, positive, <0-negative)
"""
import json
import networkx as nx

data_path="Dataset/Generated"

with open(data_path+"/dev_inter_type.json") as outfile:
    developer_interaction_record=json.load(outfile)
    
def scale(x, old_min, old_max, new_min, new_max):
    new_x=(((x-old_min)*(new_max-new_min))/(old_max-old_min))+new_min
    return new_x

def getposneg(interactions):
    result=[]
    pos=0
    neg=0
    for interaction in interactions:
        if interaction>0:
            pos+=scale(interaction, 0, 2, 0, 1)
        elif interaction<0:
            neg+=scale(abs(interaction), 0, 2, 0, 1)
        
    result.append(pos)
    result.append(neg)
    
    return result
    
G = nx.DiGraph()

for generator, commenters_data in developer_interaction_record.items():
    for commenter, interactions in commenters_data.items():
        if commenter==generator:
            continue
        result=getposneg(interactions)
        pos=result[0]
        neg=result[1]
        G.add_edge(commenter, generator, pos=pos, neg=neg)
nx.write_gpickle(G, data_path+"/rep_org_graph.gpickle")
        
        
    
    