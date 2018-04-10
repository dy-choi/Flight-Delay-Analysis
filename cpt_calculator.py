"""
Helper functions for computing CPTs.

@author: dychoi
"""
import pandas as pd
import numpy as np

# constants
data_df = pd.read_csv('./train_data.csv')
NUM_DELAYS = data_df.shape[0]

def parentless_CPT(col, visited_set, nodes_set):
    '''
    Find probability tables of nodes which do not have parents.
    '''
    df = data_df.groupby(col).size().to_frame()
    df.columns = ['num']
    df.reset_index(level=0, inplace=True)
    df['probability'] = df.num / NUM_DELAYS
    df['log_p'] = np.log(df.probability)
    visited_set.add(col)
    nodes_set.remove(col)
    return df, visited_set, nodes_set