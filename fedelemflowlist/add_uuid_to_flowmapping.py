"""Add docstring."""
import pandas as pd
from fedelemflowlist.globals import flowmappingpath,outputpath,list_version_no


#Pull in mapping file
mapping = pd.read_csv(flowmappingpath+'/FedElemFlowList_'+list_version_no+'_mapping.csv')
mapping.columns

#Pull in flowlist
flowlist = pd.read_csv(outputpath+'/FedElemFlowList_'+list_version_no+'.csv')
flowlist.columns
flowlist = flowlist[['Flowable','Compartment','Flow UUID']]

mapping_w_id = pd.merge(mapping,flowlist,left_on=['NewName','NewCategory'],right_on=['Flowable','Compartment'],how='left')
mapping_w_id = mapping_w_id.drop(columns=['Flowable','Compartment','UUID'])
#Drop old UUID, replace it with new
mapping_w_id = mapping_w_id.rename(columns={'Flow UUID':'UUID'})

mapping_w_id.to_csv(flowmappingpath+'/FedElemFlowList_'+list_version_no+'_mapping.csv',index=False)