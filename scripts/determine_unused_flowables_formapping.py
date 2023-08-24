"""
Determines FEDEFL flowables not used in a mapping and exports.

Those flowables to csv output: csv with columns 'Class','Flowable','CAS No',
'Formula','Synonyms'.
"""

import fedelemflowlist
import pandas as pd
from fedelemflowlist.globals import outputpath

#Set name of mapping file. More than one mapping file can be used
mapping_to_use = ['TRACI2.1']

if __name__ == '__main__':
    mapping = fedelemflowlist.get_flowmapping(mapping_to_use)
    # Get Flow UUIDs for flows used in selected mapping
    mapping_flow_uuids = pd.DataFrame(pd.unique(mapping['TargetFlowUUID']),columns=["Flow UUID"])

    # Get all flows
    all_flows = fedelemflowlist.get_flows()
    all_UUIDs = all_flows['Flow UUID']
    # Subset all flows to get just those used in selected mapping
    flows_used_in_mapping =  pd.merge(all_flows,mapping_flow_uuids)

    flows_used_UUIDs = flows_used_in_mapping['Flow UUID']

    # Flows not in mappings
    flows_notused_UUIDs =  set(all_UUIDs)-set(flows_used_UUIDs)
    len(flows_notused_UUIDs)

    flows_notused = all_flows[all_flows['Flow UUID'].isin(flows_notused_UUIDs)]

    #unique flowables
    flowable_fields = ['Class','Flowable','CAS No','Formula','Synonyms']
    flowables_notused = flows_notused[flowable_fields]
    flowables_notused = flowables_notused.drop_duplicates()
    flowables_notused = flowables_notused.apply(lambda x: x.astype(str),axis=0)

    flowables_notused.to_csv(
        outputpath / f'flowables_not_used_in_{mapping_to_use[0]}_mapping.csv',
        index=False)







