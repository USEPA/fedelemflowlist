import pandas as pd
from fedelemflowlist.globals import outputpath, flowmappingpath
import fedelemflowlist.jsonld as jsonld

#Returns the most recent flows list as a dataframe by default
def get_flows(preferred_only=None):
    #Get it as a dataframe
    list_file = outputpath + 'FedElemFlowListMaster.csv'
    flows = pd.read_csv(list_file,header=0)
    if preferred_only:
        flows = flows[flows['Preferred']==1]
    return flows

#Return a dataframe of the mapping file specific to the version of the list being used
#If a soruce list is provided, it tries to filter the dataframe to return only the desired mappings
def get_flowmapping(version=None,source=None):
    mapping_file = flowmappingpath + 'FedElemFlowList_0.1' + '_mapping.csv'
    try: flowmapping =  pd.read_csv(mapping_file,header=0)
    except FileNotFoundError: print("No mapping file found for " + str(source))
    if source is not None:
        flowmapping = flowmapping[flowmapping['SourceListName'].isin(source)]
    return flowmapping

def write_jsonld(flows,path):
    writer = jsonld.Writer(flow_list=flows)
    writer.write_to(path)

