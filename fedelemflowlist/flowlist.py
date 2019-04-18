#Assemble pieces to generate the elementary flow list
import pandas as pd
from fedelemflowlist.globals import inputpath,outputpath,list_version_no,flow_types,context_fields,convert_to_lower,as_path
from fedelemflowlist.uuid_generators import generate_flow_uuid,generate_context_uuid
from fedelemflowlist.jsonld_writer import write_flow_list_to_jsonld

#Import flowables by flow class with their units
flows = pd.DataFrame()
#flow_types = list(flow_types.keys())
for t in flow_types:
      input_flows_for_type = pd.read_csv(inputpath + t + '.csv',header=0)
      #Drop if its missing the flow name
      input_flows_for_type = input_flows_for_type.dropna(axis=0,how='all')
      # Add Flow Class to columns
      input_flows_for_type['Class'] = t
      flows = pd.concat([flows,input_flows_for_type])
flows = flows.fillna(value="")

media = ['air','water','ground','biotic']

media_root_lookup  = {}
for m in media:
    media_root_lookup[m] = m + '_root'

#Make directionality lowercase for now if not:
flows["Directionality"] = [convert_to_lower(x) for x in flows["Directionality"]]

#Get compartments relevant for that flow


from fedelemflowlist.compartments import compartment_paths_uuids

#resources =  flows[flows["Directionality"]=='resource']


flow_field_to_keep = flows.columns[0:6]

flows_contexts = pd.DataFrame()
for index,row in flows.iterrows():
    for k,v in media_root_lookup.items():
    #get rows where
        if row[k]==1:
             context = as_path(row["Directionality"],k)
             row[v] = str.lower(row[v])
             context_pieces = [context,row[v]]
             contexts_df = compartment_paths_uuids[
                 compartment_paths_uuids['context'].str.contains(context_pieces[0]) & compartment_paths_uuids[
                     'context'].str.contains(context_pieces[1])]

             contexts_df['Flowable'] = row.loc['Flowable']
             flowable_media_contexts = pd.merge(flows[flow_field_to_keep],contexts_df)
             flows_contexts = flows_contexts.append(flowable_media_contexts)




#keywords = ['emission/air','troposphere']
#







#Loop through flowables, creating flows for each compartment relevant for that flow type, using major





#Loop through flows generating UUID for each
flowids = []
for index,row in flows.iterrows():
        flowid = generate_flow_uuid(row['Flowable'],row[context_fields[0]], row[context_fields[1]], row['Unit'])
        flowids.append(flowid)
flows['Flow UUID'] = flowids

#Get all unique compartment combinations to create contexts
fields_for_generating_context_uuid = ['Class']+context_fields
contexts = flows[fields_for_generating_context_uuid]
contexts = contexts.drop_duplicates()
contextids=[]
for index,row in contexts.iterrows():
        contextid = generate_context_uuid(row[fields_for_generating_context_uuid[0]],
                                          row[fields_for_generating_context_uuid[1]],
                                          row[fields_for_generating_context_uuid[2]])
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



len(flowswithcontextandunitdata)