#Gets Fed Commons Flow UUID from mapping list and adds it to mapping file. Mapping file must already conform to mapping format
import pandas as pd
import fedelemflowlist as fl
from fedelemflowlist.globals import flowmappingpath

#Add source name here. The .csv mapping file with this name must be in the flowmapping directory
source = 'CDDLCI'

if __name__ == '__main__':
#Pull in mapping file
    mapping = fl.get_flowmapping(source)
    all_flows = fl.get_flows()
    all_flows = all_flows[['Flowable','Context','Flow UUID','Unit']]
    mapping_w_flowinfo = pd.merge(mapping,all_flows,left_on=['TargetFlowName','TargetFlowContext','TargetUnit'],right_on=['Flowable','Context','Unit'])
    mapping_w_flowinfo = mapping_w_flowinfo.drop(columns=['Flow UUID','Flowable','Context','Unit'])

    flowmapping_order = ['SourceListName',
                         'SourceFlowName',
                         'SourceFlowUUID',
                         'SourceFlowContext',
                         'SourceUnit',
                         'MatchCondition',
                         'ConversionFactor',
                         'TargetFlowName',
                         'TargetFlowUUID',
                         'TargetFlowContext',
                         'TargetUnit',
                         'Mapper',
                         'Verifier',
                         'LastUpdated']
    mapping_w_flowinfo = mapping_w_flowinfo[flowmapping_order]


    mapping_w_flowinfo.to_csv(flowmappingpath+source+'.csv',index=False)