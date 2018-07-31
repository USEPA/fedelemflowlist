#Assemble pieces to generate the elementary flow list
import pandas as pd
from fedelemflowlist.globals import inputpath,outputpath,list_version_no,flow_types,context_fields
from fedelemflowlist.uuid_generators import generate_flow_uuid,generate_context_uuid
from fedelemflowlist.jsonld_writer import write_flow_list_to_jsonld

#Import by flow type
flows = pd.DataFrame()
flow_types = list(flow_types.keys())
for t in flow_types:
      input_flows_for_type = pd.read_csv(inputpath + t + '.csv',header=0)
      #Drop if its missing the flow name
      input_flows_for_type = input_flows_for_type.dropna(axis=0,how='all')
      # Add Flow Class to columns
      input_flows_for_type['Class'] = t
      flows = pd.concat([flows,input_flows_for_type])
flows = flows.fillna(value="")

#Make directionality lowercase for now if not:
def convert_to_lower(x):
    x = str(x)
    x = str.lower(x)
    return x
flows["Directionality"] = [convert_to_lower(x) for x in flows["Directionality"]]

#Loop through flows generating UUID for each
flowids = []
for index,row in flows.iterrows():
        flowid = generate_flow_uuid(row['Flowable'],row[context_fields[0]], row[context_fields[1]], row['Unit'])
        flowids.append(flowid)
flows['Flow UUID'] = flowids

#Get all unique compartment combinations to create contexts
contexts = flows[context_fields]
contexts = contexts.drop_duplicates()
contextids=[]
for index,row in contexts.iterrows():
        contextid = generate_context_uuid(row[context_fields[0]], row[context_fields[1]])
        contextids.append(contextid)
contexts['Compartment UUID'] = contextids

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
write_flow_list_to_jsonld(flowswithcontextandunitdata,contexts)

#Write it to csv
flowswithcontextandunitdata.to_csv(outputpath + 'FedElemFlowList_' + list_version_no + '.csv',index=False)



