"""Exports flows and flowmappings for a selecting mapping file."""
import fedelemflowlist
import pandas as pd
from fedelemflowlist.globals import outputpath

# Set name of mapping file. More than one mapping file can be used
mapping_to_use = ['openLCA']

if __name__ == '__main__':
    mapping = fedelemflowlist.get_flowmapping(mapping_to_use)
    # Get Flow UUIDs for flows used in selected mapping
    mapping_flow_uuids = pd.DataFrame(pd.unique(mapping['TargetFlowUUID']),
                                      columns=["Flow UUID"])

    # Get all flows
    all_flows = fedelemflowlist.get_flows()
    # Subset all flows to get just those used in selected mapping
    flows_used_in_mapping =  pd.merge(all_flows, mapping_flow_uuids)

    # Now write out flows and mappings
    export_name = ''
    if isinstance(mapping_to_use, str):
        mapping_to_use = [mapping_to_use]
    for s in mapping_to_use:
        export_name = export_name + s + '_'
    export_name = export_name + 'flows_w_mappings.zip'
    fedelemflowlist.write_jsonld(flows_used_in_mapping,
                                 outputpath / export_name,
                                 mapping)
    print(f"File saved to {outputpath / export_name}")
