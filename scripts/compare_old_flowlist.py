"""
Use an archived flowlist parquet file to load in and compare with the current list.
Write csvs of the new flows and expired flows in csv format, write new flows to JSON-LD
Currently compares only by UUID.
"""

import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import outputpath

# get the current list

# Enter name of old version here. Must be in output folder
old_version_parquet = 'FedElemFlowListMaster_1.0rc4.parquet'

if __name__ == '__main__':
    current_list = fedelemflowlist.get_flows()

    # get UUIDs
    current_UUIDs = current_list['Flow UUID']

    # load old version from output folder

    list_file = outputpath + old_version_parquet
    old_list = pd.read_parquet(list_file, engine="pyarrow")
    old_list_UUIDs = old_list['Flow UUID']

    new_UUIDS = list(set(current_UUIDs) - set(old_list_UUIDs))
    new_flows = current_list[current_list['Flow UUID'].isin(new_UUIDS)]
    new_flows.to_csv(outputpath + 'new_flows.csv', index=False)
    fedelemflowlist.write_jsonld(new_flows, outputpath + 'FedElemFlowList_newflows.zip')
    expired_UUIDs = list(set(old_list_UUIDs) - set(current_UUIDs))
    expired_flows = old_list[old_list['Flow UUID'].isin(expired_UUIDs)]

    expired_flows.to_csv(outputpath + 'expired_flows.csv', index=False)
