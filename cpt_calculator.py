"""
Helper functions for computing CPTs.

@author: dychoi
"""
import pandas as pd
import numpy as np


# read in training data, edge data, and initialize NUM_DELAYS
data_df = pd.read_csv('./train_data.csv')
edges_df = pd.read_csv('./edges.csv')
nodes_with_parents = list(set(edges_df.Target))
nodes_no_parents = list(set(edges_df.Source) - set(edges_df.Target))

# some constants
nodes_set = set(nodes_with_parents + nodes_no_parents)
visited_set = set()
NUM_DELAYS = data_df.shape[0]

# make dictionary of nodes and their parents
node_parents = dict()
nodes_with_parents
for node in nodes_with_parents:
    node_parents[node] = set(edges_df.Source[edges_df.Target == node])
for node in nodes_no_parents:
    node_parents[node] = set()
    
###################################### FUNCTIONS ######################################

def get_parentless_nodes():
    return nodes_no_parents

def get_nodes_set():
    return nodes_set

def get_node_parents():
    return node_parents

def available_nodes():
    '''
    return list of available nodes to visit
    '''
    li = []
    for node in nodes_set:
        if node_parents[node].issubset(visited_set):
            li += [node]
    return li

def parentless_CPT(col):
    '''
    Find probability tables of nodes which do not have parents.
    '''
    df = data_df.groupby(col).size().to_frame()
    df.columns = ['num']
    df.reset_index(level=0, inplace=True)
    df['prob'] = df.num / NUM_DELAYS
    df['log_p'] = np.log(df.prob)
    visited_set.add(col)
    nodes_set.remove(col)
    return df

def nonparentless_CPT(node):
    df = data_df.groupby(list(node_parents[node]) + [node]).size().reset_index().rename(columns={0:'num'})
    temp_df = df.groupby(list(node_parents[node]))['num'].sum().to_frame().rename(columns={'num': 'num_sum'}).reset_index()
    df = df.merge(temp_df, left_on=list(node_parents[node]),right_on=list(node_parents[node]))
    df['prob'] = df.num / df.num_sum
    df['log_p'] = np.log(df.prob)
    df = df.drop(['num','num_sum'],axis=1)
    visited_set.add(node)
    nodes_set.remove(node)
    return df