"""
Helper functions for cleaning dataframe up.

@author: dychoi
"""

import pandas as pd
import time

columns_to_drop = ['index','YEAR', 'QUARTER','ORIGIN','DEST', 'UNIQUE_CARRIER','DEP_TIME','DEP_TIME_BLK','DEP_DELAY_GROUP', 'DEP_DELAY_NEW', 'DEP_DEL15','WHEELS_OFF','WHEELS_ON','ARR_DELAY','ARR_DELAY_NEW','SECURITY_DELAY','DIVERTED','Unnamed: 29']

def filterRoutes(df):
    '''
    filter df to contain delayed fligths from SFO to PHL routes only.
    '''
    df = df[(df['ORIGIN'] == 'SFO') & (df['DEST'] == 'PHL') & (df['ARR_DELAY'] > 0)]
    df = df.reset_index()
    return df.drop(columns_to_drop,axis=1)

def dateColumns(df):
    '''
    Given a column with mm/dd/yyyy, create a MONTH and DAY column.
    '''
    dates = [str(d).replace('/','') for d in list(df['Date'])]
    dates = [time.strptime(d,'%m%d%Y') for d in dates]
    df['MONTH'] = [d.tm_mon for d in dates]
    df['DAY'] = [d.tm_mday for d in dates]
    return df
    
def changeTimetoBinary(df, col):
    '''
    change all times in df[col] to binary variable AM (0) or PM (1)
    '''
    mask = df[col] < 12.0
    df.loc[mask, col] = 0
    mask = df[col] >= 12.0
    df.loc[mask, col] = 1
    return df
    
def changeDelaytoBinary(df, col):
    '''
    change all delay entries in df[col] to binary vairable no delay attributed (0) and delay attributed
    '''
    mask = df[col] > 0.0
    df.loc[mask, col] = 1
    return df