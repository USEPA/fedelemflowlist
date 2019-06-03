import pandas as pd
from fedelemflowlist.globals import outputpath, flowmappingpath
import fedelemflowlist.jsonld as jsonld
import os

#Returns the most recent flows list as a dataframe by default
def get_flows(preferred_only=None):
    #Get it as a dataframe
    list_file = outputpath + 'FedElemFlowListMaster.csv'
    flows = pd.read_csv(list_file,header=0)
    if preferred_only:
        flows = flows[flows['Preferred']==1]
    return flows

def get_flowmapping(source=None):
    """Gets a flowmapping in standard format

    Returns an error if specified source does not equal the source name
    Looks for a dataframe of the mapping file specific to the source
    If a source list is provided, it returns only the desired mappings
    """
    flowmappings = pd.DataFrame()
    if source is not None:
        if type(source).__name__ == 'str':
            source = [source]
        for f in source:
            mapping_file = flowmappingpath+f+'.csv'
            try:
                flowmapping = pd.read_csv(mapping_file, header=0)
                flowmappings = pd.concat([flowmappings, flowmapping])
            except FileNotFoundError:
                print("No mapping file found for " + str(f))
    else:
        #load all mappings in directory
        files = os.listdir(flowmappingpath)
        for name in files:
            if name.endswith(".csv"):
                flowmapping = pd.read_csv(flowmappingpath+name, header=0)
                flowmappings = pd.concat([flowmappings,flowmapping])
    return flowmappings

def write_jsonld(flows,path):
    writer = jsonld.Writer(flow_list=flows)
    writer.write_to(path)

