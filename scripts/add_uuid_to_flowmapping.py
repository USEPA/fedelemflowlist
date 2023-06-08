"""
Gets Fed Commons Flow UUID.

From mapping list and adds it to mapping file(s). Mapping file must already
conform to mapping format.
"""
import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import flowmappingpath, add_uuid_to_mapping


#Add source name here. The .csv mapping file with this name must be in the flowmapping directory
#None can be used to update UUIDs in all mapping files
source = None

if __name__ == '__main__':
    # Pull in mapping file
    mapping = fedelemflowlist.get_flowmapping(source)
    
    mapping_w_flowinfo = add_uuid_to_mapping(mapping)

    for s in pd.unique(mapping_w_flowinfo['SourceListName']):
        mapping = mapping_w_flowinfo[mapping_w_flowinfo['SourceListName'] == s]
        mapping.to_csv(flowmappingpath / f'{s}.csv', index=False)
