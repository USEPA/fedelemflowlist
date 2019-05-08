#Assemble pieces to generate the elementary flow list
import pandas as pd
from fedelemflowlist.globals import inputpath,outputpath,list_version_no,flow_classes,context_fields,convert_to_lower,as_path
from fedelemflowlist.contexts import context_path_uuid,compartment_classes,primary_context_classes,secondary_context_classes
from fedelemflowlist.uuid_generators import make_uuid
from fedelemflowlist.jsonld_writer import write_flow_list_to_jsonld

import logging as log
log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

#Import flowables by flow class with their units, as well as flow class membership
flowables = pd.DataFrame()
flowables_w_primary_contexts = pd.DataFrame()
primary_contexts = pd.DataFrame()
#flow_types = list(flow_types.keys())
for t in flow_classes:
      #Handle flowables first
      flowables_for_class = pd.read_excel(inputpath + t + '.xlsx', sheet_name='Flowables', header=0)
      #Drop if its missing the flow name
      flowables_for_class = flowables_for_class.dropna(axis=0, how='all')
      # Add Flow Class to columns
      flowables_for_class['Class'] = t
      flowables = pd.concat([flowables, flowables_for_class])
      class_primary_contexts =  pd.read_excel(inputpath + t + '.xlsx', sheet_name='FlowablePrimaryContexts', header=0)
      class_primary_contexts = class_primary_contexts.dropna(axis=0,how='all')

      #primary_contexts['Directionality'] = [convert_to_lower(x) for x in primary_contexts["Directionality"]]
      #primary_contexts['Environmental Media'] = [convert_to_lower(x) for x in primary_contexts["Environmental Media"]]


      #merge
      class_flowables_w_primary_contexts = pd.merge(flowables_for_class,class_primary_contexts)
      flowables_w_primary_contexts = pd.concat([flowables_w_primary_contexts,class_flowables_w_primary_contexts],ignore_index=True)

      primary_contexts_unique = class_primary_contexts[primary_context_classes].drop_duplicates()
      primary_contexts_unique['Class']=t
      primary_contexts = pd.concat([class_primary_contexts,primary_contexts_unique])
flowables = flowables.fillna(value="")


#Get compartments relevant for that flow


#resources =  flows[flows["Directionality"]=='resource']




#Read in flowable context membership
SecondaryContextMembership = pd.read_excel(inputpath + 'SecondaryContextMembership.xlsx', sheet_name='SecondaryContextMembership') #
#Create a dictionary describing what secondary context classes go with each flow class

if list(SecondaryContextMembership.columns[1:]) != compartment_classes:
    log.debug('ERROR: FlowableContextMembership compartment class columns must match Context compartment class columns')

#compartment_classes_in_flow_class = {}
#for index,row in SecondaryContextMembership.iterrows():
#    flow_class_pattern = [compartment_classes[x-1] for x in range(1, max_compartment_classes+1) if row[x] != 0]
#    compartment_classes_in_flow_class[row['FlowClass']]=flow_class_pattern
#compartment_classes_in_flow_class['Biological']

class_context_patterns = pd.DataFrame(columns=['Class', 'Directionality', 'Environmental Media','Primary_Context_Path','Pattern'])
index_first_secondary_compartment = list(SecondaryContextMembership.columns).index(secondary_context_classes[0])
index_last_secondary_compartment = list(SecondaryContextMembership.columns).index(secondary_context_classes[len(secondary_context_classes)-1])
for index,row in SecondaryContextMembership.iterrows():
    pattern = [compartment_classes[x] for x in range(index_first_secondary_compartment, index_last_secondary_compartment) if row[x] != 0]
    pattern_w_primary = primary_context_classes.copy() + pattern
    #convert to string
    pattern_w_primary = ','.join(pattern_w_primary)
    primary_context_path = as_path(row['Directionality'],row['Environmental Media'])
    class_context_patterns = class_context_patterns.append({'Class':row['FlowClass'],
                                                                    'Directionality':row['Directionality'],
                                                                    'Environmental Media': row['Environmental Media'],
                                                                    'Primary_Context_Path':primary_context_path,
                                                                    'Pattern':pattern_w_primary}, ignore_index=True)

#Cycle through these class context patterns and get context_paths
field_to_keep = ['Class', 'Directionality', 'Environmental Media']
class_contexts = pd.DataFrame()
for index,row in class_context_patterns.iterrows():
    class_context_patterns_row = row[field_to_keep]
    #Get the contexts specific to this class by matching the Pattern and Primary_Context_Path
    contexts_df = context_path_uuid[(context_path_uuid['Pattern']==row['Pattern']) & (context_path_uuid['Context'].str.contains(row['Primary_Context_Path']))]
    for f in field_to_keep:
        contexts_df[f]=row[f]
    contexts_df = contexts_df.drop(columns='Pattern')
    class_contexts = pd.concat([class_contexts,contexts_df],ignore_index=True)



#Need to check that the primary context names match the name in the context paths, and that the pattern matches the
# patterns in context_patterns



#Merge this table now with the flowables and primary contexts with the full contexts per class, creating flows for each compartment relevant for that flow type, using major
flows = pd.merge(flowables_w_primary_contexts,class_contexts)

#Loop through flows generating UUID for each
from fedelemflowlist.uuid_generators import make_uuid
flowids = []
for index,row in flows.iterrows():
    flowid = make_uuid(row['Flowable'],row['Context'],row['Unit'])
    flowids.append(flowid)
flows['Flow UUID'] = flowids

#Import unit metadata (from openLCA)
unit_meta = pd.read_csv(inputpath+'unit_meta_data.csv',header=0)

#Merge it with the main table
#rename flow propoerty factor temporarily
flows = pd.merge(flows,unit_meta,how='left')

contexts_in_flows = flows[['Context','Context_UUID']]
contexts_in_flows = contexts_in_flows.drop_duplicates()

#Write it to json-ld
write_flow_list_to_jsonld(flows,contexts_in_flows)

#Write it to csv
#flows.to_csv(outputpath + 'FedElemFlowList_' + list_version_no + '.csv',index=False)



len(flowswithcontextandunitdata)