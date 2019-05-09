# Assemble pieces to generate the elementary flow list
import pandas as pd
from fedelemflowlist.globals import log, inputpath, outputpath, list_version_no, flow_classes, as_path
from fedelemflowlist.contexts import context_path_uuid, primary_context_classes, secondary_context_classes
from fedelemflowlist.uuid_generators import make_uuid
from fedelemflowlist.jsonld_writer import write_flow_list_to_jsonld

# Import flowables by flow class with their units, as well as primary flow class membership
flowables = pd.DataFrame()
flowables_w_primary_contexts = pd.DataFrame()
primary_contexts = pd.DataFrame()

for t in flow_classes:
    # Handle flowables first
    flowables_for_class = pd.read_excel(inputpath + t + '.xlsx', sheet_name='Flowables', header=0)
    # Drop if the line is blank
    flowables_for_class = flowables_for_class.dropna(axis=0, how='all')
    # Add Flow Class to columns
    flowables_for_class['Class'] = t
    flowables = pd.concat([flowables, flowables_for_class])
    class_primary_contexts = pd.read_excel(inputpath + t + '.xlsx', sheet_name='FlowablePrimaryContexts', header=0)
    class_primary_contexts = class_primary_contexts.dropna(axis=0, how='all')

    # primary_contexts['Directionality'] = [convert_to_lower(x) for x in primary_contexts["Directionality"]]
    # primary_contexts['Environmental Media'] = [convert_to_lower(x) for x in primary_contexts["Environmental Media"]]

    # merge
    class_flowables_w_primary_contexts = pd.merge(flowables_for_class, class_primary_contexts)
    flowables_w_primary_contexts = pd.concat([flowables_w_primary_contexts, class_flowables_w_primary_contexts],
                                             ignore_index=True)

    primary_contexts_unique = class_primary_contexts[primary_context_classes].drop_duplicates()
    primary_contexts_unique['Class'] = t
    primary_contexts = pd.concat([class_primary_contexts, primary_contexts_unique], ignore_index=True, sort=False)

# flowables = flowables.fillna(value="")

# Read in flowable context membership
SecondaryContextMembership = pd.read_excel(inputpath + 'SecondaryContextMembership.xlsx',
                                           sheet_name='SecondaryContextMembership')  #

# if list(SecondaryContextMembership.columns[1:]) != compartment_classes:
#    log.debug('ERROR: FlowableContextMembership compartment class columns must match Context compartment class columns')

context_patterns_used = pd.DataFrame(
    columns=['Class', 'Directionality', 'Environmental Media', 'Primary_Context_Path', 'Pattern'])
for index, row in SecondaryContextMembership.iterrows():
    pattern = [x for x in secondary_context_classes if row[x] != 0]
    pattern_w_primary = primary_context_classes.copy() + pattern
    # convert to string
    pattern_w_primary = ','.join(pattern_w_primary)
    primary_context_path = as_path(row['Directionality'], row['Environmental Media'])
    context_patterns_used = context_patterns_used.append({'Class': row['FlowClass'],
                                                          'Directionality': row['Directionality'],
                                                          'Environmental Media': row['Environmental Media'],
                                                          'Primary_Context_Path': primary_context_path,
                                                          'Pattern': pattern_w_primary}, ignore_index=True)

# Cycle through these class context patterns and get context_paths
field_to_keep = ['Class', 'Directionality', 'Environmental Media']
class_contexts = pd.DataFrame()
for index, row in context_patterns_used.iterrows():
    class_context_patterns_row = row[field_to_keep]
    # Get the contexts specific to this class by matching the Pattern and Primary_Context_Path
    contexts_df = context_path_uuid[(context_path_uuid['Pattern'] == row['Pattern']) & (
        context_path_uuid['Context'].str.contains(row['Primary_Context_Path']))]
    for f in field_to_keep:
        contexts_df[f] = row[f]
    contexts_df = contexts_df.drop(columns='Pattern')
    class_contexts = pd.concat([class_contexts, contexts_df], ignore_index=True)

# Need to check that the primary context names match the name in the context paths, and that the pattern matches the
# patterns in context_patterns

# Merge this table now with the flowables and primary contexts with the full contexts per class, creating flows for each compartment relevant for that flow type, using major
flows = pd.merge(flowables_w_primary_contexts, class_contexts)

# Loop through flows generating UUID for each
flowids = []
for index, row in flows.iterrows():
    flowid = make_uuid(row['Flowable'], row['Context'], row['Unit'])
    flowids.append(flowid)
flows['Flow UUID'] = flowids

# Import unit metadata (from openLCA)
unit_meta = pd.read_csv(inputpath + 'unit_meta_data.csv', header=0)

# Merge it with the main table
# rename flow propoerty factor temporarily
flows = pd.merge(flows, unit_meta, how='left')

contexts_in_flows = flows[['Context', 'Context UUID']]
contexts_in_flows = contexts_in_flows.drop_duplicates()

# Write it to json-ld
# write_flow_list_to_jsonld(flows, contexts_in_flows)

# Write it to csv
# flows.to_csv(outputpath + 'FedElemFlowList_' + list_version_no + '.csv', index=False)
