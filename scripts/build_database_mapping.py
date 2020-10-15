import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath, flowmapping_fields, log, flowmappingpath

#Input source name here. The .csv mapping file with this name must be in the input directory
source_name = 'TRI'

# Pull flowable mapping file. Assume these are in input folder with lcia_name+standardname.csv
flowables = pd.read_csv(inputpath + source_name + '_FlowableMappings.csv')
len(flowables)

# Pull context mapping file. Assume these are in input folder with lcia_name+standardname.csv
context_mappings = pd.read_csv(inputpath + source_name + '_ContextMappings.csv')
len(context_mappings)

# Combined flowables and context files for every combination
flowables['target'] = 1
context_mappings['target'] = 1

flow_mapping = pd.merge(flowables,context_mappings,on='target').drop('target',axis=1)
len(flow_mapping)

# Remove extraneous columns
flow_mapping = flow_mapping.drop(columns=['Map method', 'Note'])

# Add source name name and missing fields
flow_mapping['SourceListName'] = source_name
flow_mapping['ConversionFactor'] = 1
flow_mapping['SourceFlowUUID'] = ""
flow_mapping['TargetFlowUUID'] = ""

# Reorder the mappings
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

# Pull in default conversion factors
conversions = fedelemflowlist.get_alt_conversion()

# merge in conversion factors where source unit = alternate unit
flow_mapping = pd.merge(flow_mapping, conversions, how='left',
                                  left_on=['TargetFlowName', 'SourceUnit', 'TargetUnit'],
                                  right_on=['Flowable', 'AltUnit', 'Unit'])

# update conversion factor where current conversion is 1 and the updated conversion exists
converted1 = flow_mapping['InverseConversionFactor'].notnull()
converted2 = flow_mapping['ConversionFactor']==1
flow_mapping['Convert'] = converted1 & converted2
flow_mapping.loc[(flow_mapping['Convert']==True),
                             'ConversionFactor']=flow_mapping['InverseConversionFactor']
converted = flow_mapping['Convert'].sum()
log.info('added conversion factors for ' + str(converted) + ' flows')
flow_mapping = flow_mapping.drop(columns=['Flowable','Unit',
                                                         'AltUnit','AltUnitConversionFactor',
                                                         'InverseConversionFactor', 'Convert'])

# Add UUIDs from FEDEFL
mapping_length = len(flow_mapping)
all_flows = fedelemflowlist.get_flows()
all_flows = all_flows[['Flowable', 'Context', 'Flow UUID', 'Unit']]
flow_mapping = pd.merge(flow_mapping, all_flows,
                                  left_on=['TargetFlowName', 'TargetFlowContext', 'TargetUnit'],
                                  right_on=['Flowable', 'Context', 'Unit'])
flow_mapping = flow_mapping.drop(columns=['TargetFlowUUID', 'Flowable',
                                                          'Context', 'Unit'])
flow_mapping = flow_mapping.rename(columns={'Flow UUID': 'TargetFlowUUID'})
mapping_merged_len = len(flow_mapping)
if mapping_length > mapping_merged_len:
    log.debug("Not all flows were mapped to flows in the list")

flowmapping_order = list(flowmapping_fields.keys())
flow_mapping = flow_mapping[flowmapping_order]

# Write them to a csv
flow_mapping.to_csv(flowmappingpath + source_name + 'new.csv', index=False)
