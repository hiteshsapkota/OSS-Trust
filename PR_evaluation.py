#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:32:52 2019

@author: hxs1943
"""
import json
from trustpropagation import findtrust
import networkx as nx
import csv
import numpy as np
"""Determines and stores the trust values and corresponding PR status"""

accepted_trust_values = []
rejected_trust_values = []
direct_value = 0
indirect_value=0
unconnected_value = 0
all_value = 0
data_path = "Dataset/Generated"
G = nx.read_gpickle(data_path+'/rep_org_graph.gpickle')

with open(data_path+"/test_preprocomm.json") as outfile:
    test_preprocomm = json.load(outfile)
 
file = open(data_path+"/Result/PR_trust_rep_avg.csv", "w")
writer = csv.writer(file)
fields = [['project', 'PR ID', 'generator',  'belief', 'disbelief', 'uncertainty', 'status']]
writer.writerows(fields) 
for project, project_record in test_preprocomm.items():
    print("Working on the project", project)
    with open(data_path+"/PR/"+"all_prs_"+project+".json") as outfile:
            project_PR_record = json.load(outfile)
    for ID, PR_record in project_record.items():
        generator = PR_record[0] 
        if generator not in G.nodes():
            unconnected_value+=1
            continue
        all_value+=1
        belief_records = []
        disbelief_records = []
        uncertainty_records=[]

        pr_status = project_PR_record[ID]["merged"]
        commenters = PR_record[2]
        direct=False
        for i, commenter in enumerate(commenters):
            #print("I  have completed", i/len(commenters))
            if commenter not in G.nodes():
                indirect_value+=1
                continue
            if generator==commenter:
                continue
            if G.has_edge(commenter, generator):
                #print("Edge exists")
                direct=True
                pos = G.adj[commenter][generator]['pos']
                neg = G.adj[commenter][generator]['neg']
                b=pos/(pos+neg+2)
                u = 2/(pos+neg+2)
                trust = [b, 1-b-u, u]
            else:
                print("Finding trust indireclty")
                trust = findtrust('ap-max', 'tp-discount', commenter, generator, G)
                
            if direct:
                direct_value+=1
            elif not direct:
                indirect_value+=1
            belief_records.append(trust[0])
            disbelief_records.append(trust[1])
            uncertainty_records.append(trust[2])
            if trust[0]==0 and trust[2]==1:
                continue
       
        belief = np.mean(belief_records)
        disbelief = np.mean(disbelief_records)
        uncertainty = np.mean(uncertainty_records)
        if pr_status is True:
                fields = [[project, generator, ID, belief, disbelief, uncertainty, 'True']]
                writer.writerows(fields)
                accepted_trust_values.append(trust)
        elif pr_status is False:
                 fields = [[project, generator, ID, belief, disbelief, uncertainty, 'False']]
                 writer.writerows(fields)
                 rejected_trust_values.append(trust)
                

        
