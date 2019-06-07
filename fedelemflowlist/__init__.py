import pandas as pd
from fedelemflowlist.globals import outputpath, flowmappingpath
import fedelemflowlist.jsonld as jsonld
import os

def get_flows(preferred_only=None):
    """Gets a flow list in a standard format

    Returns the full master flow list unless preferred flows is lists
    :param preferred_only:
    :return: standard Flow List dataframe
    """
    list_file = outputpath + 'FedElemFlowListMaster.csv'
    flows = pd.read_csv(list_file,header=0)
    if preferred_only:
        flows = flows[flows['Preferred']==1]
    return flows

def get_flowmapping(source=None):
    """Gets a flow mapping in standard format

    Looks for a dataframe of the mapping file specific to the source
    If a source list is provided, it returns only the desired mappings
    Returns an error if specified source does not equal the source name
    :param source: Name of source list in
    :return: standard Flow Mapping dataframe
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

def write_jsonld(flows,path,mappings=None):
    """ Writes a standard openLCA JSON-LD zip archive with elementary flows and optionally flowmappings

    :param flows: standard pd Flow List dataframe, generally from get_flows()
    :param path: path and filename with .zip extention, e.g. 'c:users/mai/fedcommonsflows.zip'
    :param mappings: standard pd Flow Mapping dataframe , generally from get_flowmapping()
    :return: writes out .zip file
    """
    writer = jsonld.Writer(flow_list=flows,flow_mapping=mappings)
    writer.write_to(path)

