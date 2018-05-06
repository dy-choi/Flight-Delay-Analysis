"""
Helper functions for computing CPTs.

@author: dychoi
"""
import pandas as pd
import numpy as np
from operator import mul

# constant
TINY = np.finfo(float).tiny


# read in training data, edge data, and initialize NUM_DELAYS
data_df = pd.read_csv('./train_data.csv').astype('int',copy=False)
edges_df = pd.read_csv('./edges.csv')
nodes_with_parents = list(set(edges_df.Target))
nodes_no_parents = list(set(edges_df.Source) - set(edges_df.Target))

# some constants
nodes_set = set(nodes_with_parents + nodes_no_parents)
visited_set = set()
NUM_DELAYS = data_df.shape[0]

# make dictionary of nodes and their parents
node_parents = dict()
for node in nodes_with_parents:
    node_parents[node] = set(edges_df.Source[edges_df.Target == node])
for node in nodes_no_parents:
    node_parents[node] = set()

# make dictionary of number of posisble values for each node
node_values = {
'TAXI_OUT': [i for i in range(7)],
 'ScheduledDepartureSFO': [i for i in range(5)],
 'CRS_DEP_TIME':[0, 1],
 'ARR_DEL15':[0, 1],
 'CARRIER_DELAY':[0, 1],
 'WEATHER_DELAY':[0, 1],
 'DelayedDepartureSFO':[0, 1],
 'LATE_AIRCRAFT_DELAY':[0, 1],
 'DEP_DELAY':[0, 1, -1],
 'DelayedArrivalPHL':[0, 1],
 'TAXI_IN':[i for i in range(13)],
 'ScheduledArrivalPHL':[i for i in range(5)],
 'CRS_ARR_TIME':[0, 1],
 'NAS_DELAY':[0, 1],
 'MONTH': [i for i in range(1,13)],
 'DAY_OF_WEEK': [i for i in range(1,8)]
}
    
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
    return [node for node in nodes_set if node_parents[node].issubset(visited_set)]

def parentless_CPT(col):
    '''
    Compute probability tables of nodes which do not have parents.
    '''
    df = data_df.groupby(col).size().to_frame()
    df.columns = ['num']
    df.reset_index(level=0, inplace=True)
    df['prob'] = df.num / NUM_DELAYS
    df['log_p'] = np.log(df.prob)
    df = df.drop(['num'],axis=1)

    # update node sets
    visited_set.add(col)
    nodes_set.remove(col)
    return df

def nonparentless_CPT(node):
    '''
    Compute probability tables of nodes that have parents.
    '''
    # compute CPT
    df = data_df.groupby(list(node_parents[node]) + [node]).size().reset_index().rename(columns={0:'num'})
    temp_df = df.groupby(list(node_parents[node]))['num'].sum().to_frame().rename(columns={'num': 'num_sum'}).reset_index()
    df = df.merge(temp_df, left_on=list(node_parents[node]),right_on=list(node_parents[node]))
    df['prob'] = df.num / df.num_sum
    df['log_p'] = np.log(df.prob)
    df = df.drop(['num','num_sum'],axis=1)
    
    # update node sets
    visited_set.add(node)
    nodes_set.remove(node)
    
    # calculate number of expected rows
    num_rows = np.prod([len(node_values[parent]) for parent in [node for node in node_parents[node]]]) * len(node_values[node])
    num_missing = num_rows - df.shape[0]
    if num_missing > 0:
        print('Note: There are', df.shape[0], 'rows in the above table, but we should have', num_rows, \
              ', which means that', num_missing, 'row(s) missing values have been replaced with to occur with probability',\
              TINY, '.')
        df = fill_missing(node, df)
    return df

def fill_missing(node, df):
    '''
    Complete the CPT (df) by adding in values that are missing observations.
    '''
    # make a complete CPT
    temp = [node_values[p] for p in node_parents[node]] + [node_values[node]]
    temp = np.stack(np.meshgrid(*temp), -1).reshape(-1, len(temp))
    temp = pd.DataFrame(temp,columns=df.columns.tolist()[:-2])
    
    # merge with original df
    on_li = df.columns.tolist()[:-2]
    df = temp.merge(df, on=on_li, how='outer')

    # replace NaN values with very small values
    df['prob'].fillna(TINY, inplace=True)
    df['log_p'].fillna(np.log(TINY), inplace=True)
    return df