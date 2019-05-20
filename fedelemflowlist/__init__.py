import pandas as pd
import os
from fedelemflowlist.globals import outputpath, flowmappingpath

#Returns the most recent flows list as a dataframe by default
def get_flowlist(version=None,format='df'):
    if version is None:
        list = identify_most_recent_list()
    else:
        list = 'FedElemFlowList_' + version
    #Get it as a dataframe
    list_file = outputpath + list + '.csv'
    if format == 'df':
        flowlist = pd.read_csv(list_file,header=0)
    return flowlist

def list_flowlists():
    files = os.listdir(outputpath)
    flowslists = []
    for name in files:
        if name.endswith(".csv"):
            n = name.strip('.csv')
            flowslists.append(n)
    return flowslists

def identify_most_recent_list(list_type='any'):
   flowlists =  list_flowlists()

   #temp
   return str(flowlists[0])

#Return a dataframe of the mapping file specific to the version of the list being used
#If a soruce list is provided, it tries to filter the dataframe to return only the desired mappings
def get_flowmapping(version=None,source_list=None):
    if version is None:
        list = identify_most_recent_list()
    else:
        list = 'FedElemFlowList_' + version
    mapping_file = flowmappingpath + list + '_mapping.csv'

    try: flowmapping =  pd.read_csv(mapping_file,header=0)
    except FileNotFoundError: print("No mapping file found for list " + list)

    if source_list is not None:
        flowmapping = flowmapping[flowmapping['Source'].isin(source_list)]
    return flowmapping
