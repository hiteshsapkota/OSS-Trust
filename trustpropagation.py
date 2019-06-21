#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 17:26:59 2019

@author: hxs1943
"""
import networkx as nx
import numpy as np
import sklearn.metrics
import json
def transitivity(b1, u1, b2, u2, oper_type='tp-min'):
    if oper_type == 'tp-min':
        if b1==b2:
             u = max(u1, u2)
             b = b1
             return [b, u]
        b = min(b1, b2)
        if b==b1:
            u = u1
        else:
            u=u2
        return [b, u]
    elif oper_type == 'tp-discount':
         u= 1-b1*(1-u2)
         b = b1*b2
         return [b, u]
       
        
    #something will be added
    
def aggregation(r_data, s_data, oper_type='ap-max'):
    #something will be added
    if oper_type == 'ap-max':
        b_data = []
        u_data = []
        for i in range(0, len(r_data)):
            bu = findbu(r_data[i], s_data[i])
            b_data.append(bu[0])
            u_data.append(bu[1])
        try:
            b = max(b_data)
        except ValueError:
            print(r_data)
        indices = [b_data.index(belief) for belief in b_data if belief==b]
        u = min([u_data[index] for index in indices])
        return [b, u]
    elif oper_type == 'ap-cons':
        bu=findbu(sum(r_data), sum(s_data))
        return [bu[0], bu[1]]
    
    elif oper_type == 'ap-mean':
         b_data = []
         u_data = []
         for i in range(0, len(r_data)):
             bu = findbu(r_data[i], s_data[i])
             b_data.append(bu[0])
             u_data.append(bu[1])
         b = np.mean(b_data)
         u=u_data[0]
         for i in range(1, len(u_data)):
             u1 = u_data[i]
             u = np.sqrt(u**2+u1**2)/2
         return [b, u]
    
###Mapping from interaction to Trust Space###
def findbu(r, s):
    b=r/(r+s+2)
    u=2/(r+s+2)
    return [b, u]  

def findrs(b, u):
    r=(2*b)/u
    s=2*(1-b-u)/u 
    return [r, s]

"""Determines indirect trust between pair of developers"""

def findtrust(agg, concat, developer1, developer2, H):
    if nx.has_path(H, source = developer1, target = developer2):
        r_data = []
        s_data = []
        if nx.shortest_path_length(H, source = developer1, target = developer2)>3:
            paths = nx.all_shortest_paths(H,source=developer1,target=developer2)
        else:
            paths = nx.all_simple_paths(H, source = developer1, target = developer2, cutoff=3)
        for path in paths:
            if len(path)==2:
                continue
            count=0
            dev1 = path[0]
            dev2 = path[1]
            pos = H.adj[dev1][dev2]['pos']
            neg = H.adj[dev1][dev2]['neg']
            bu = findbu(pos, neg)
            resb= bu[0]
            resu = bu[1]
            
            while count<len(path)-2:
                bu=findbu(H.adj[path[count+1]][path[count+2]]['pos'], H.adj[path[count+1]][path[count+2]]['neg'] )
                b=bu[0]
                u=bu[1]
                result=transitivity(resb,resu,b,u, oper_type=concat)
                resb=result[0]
                resu=result[1]
                count=count+1
            result=findrs(resb, resu)
            r_data.append(result[0])
            s_data.append(result[1]) 
        if len(r_data)==0:
            return [0, 0, 1]
        bu=aggregation(r_data,s_data, oper_type = agg)
        b=bu[0]
        u=bu[1]
    else:
           b=0
           u=1
    return [b, (1-b-u), u]
    
    
    
    
if __name__=="__main__":
    data_path = 'Dataset/Generated'
    G = nx.read_gpickle(data_path+'/trust_graph.gpickle')
    connected_nodes_pair=[]
    total_edges = len(G.edges())
    req_edges = 0.01*total_edges
    for i, edge in enumerate(G.edges()):
        if i>=req_edges:
           break 
        dev1= edge[0]
        dev2 = edge[1]
        connected_nodes_pair.append((dev1, dev2))
   
   
    
        
    
    data = {}
    transit = ['tp-min', 'tp-discount']
    aggreg = ['ap-max', 'ap-cons', 'ap-mean']
    for trans in transit:
        for agg in aggreg:
             direct_b = []
             direct_u = []
             indirect_b = []
             indirect_u = []
             for edge in connected_nodes_pair:
                 dev1 = edge[0]
                 dev2 = edge[1]
                 pos = G.adj[dev1][dev2]['pos']
                 neg = G.adj[dev1][dev2]['neg']
                 [b, u] = findbu(pos, neg)
                 direct_b.append(b)
                 direct_u.append(u)
                 [ind_b, _, ind_u] = findtrust(agg, trans,  dev1, dev2, G)
                 indirect_b.append(ind_b)
                 indirect_u.append(ind_u)
             MAE_B = sklearn.metrics.mean_absolute_error(direct_b, indirect_b)
             MAE_U = sklearn.metrics.mean_absolute_error(direct_u, indirect_u)
             RMSE_B = np.sqrt(sklearn.metrics.mean_squared_error(direct_b, indirect_b))
             RMSE_U =  np.sqrt(sklearn.metrics.mean_squared_error(direct_u, indirect_u))
             print("For:", (trans, agg), "MAE:", (MAE_B, MAE_U), "RMSE:", (RMSE_B, RMSE_U))
             data[(trans, agg)] = [MAE_B, MAE_U, RMSE_B, RMSE_U]
    with open(data_path+"/Result/"+"trust_prop_performance.json", "w") as infile:
        json.dump(data, infile)
             
                 
                 
             
            
    #Something will be added here
