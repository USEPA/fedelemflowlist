# Assemble pieces to generate the elementary flow list
import pandas as pd
from fedelemflowlist.globals import log, inputpath, outputpath, as_path,flow_list_specs
from fedelemflowlist.contexts import context_path_uuid
from fedelemflowlist.uuid_generators import make_uuid

flowable_data_types = {'CAS No':'str','Formula':'str','Flowable Preferred':'Int64'}

def read_in_flowclass_file(flowclass,flowclasstype):
    data_types = None
    if flowclasstype=='Flowables':
        data_types = flowable_data_types
    flowclassfile = pd.read_csv(inputpath + flowclass + flowclasstype + '.csv', header=0, dtype=data_types)
    return flowclassfile


if __name__ == '__main__':

    # Import flowables by flow class with their units, as well as primary flow class membership
    flowables = pd.DataFrame()
    flowables_w_primary_contexts = pd.DataFrame()
    primary_contexts = pd.DataFrame()

    # Loop through flow class specific files based on those classes specified in flowlistspecs
    for t in flow_list_specs["flow_classes"]:
        # Handle flowables first
        flowables_for_class = read_in_flowclass_file(t,'Flowables')
        log.info('Import ' + str(len(flowables_for_class)) + ' flowables for class ' + t)
        # Drop if the line is blank
        flowables_for_class = flowables_for_class.dropna(axis=0, how='all')
        #Drop duplicate flowables in list
        flowables_for_class = flowables_for_class.drop_duplicates(subset='Flowable')
        # Add Flow Class to columns
        flowables_for_class['Class'] = t
        flowables = pd.concat([flowables, flowables_for_class], ignore_index=True, sort=False)
        class_primary_contexts = read_in_flowclass_file(t,'FlowablePrimaryContexts')
        flowables_for_class = flowables_for_class.drop_duplicates()
        log.info('Import ' + str(len(class_primary_contexts)) + ' flowable primary contexts for class ' + t)
        class_primary_contexts = class_primary_contexts.dropna(axis=0, how='all')

        #Check that every flowable has a primary context
        flowables_missing_primary_contexts = list(set(flowables_for_class['Flowable']) - set(class_primary_contexts['Flowable']))
        if len(flowables_missing_primary_contexts) > 0:
            log.warning('Flowables ' + str(flowables_missing_primary_contexts) +' are missing primary contexts.')

        # merge
        class_flowables_w_primary_contexts = pd.merge(flowables_for_class, class_primary_contexts)
        log.info('Create ' + str(len(class_flowables_w_primary_contexts)) + ' flows with primary context for class ' + t)
        flowables_w_primary_contexts = pd.concat([flowables_w_primary_contexts, class_flowables_w_primary_contexts],
                                                 ignore_index=True, sort=False)

        primary_contexts_unique = class_primary_contexts[flow_list_specs["primary_context_classes"]].drop_duplicates()
        primary_contexts_unique['Class'] = t
        primary_contexts = pd.concat([class_primary_contexts, primary_contexts_unique], ignore_index=True, sort=False)

    log.info('Total of ' + str(len(flowables_w_primary_contexts)) + ' flows with primary contexts created.')

    # Read in flowable context membership
    SecondaryContextMembership = pd.read_csv(inputpath + 'SecondaryContextMembership.csv')
    log.info('Read in secondary context membership')
    # if list(SecondaryContextMembership.columns[1:]) != compartment_classes:
    #    log.debug('ERROR: FlowableContextMembership compartment class columns must match Context compartment class columns')

    secondary_context_classes = flow_list_specs["secondary_context_classes"]
    context_patterns_used = pd.DataFrame(
        columns=['Class', 'Directionality', 'Environmental Media', 'Primary_Context_Path', 'Pattern','ContextPreferred'])
    for index, row in SecondaryContextMembership.iterrows():
        pattern = [x for x in secondary_context_classes if row[x] != 0]
        pattern_w_primary = flow_list_specs["primary_context_classes"].copy() + pattern
        # convert to string
        pattern_w_primary = ','.join(pattern_w_primary)
        primary_context_path = as_path(row['Directionality'], row['Environmental Media'])
        context_patterns_used = context_patterns_used.append({'Class': row['FlowClass'],
                                                              'Directionality': row['Directionality'],
                                                              'Environmental Media': row['Environmental Media'],
                                                              'Primary_Context_Path': primary_context_path,
                                                              'Pattern': pattern_w_primary,
                                                              'ContextPreferred':row['ContextPreferred']}, ignore_index=True)

    # Cycle through these class context patterns and get context_paths

    #! This code segment is slow - could be improved
    log.info('Getting relevant contexts for each class ...')
    field_to_keep = ['Class', 'Directionality', 'Environmental Media','ContextPreferred']
    class_contexts = pd.DataFrame()
    for index, row in context_patterns_used.iterrows():
        class_context_patterns_row = row[field_to_keep]
        # Get the contexts specific to this class by matching the Pattern and Primary_Context_Path
        contexts_df = context_path_uuid[(context_path_uuid['Pattern'] == row['Pattern']) & (
            context_path_uuid['Context'].str.contains(row['Primary_Context_Path']))]
        for f in field_to_keep:
            contexts_df.loc[:,f] = row[f]
        contexts_df = contexts_df.drop(columns='Pattern')
        class_contexts = pd.concat([class_contexts, contexts_df], ignore_index=True, sort=False)

    # Need to check that the primary context names match the name in the context paths, and that the pattern matches the
    # patterns in context_patterns

    # Merge this table now with the flowables and primary contexts with the full contexts per class, creating flows for each compartment relevant for that flow type, using major
    flows = pd.merge(flowables_w_primary_contexts, class_contexts, on=['Class','Directionality','Environmental Media'])

    #Drop duplicate flows if they exist
    if len(flows[flows.duplicated(keep=False)])>0:
        log.debug("Duplicate flows exist. They will be removed.")
        flows = flows.drop_duplicates()

    #If both the flowable and context are preferred, make this a preferred flow
    flows['Preferred'] = 0
    flows.loc[(flows['Flowable Preferred']==1) & (flows['ContextPreferred']==1),'Preferred'] = 1

    #Drop unneeded columns
    cols_to_drop = ['Flowable Preferred','ContextPreferred','Directionality','Environmental Media']
    flows = flows.drop(columns=cols_to_drop)

    # Loop through flows generating UUID for each
    flowids = []
    log.info('Generating unique UUIDs for each flow...')
    for index, row in flows.iterrows():
        flowid = make_uuid(row['Flowable'], row['Context'], row['Unit'])
        flowids.append(flowid)
    flows['Flow UUID'] = flowids

    contexts_in_flows = flows[['Context', 'Context UUID']]
    contexts_in_flows = contexts_in_flows.drop_duplicates()
    log.info('Created ' + str(len(flows)) + ' flows with ' + str(len(contexts_in_flows))  + ' unique contexts')


    # Write it to parquet
    flows.to_parquet(outputpath + 'FedElemFlowListMaster.parquet', engine='pyarrow')
    log.info('Stored flows in ' + 'output/FedElemFlowListMaster.parquet')
