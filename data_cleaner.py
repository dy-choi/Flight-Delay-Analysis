"""
File reads in twelve .csv files containing flight routes and one .csv file
that reads in airport information. Then, the data is cleaned to produce one
dataframe, flights_df that contains only informations relevant to flights from
SFO to PHL.

@author: dychoi
"""

import pandas as pd
import functions as fun


    
# read data and filter for relevant delayed flights
jan_df = fun.filterRoutes(pd.read_csv('./month/jan2017.csv'))
feb_df = fun.filterRoutes(pd.read_csv('./month/feb2017.csv'))
mar_df = fun.filterRoutes(pd.read_csv('./month/mar2017.csv'))
apr_df = fun.filterRoutes(pd.read_csv('./month/apr2017.csv'))
may_df = fun.filterRoutes(pd.read_csv('./month/may2017.csv'))
jun_df = fun.filterRoutes(pd.read_csv('./month/jun2017.csv'))
jul_df = fun.filterRoutes(pd.read_csv('./month/jul2017.csv'))
aug_df = fun.filterRoutes(pd.read_csv('./month/aug2017.csv'))
sep_df = fun.filterRoutes(pd.read_csv('./month/sep2017.csv'))
oct_df = fun.filterRoutes(pd.read_csv('./month/oct2017.csv'))
nov_df = fun.filterRoutes(pd.read_csv('./month/nov2017.csv'))
dec_df = fun.filterRoutes(pd.read_csv('./month/dec2017.csv'))

# concatenate dataframes by quarter
flights_df = pd.concat([jan_df, feb_df,mar_df,apr_df, may_df, jun_df, jul_df, aug_df, sep_df, oct_df, nov_df, dec_df])

# keep hour information from CRS but not minutes
flights_df['CRS_DEP_TIME'] = flights_df['CRS_DEP_TIME'] // 100
flights_df['CRS_ARR_TIME'] = flights_df['CRS_ARR_TIME'] // 100

airports_df = pd.read_csv('./faa-aspm/airports.csv').dropna(axis=0,how='all')

# split Date into MONTH and DAY
airports_df['Facility'] = airports_df['Facility'].str.strip()
fun.dateColumns(airports_df)
airports_df = airports_df.drop(['Date','% DelayedGateDepartures','% DelayedGateArrivals','Date'],axis=1)
airports_df = airports_df.drop(['DeparturesFor MetricComputation','ArrivalsFor MetricComputation','AverageMinutesOf DelayPer DelayedGateDeparture','AverageMinutesOf DelayPer DelayedGateArrival'],axis=1)

# find departure and arrival informations at airport at time of departure/arrival
# SFO (departure)
flights_SFO_df = pd.merge(flights_df, airports_df, how='inner', left_on=['MONTH','DAY_OF_MONTH','CRS_DEP_TIME'], right_on=['MONTH','DAY','Hour'])
flights_SFO_df = flights_SFO_df[flights_SFO_df['Facility'] == 'SFO']
# PHL (arrival)
flights_PHL_df = pd.merge(flights_df, airports_df, how='inner', left_on=['MONTH','DAY_OF_MONTH','CRS_DEP_TIME'], right_on=['MONTH','DAY','Hour'])
flights_PHL_df = flights_PHL_df[flights_PHL_df['Facility'] == 'PHL']
# set departure/arrival information as fields of flights_df
flights_df['DelayedDepartureSFO'] = flights_PHL_df['DelayedGateDepartures']
flights_df['ScheduledDepartureSFO'] = flights_PHL_df['ScheduledDepartures']
flights_df['DelayedArrivalPHL'] = flights_PHL_df['DelayedGateArrivals']
flights_df['ScheduledArrivalPHL'] = flights_PHL_df['ScheduledArrivals']
flights_df.fillna(0,inplace=True)
flights_df = flights_df.reset_index()
flights_df = flights_df.drop(['index'],axis=1)
flights_df = flights_df.drop(['DAY_OF_MONTH'],axis=1)
