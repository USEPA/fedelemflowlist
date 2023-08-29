"""
Compares exisiting flowable mappings to flows identified in StEWI output files
"""

import pandas as pd
import stewi
from fedelemflowlist.globals import inputpath_mapping

inventories = None
#inventories = ['NEI','TRI','DMR',]

dic = stewi.getAvailableInventoriesandYears('flow')

all_flows = pd.DataFrame()
for inventory, year_list in dic.items():
    if (inventories is None) or (inventory in inventories):
        for year in year_list:
            flows = stewi.getInventoryFlows(inventory, year)
            flows['Source'] = inventory
            all_flows = pd.concat([all_flows, flows], ignore_index=True)
all_flows = all_flows[['FlowName','Source']].drop_duplicates()

for source_name in all_flows['Source'].unique():
    try:
        flowables = pd.read_csv(inputpath_mapping / f'{source_name}_FlowableMappings.csv')
    except FileNotFoundError:
        print(f'FlowableMappings not found for {source_name}')
        continue
    # remove unmapped flows
    #flowables.dropna(subset=['TargetUnit'], inplace=True)
    #flowables = flowables[~(flowables['TargetFlowName']=='[unmapped]')]
    source_flows = all_flows[all_flows['Source']==source_name]
    mapping_flowables = set(flowables['SourceFlowName'])
    source_flowables = set(source_flows['FlowName'])
    extra = list(sorted(mapping_flowables - source_flowables))
    missing = list(sorted(source_flowables - mapping_flowables))
    if len(missing) > 0:
        print(str(len(missing)) + ' flows missing for ' + source_name + " in FlowableMapping:")
        print(missing)
    else:
        print(f'all flows found in FlowableMappings for {source_name}')
