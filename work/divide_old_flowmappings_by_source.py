
import pandas as pd
from fedelemflowlist.globals import outputpath, flowmappingpath

oldmapping = pd.read_csv('work/FedElemFlowList_0.1_mapping.csv',header=0)

old_to_new_fl_context = {'TargetFlowContext':['air','ground','water'],'NewTargetFlowContext':['emission/air','emission/ground','emission/water']}

old_to_new_fl_context_df = pd.DataFrame(old_to_new_fl_context)
oldmapping = pd.merge(oldmapping, old_to_new_fl_context_df)


#Replace old UUIDs

import fedelemflowlist as fl
all_flows = fl.get_flows()
all_flows = all_flows[['Flowable','Context','Flow UUID']]
oldmapping = pd.merge(oldmapping,all_flows,left_on=['TargetFlowName','NewTargetFlowContext'],right_on=['Flowable','Context'])
oldmapping = oldmapping.drop(columns=['TargetFlowContext','SourceListVersion','Flowable','Context','TargetFlowUUID'])
oldmapping = oldmapping.rename(columns={'NewTargetFlowContext':'TargetFlowContext','Flow UUID':'TargetFlowUUID'})
oldmapping['SourceFlowUUID'] = None
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
oldmapping =oldmapping[flowmapping_order]

import time
oldmapping['LastUpdated'] = '07/20/2018'


for s in oldmapping['SourceListName']:
    mapping = oldmapping[oldmapping['SourceListName']==s]
    mapping.to_csv(flowmappingpath+s+'.csv',index=False)



