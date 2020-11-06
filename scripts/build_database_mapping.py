import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath, flowmapping_fields, log, flowmappingpath,\
    add_uuid_to_mapping, add_conversion_to_mapping

#Input source name here. The .csv mapping file with this name must be in the input directory
source_name = 'TRI'

if __name__ == '__main__':
    # Pull flowable mapping file. Assume these are in input folder with source_name+FlowableMappings.csv
    flowables = pd.read_csv(inputpath + source_name + '_FlowableMappings.csv')
    flowables.sort_values(by=['SourceFlowName'],inplace=True, ignore_index=True)
    if flowables.duplicated(subset=['SourceFlowName']).any():
        log.warning('Duplicate source flows in flowables list:')
        dup = flowables.loc[flowables.duplicated(subset=['SourceFlowName'])]
        log.warning(dup.SourceFlowName.tolist())
        flowables.drop_duplicates(subset=['SourceFlowName'],inplace=True, ignore_index=True)
    
    # Pull context mapping file. Assume these are in input folder with source_name+ContextMappings.csv
    context_mappings = pd.read_csv(inputpath + source_name + '_ContextMappings.csv')
    
    # Combined flowables and context files for every combination
    flowables['target'] = 1
    context_mappings['target'] = 1
    flow_mapping = pd.merge(flowables,context_mappings,on='target').drop('target',axis=1)
    
    # Remove extraneous columns
    flow_mapping = flow_mapping.drop(columns=['Map method', 'Note'])
    
    # Add source name name and missing fields
    flow_mapping['SourceListName'] = source_name
    flow_mapping['SourceFlowUUID'] = ""
    flow_mapping['TargetFlowUUID'] = ""
    if 'ConversionFactor' not in flow_mapping:
        flow_mapping['ConversionFactor'] = 1
        log.info('ConversionFactor column not included in input file, added to mapping')
    flow_mapping['ConversionFactor']=flow_mapping['ConversionFactor'].fillna(1)

    flow_mapping = add_conversion_to_mapping(flow_mapping)
    
    flow_mapping = add_uuid_to_mapping(flow_mapping)
    
    # Write them to a csv
    flow_mapping.to_csv(flowmappingpath + source_name + '.csv', index=False)
