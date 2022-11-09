"""Set common variables for use in package."""
import sys
import os
import logging as log
import fedelemflowlist
import pandas as pd
import datetime

try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'fedelemflowlist/'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'
inputpath_mapping = inputpath + 'mapping input/'
flowmappingpath = modulepath + 'flowmapping/'

flow_list_fields = {'Flowable': [{'dtype': 'str'}, {'required': True}],
                    'CAS No': [{'dtype': 'str'}, {'required': False}],
                    'Formula': [{'dtype': 'str'}, {'required': False}],
                    'Synonyms': [{'dtype': 'str'}, {'required': False}],
                    'Unit': [{'dtype': 'str'}, {'required': True}],
                    'Class': [{'dtype': 'str'}, {'required': True}],
                    'External Reference': [{'dtype': 'str'}, {'required': False}],
                    'Preferred': [{'dtype': 'int'}, {'required': False}],
                    'Context': [{'dtype': 'str'}, {'required': True}],
                    'Flow UUID': [{'dtype': 'str'}, {'required': True}],
                    'AltUnit': [{'dtype': 'str'}, {'required': False}],
                    'AltUnitConversionFactor': [{'dtype': 'float'}, {'required': False}]
                    }
flowmapping_fields = {'SourceListName': [{'dtype': 'str'}, {'required': True}],
                      'SourceFlowName': [{'dtype': 'str'}, {'required': True}],
                      'SourceFlowUUID': [{'dtype': 'str'}, {'required': False}],
                      'SourceFlowContext': [{'dtype': 'str'}, {'required': True}],
                      'SourceUnit': [{'dtype': 'str'}, {'required': True}],
                      'MatchCondition': [{'dtype': 'str'}, {'required': False}],
                      'ConversionFactor': [{'dtype': 'float'}, {'required': False}],
                      'TargetFlowName': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowUUID': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowContext': [{'dtype': 'str'}, {'required': True}],
                      'TargetUnit': [{'dtype': 'str'}, {'required': True}],
                      'Mapper': [{'dtype': 'str'}, {'required': False}],
                      'Verifier': [{'dtype': 'str'}, {'required': False}],
                      'LastUpdated': [{'dtype': 'str'}, {'required': False}]}

log.basicConfig(level=log.INFO, format='%(levelname)s %(message)s',
                stream=sys.stdout)

flow_list_specs = {
    "list_version": "1.0.9",
    "flow_classes": ["Biological", "Chemicals", "Energy", "Geological",
                     "Groups", "Land", "Other", "Water"],
    "primary_context_classes": ["Directionality", "Environmental Media"],
    "secondary_context_classes": ["Vertical Strata", "Land Use",
                                  "Human-Dominated", "Terrestrial",
                                  "Aquatic Feature", "Indoor",
                                  "Population Density", "Release Height"]
    }


def as_path(*args: str) -> str:
    """Converts strings to lowercase path-like string
    Take variable order of string inputs
    :param args: variable-length of strings
    :return: string
    """
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).strip().lower())
    return "/".join(strings)

def add_uuid_to_mapping(flow_mapping):
    """
    Adds UUIDs from FEDEFL to a flow mapping file
    :param flow_mapping: dataframe of flow mapping in standard format
    return: flow_mapping_uuid
    """
    mapping_length = len(flow_mapping)
    all_flows = fedelemflowlist.get_flows()
    all_flows = all_flows[['Flowable', 'Context', 'Flow UUID', 'Unit']]
    flow_mapping = pd.merge(flow_mapping, all_flows, how='left',
                            left_on=['TargetFlowName', 'TargetFlowContext', 'TargetUnit'],
                            right_on=['Flowable', 'Context', 'Unit'])
    columns_to_drop = ['Flowable','Context', 'Unit']
    if 'TargetFlowUUID' in flow_mapping:
        columns_to_drop.append('TargetFlowUUID')
    flow_mapping = flow_mapping.drop(columns=columns_to_drop)
    flow_mapping = flow_mapping.rename(columns={'Flow UUID': 'TargetFlowUUID'})
    flow_mapping_uuid = flow_mapping.dropna(subset=['TargetFlowUUID'])
    mapping_merged_len = len(flow_mapping_uuid)
    if mapping_length > mapping_merged_len:
        log.warning("UUIDs not available for all flows")
        dropped = flow_mapping.loc[~flow_mapping.index.isin(flow_mapping_uuid.index)]
        dropped = (dropped[['TargetFlowName','TargetFlowContext']]
                   .drop_duplicates()
                   .reset_index(drop=True))
        fname = (f"LOG_FlowsMappedWNoUUIDsFound_"
                 f"{datetime.datetime.now().strftime('%Y_%m_%d')}.csv")
        dropped.to_csv(outputpath + fname, index=False)
        log.info(f"Mapped flows without UUIDs written to {fname}")
    flow_mapping_uuid.reset_index(drop=True, inplace=True)
    flowmapping_order = [c for c in list(flowmapping_fields.keys())
                         if c in flow_mapping_uuid.columns.tolist()]
    flow_mapping_uuid = flow_mapping_uuid[flowmapping_order]

    return flow_mapping_uuid

def add_conversion_to_mapping(flow_mapping):
    """
    Adds conversion factors from FEDEFL to a flow mapping file
    :param flow_mapping: dataframe of flow mapping in standard format
    return: mapping_w_conversion
    """
    conversions = fedelemflowlist.get_alt_conversion()
    # merge in conversion factors where source unit = alternate unit
    mapping_w_conversion = pd.merge(flow_mapping, conversions, how='left',
                                    left_on=['TargetFlowName', 'SourceUnit', 'TargetUnit'],
                                    right_on=['Flowable', 'AltUnit', 'Unit'])

    # update conversion factor where current conversion is 1 and the updated conversion exists
    converted1 = mapping_w_conversion['InverseConversionFactor'].notnull()
    converted2 = mapping_w_conversion['ConversionFactor']==1
    mapping_w_conversion['Convert']=converted1 & converted2
    mapping_w_conversion.loc[(mapping_w_conversion['Convert']==True),
                             'ConversionFactor']=mapping_w_conversion['InverseConversionFactor']
    converted = mapping_w_conversion['Convert'].sum()
    log.info('added conversion factors for ' + str(converted) + ' flows')
    mapping_w_conversion = (mapping_w_conversion
                            .drop(columns=['Flowable','Unit', 'AltUnit',
                                           'AltUnitConversionFactor',
                                           'InverseConversionFactor',
                                           'Convert'])
                            )
    return mapping_w_conversion
