#Gets Fed Commons Flow UUID from mapping list and adds it to mapping file(s). Mapping file must already conform to mapping format
import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import flowmappingpath,flowmapping_fields

#Add source name here. The .csv mapping file with this name must be in the flowmapping directory
source = None

if __name__ == '__main__':
#Pull in mapping file
    mapping = fedelemflowlist.get_flowmapping(source)
    all_flows = fedelemflowlist.get_flows()
    all_flows = all_flows[['Flowable','Context','Flow UUID','Unit']]
    mapping_w_flowinfo = pd.merge(mapping,all_flows,left_on=['TargetFlowName','TargetFlowContext','TargetUnit'],right_on=['Flowable','Context','Unit'])
    mapping_w_flowinfo = mapping_w_flowinfo.drop(columns=['Flow UUID','Flowable','Context','Unit'])

    flowmapping_order = list(flowmapping_fields.keys())
    mapping_w_flowinfo = mapping_w_flowinfo[flowmapping_order]

    for s in pd.unique(mapping_w_flowinfo['SourceListName']):
        mapping = mapping_w_flowinfo[mapping_w_flowinfo['SourceListName']==s]
        mapping.to_csv(flowmappingpath+s+'.csv',index=False)