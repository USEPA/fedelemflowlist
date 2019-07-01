"""
Provides a pandas dataframe of all contexts as paths and as a pattern of context classes
Used by flowlist.py
"""

import pandas as pd
from fedelemflowlist.globals import inputpath, as_path, log, flow_list_specs

contexts = pd.read_csv(inputpath + 'Contexts.csv', na_values='N/A')

# Get levels for max number of compartment classes
max_compartment_classes = len(contexts.columns)
# Define compartment_classes
compartment_classes = flow_list_specs['primary_context_classes'] +\
                      flow_list_specs['secondary_context_classes']

if compartment_classes != list(contexts.columns):
    log.debug('ERROR: Compartment class list does not match column headers in Contexts sheet')

# Create dictionary of context levels
context_levels = {}
counter = 0
for c in compartment_classes:
    context_levels['c_' + str(counter)] = c
    counter = counter + 1

# Drop duplicates just as a check
contexts = contexts.drop_duplicates()

# Describe a pattern of compartment classes used in each context
# Create a clean list with no NAs
context_patterns = []
context_list_na_removed = list()
for index, row in contexts.iterrows():
    pattern = [compartment_classes[x] for x in range(0, max_compartment_classes)
               if str(row[x]) != 'nan']
    pattern = ','.join(pattern)
    context_patterns.append(pattern)
    row_list = row.values
    row_list_na_removed = [x for x in row.values if str(x) != 'nan']
    context_list_na_removed.append(row_list_na_removed)

# Using this clean list, generate context paths
context_paths = list()
for r in context_list_na_removed:
    #Pass the uuid function the list as a series of string arguments
    compartment_path = as_path(*r)
    context_paths.append(compartment_path)

# Write the context paths and patterns to a dictionary, then df
d = {'Context': context_paths, 'Pattern': context_patterns}
all_contexts = pd.DataFrame(data=d)
