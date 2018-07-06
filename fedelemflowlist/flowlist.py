#Assemble pieces to generate the elementary flow list
import pandas as pd
import iomb.util
from fedelemflowlist.globals import inputpath,outputpath,list_version_no,flow_types,context_fields

#Import by flow type
#Later can loop through by defined type

flows = pd.DataFrame()
for t in flow_types:
      input_flows_for_type = pd.read_csv(inputpath + t + '_flows.csv',header=0)
      flows = pd.concat([flows,input_flows_for_type])

from fedelemflowlist.uuid_generators import generate_flow_uuid
#Loop through flows generating UUID for each
flowids = []
for index,row in flows.iterrows():
        #flowid = iomb.util.make_uuid(row['Flowable'],row['Flow directionality'], row['Flow compartment'], row['Unit'])
        flowid = generate_flow_uuid(row['Flowable'],row[context_fields[0]], row[context_fields[1]], row['Unit'])
        flowids.append(flowid)
flows['Flow UUID'] = flowids

#Get all unique compartment combinations to create contexts
contexts = flows[context_fields]
contexts = contexts.drop_duplicates()
from fedelemflowlist.uuid_generators import generate_context_uuid
contextids=[]
for index,row in contexts.iterrows():
        contextid = generate_context_uuid(row[context_fields[0]], row[context_fields[1]])
        contextids.append(contextid)
contexts['Context UUID'] = contextids

#Merge back in with flow list
flowswithcontext = pd.merge(flows,contexts,on=context_fields)

#Import unit metadata (from openLCA)
unit_meta = pd.read_csv(inputpath+'unit_meta_data.csv',header=0)

#Merge it with the main table
#rename flow propoerty factor temporarily
flowswithcontext = flowswithcontext.rename(columns={'Flow property factor':'Flow quality'})
flowswithcontextandunitdata = pd.merge(flowswithcontext,unit_meta,left_on=['Flow quality','Unit'],
                                       right_on=['Quality','Unit'],how='left')
flowswithcontextandunitdata = flowswithcontextandunitdata.drop(columns='Quality')

#Write it to json-ld
from fedelemflowlist.jsonld_writer import write_flow_list_to_jsonld
write_flow_list_to_jsonld(flowswithcontextandunitdata)

#Save it to csv
flowswithcontextandunitdata.to_csv(outputpath + 'FedElemFlowList_' + list_version_no + '.csv',index=False)

#Save to pickle
#pd.to_pickle(flows,'./output/ElementaryFlowList')


