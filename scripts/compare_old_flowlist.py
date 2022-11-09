"""
Use an archived flowlist parquet file to load in and compare with the current list.

Write csvs of the new flows and expired flows in csv format, write new flows to JSON-LD
Currently compares only by UUID.
"""

import fedelemflowlist
from fedelemflowlist.globals import outputpath, flow_list_specs,\
    load_flowlist

# get the current list

# Enter name of old version here. Must be in output folder
old_version = '1.0.8'

if __name__ == '__main__':
    current_list = load_flowlist()
    ver = flow_list_specs['list_version']
    # get UUIDs
    current_UUIDs = current_list['Flow UUID']

    # load old version from output folder
    old_list = load_flowlist(version=old_version)
    old_list_UUIDs = old_list['Flow UUID']

    new_UUIDS = list(set(current_UUIDs) - set(old_list_UUIDs))
    new_flows = current_list[current_list['Flow UUID'].isin(new_UUIDS)]
    new_flows.to_csv(f"{outputpath}/new_flows{old_version}to{ver}.csv",
                     index=False)
    fedelemflowlist.write_jsonld(new_flows,
                                 f"{outputpath}/FedElemFlowList_newflows{old_version}to{ver}.zip")
    expired_UUIDs = list(set(old_list_UUIDs) - set(current_UUIDs))
    expired_flows = old_list[old_list['Flow UUID'].isin(expired_UUIDs)]
    expired_flows.to_csv(f"{outputpath}/expired_flows{old_version}to{ver}.csv",
                         index=False)
