"""
Regression analysis to find dependencies.
Final output is flight_edges_df, which contains from_node and to_node.
This version never actually calls the helper function 'regression model'
which was used to build the actual model.

@author: dychoi
"""
import pandas as pd
import networkx as nx
from sklearn.model_selection import train_test_split

import data_cleaner as data
import functions as fun

flights_df = data.flights_df

# 20% test data
# 774 train data, 194 test data
train_df,test_df = train_test_split(flights_df, test_size=0.2)

# initialize variables bn (for Bayesian Network) and flight_edges_df
bn = nx.DiGraph()
flight_edges_df = pd.DataFrame(columns=['from_node', 'to_node'])

arr_15_from = ['CRS_DEP_TIME','DEP_DELAY','CRS_ARR_TIME','CARRIER_DELAY','NAS_DELAY','LATE_AIRCRAFT_DELAY']
# update dataframe of edges and draw graph
flight_edges_df, bn = fun.update_flights_edges_df(arr_15_from, 'ARR_DEL15',flight_edges_df)


nas_delay_from = ['QUARTER','CRS_DEP_TIME','DEP_DELAY','TAXI_OUT','TAXI_IN','CRS_ARR_TIME','DIVERTED','CARRIER_DELAY','WEATHER_DELAY','LATE_AIRCRAFT_DELAY']

flight_edges_df, bn = fun.update_flights_edges_df(nas_delay_from, 'NAS_DELAY',flight_edges_df)

late_aircraft_from = ['MONTH','DEP_DELAY','CARRIER_DELAY','WEATHER_DELAY','NAS_DELAY']
flight_edges_df, bn = fun.update_flights_edges_df(late_aircraft_from, 'LATE_AIRCRAFT_DELAY',flight_edges_df)
# remove both edges
flight_edges_df, bn = fun.remove_edge('NAS_DELAY','LATE_AIRCRAFT_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('LATE_AIRCRAFT_DELAY','NAS_DELAY', flight_edges_df)

carrier_delay_from = ['CRS_DEP_TIME','DEP_DELAY','TAXI_OUT','TAXI_IN','CRS_ARR_TIME','DIVERTED','WEATHER_DELAY','NAS_DELAY','LATE_AIRCRAFT_DELAY']
flight_edges_df, bn = fun.update_flights_edges_df(carrier_delay_from, 'CARRIER_DELAY',flight_edges_df)
# remove both edges
flight_edges_df, _ = fun.remove_edge('CARRIER_DELAY','NAS_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('NAS_DELAY','CARRIER_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('CARRIER_DELAY','LATE_AIRCRAFT_DELAY', flight_edges_df)

weather_delay_from = ['CRS_DEP_TIME']
flight_edges_df, bn = fun.update_flights_edges_df(weather_delay_from, 'WEATHER_DELAY',flight_edges_df)

security_delay_from = ['DAY_OF_WEEK','DEP_DELAY','TAXI_OUT','CARRIER_DELAY','NAS_DELAY','LATE_AIRCRAFT_DELAY']
flight_edges_df, bn = fun.update_flights_edges_df(security_delay_from, 'SECURITY_DELAY',flight_edges_df)

quarter_from = ['MONTH','CRS_DEP_TIME','CRS_ARR_TIME']
flight_edges_df, bn = fun.update_flights_edges_df(quarter_from, 'QUARTER',flight_edges_df)

departure_delay_from = ['QUARTER','MONTH','DAY_OF_WEEK','CRS_DEP_TIME','TAXI_OUT','TAXI_IN','CRS_ARR_TIME','DIVERTED','CARRIER_DELAY','WEATHER_DELAY','NAS_DELAY','LATE_AIRCRAFT_DELAY']
flight_edges_df, _ = fun.update_flights_edges_df(departure_delay_from,'DEP_DELAY',flight_edges_df)
flight_edges_df, _ = fun.remove_edge('NAS_DELAY','SECURITY_DELAY', flight_edges_df)
flight_edges_df, _ = fun.remove_edge('NAS_DELAY','DEP_DELAY', flight_edges_df)
flight_edges_df, _ = fun.remove_edge('DEP_DELAY', 'LATE_AIRCRAFT_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('DEP_DELAY', 'CARRIER_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('DEP_DELAY', 'SECURITY_DELAY', flight_edges_df)

taxi_out_from = ['QUARTER','CRS_DEP_TIME','DEP_DELAY','TAXI_IN','CRS_ARR_TIME','CARRIER_DELAY','WEATHER_DELAY','NAS_DELAY','LATE_AIRCRAFT_DELAY']
flight_edges_df, bn = fun.update_flights_edges_df(taxi_out_from,'TAXI_OUT',flight_edges_df)
flight_edges_df, bn = fun.remove_edge('TAXI_OUT', 'NAS_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('TAXI_OUT', 'CARRIER_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('TAXI_OUT', 'SECURITY_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('DEP_DELAY', 'NAS_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('DEP_DELAY', 'TAXI_OUT', flight_edges_df)

taxi_in_from = ['QUARTER','CRS_DEP_TIME','DEP_DELAY','TAXI_OUT','CRS_ARR_TIME','DIVERTED','CARRIER_DELAY','WEATHER_DELAY','NAS_DELAY','LATE_AIRCRAFT_DELAY']
flight_edges_df, _ = fun.update_flights_edges_df(taxi_in_from,'TAXI_IN',flight_edges_df)
flight_edges_df, _ = fun.remove_edge('TAXI_OUT','DEP_DELAY', flight_edges_df)
flight_edges_df, _ = fun.remove_edge('TAXI_IN','NAS_DELAY', flight_edges_df)
flight_edges_df, _ = fun.remove_edge('TAXI_IN','CARRIER_DELAY', flight_edges_df)
flight_edges_df, _ = fun.remove_edge('TAXI_IN','DEP_DELAY', flight_edges_df)
flight_edges_df, bn = fun.remove_edge('TAXI_IN','TAXI_OUT', flight_edges_df)

delayed_SFO_from = ['WEATHER_DELAY','ScheduledDepartureSFO','DelayedArrivalPHL','ScheduledArrivalPHL']
flight_edges_df, bn = fun.update_flights_edges_df(delayed_SFO_from,'DelayedDepartureSFO',flight_edges_df)

delayed_PHL_from = ['CRS_DEP_TIME','WEATHER_DELAY','DelayedDepartureSFO','ScheduledDepartureSFO','ScheduledArrivalPHL']
flight_edges_df, bn = fun.update_flights_edges_df(delayed_PHL_from,'DelayedArrivalPHL',flight_edges_df)
flight_edges_df, bn = fun.remove_edge('DelayedArrivalPHL','DelayedDepartureSFO', flight_edges_df)
print("is DAG : ", nx.is_directed_acyclic_graph(bn), ", is tree : ", nx.is_tree(bn))