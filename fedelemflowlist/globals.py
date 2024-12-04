"""Set common variables for use in package."""
import sys
from pathlib import Path
import logging as log
import fedelemflowlist
import pandas as pd
from datetime import datetime
from esupy.processed_data_mgmt import Paths, FileMeta, \
    load_preprocessed_output, write_df_to_file, download_from_remote
from esupy.util import get_git_hash

MODULEPATH = Path(__file__).resolve().parent

inputpath = MODULEPATH / 'input'
inputpath_mapping = inputpath / 'mapping input'
flowmappingpath = MODULEPATH / 'flowmapping/'

fedefl_path = Paths()
fedefl_path.local_path = fedefl_path.local_path / 'fedelemflowlist'
outputpath = fedefl_path.local_path
WRITE_FORMAT = 'parquet'
GIT_HASH = get_git_hash()

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
    "package_version": "1.2.5",
    "list_version": "1.3.0",
    "flow_classes": ["Biological", "Chemicals", "Energy", "Geological",
                     "Groups", "Land", "Other", "Water"],
    "primary_context_classes": ["Directionality", "Environmental Media"],
    "secondary_context_classes": ["Vertical Strata", "Land Use",
                                  "Human-Dominated", "Terrestrial",
                                  "Aquatic Feature", "Indoor",
                                  "Population Density", "Release Height"]
    }


def set_metadata(version=None):
    meta = FileMeta()
    meta.name_data = 'FedElemFlowListMaster'
    meta.tool = "fedelemflowlist"
    if not version:
        version = flow_list_specs['list_version']
    else:
        meta.name_data = f"{meta.name_data}_v{version}"
    meta.tool_version = version
    meta.ext = WRITE_FORMAT
    meta.git_hash = GIT_HASH
    meta.date_created = datetime.now().strftime('%d-%b-%Y')
    return meta


def store_flowlist(df):
    meta = set_metadata()
    try:
        log.info(f'saving flowlist to {fedefl_path.local_path}')
        write_df_to_file(df, fedefl_path, meta)
    except:
        log.error('Failed to save flowlist')


def load_flowlist(version=None, download_if_missing=True):
    meta = set_metadata(version)
    df = load_preprocessed_output(meta, fedefl_path)
    if df is None and download_if_missing:
        log.info('Flowlist not found, downloading from remote...')
        download_from_remote(meta, fedefl_path)
        df = load_preprocessed_output(meta, fedefl_path)
    if df is None:
        log.info('Flowlist not found, generating locally...')
        fedelemflowlist.flowlist.generate_flowlist()
        df = load_preprocessed_output(meta, fedefl_path)
        if df is None:
            log.error('Error retrieving flowlist')
            raise FileNotFoundError
    return df


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
                 f"{datetime.now().strftime('%Y_%m_%d')}.csv")
        dropped.to_csv(f'{outputpath}/{fname}', index=False)
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
