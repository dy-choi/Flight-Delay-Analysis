# Flight Delay Analysis: SFO to PHL
Master's Independent Study at the University of Pennsylvania (Spring 2018)

Flight delay is a costly problem to consumers, airlines, and industrial experts. Delays provoke complaints from passengers, create high costs to airlines, and result in difficulties for airport operations. It is therefore important for the Federal Aviation Administration (FAA) to understand the causes of delay as a means to reduce the total cost that delays can cause.

Known factors that cause flight delays include weather at the origin airport, congestion at the origin airport, and air traffic management (ATM) decisions such as Ground Delay Programs (GDP). Each component interacts with other components in complex ways, which is why flight delays are an inherently stochastic phenomenon. Simply examining the marginal distributions of such factor does not truly reveal the effects that such factors have or the relationship between any two of such factors.

Here, we will perform a case study of the use of Bayesian networks to model the relationship between different components of aircraft delay and the causal factors that affect delays. Bayesian networks allow us to simultaneously examine multiple components of delay and their relationships in a single analysis, an advantage that the use of Bayesian networks has over linear and nonlinear regression models. Moreover, Bayesian network models provide not only just predictions of future delays that incorporate the interrelationships among causal factors, but also a means of assessing the ultimate influence each causal factors has on arrival delay.

In particular, we will examine delays in flight from San Francisco International Airport (SFO) to Philadelphia International Airport (PHL).

There are four steps in this Bayesian Network analysis of flight delays.

## 1. Data Cleaning

This section reads in all the data and cleaning it up to keep just hte necessary information. This is done using two files. **data_cleaner.py, graph_functions.py, and DataPreparation.ipynb.** As the file names suggest, data_cleaner.py and graph_function.py contains functions that data wrangling- and graph-related functions. All the reading and cleaning occurs in DataPreparation.ipynb. Since we only need a fraction of the data made available to us (specifically, just the PHL - SFO data), we will write the output out to five files:

- **nodes.csv** contains the all the nodes of the Bayesian Network
- **edges.csv** contains all the directed edges of the network
- **train_data.csv** contains the training set (arbitrary 80% of all available data)
- **test_data.csv** contains the test set (the remaining 20% of the data)
- **full_data.csv** contains the train and test sets.

## 2. Data Visualization

We use the Geph software to create a visualization of the directed acylic graph (DAG). The output is **flights_delay_visualization.png**.

## 3. Computing Conditional Probability Tables

Here, we are computing the conditional probabilities relevant to each node. To do this, we first define helper functions in **cpt_calculator.py** which are called in **BayesianNetworkAnalysis.ipynb**.

## 4. Testing
