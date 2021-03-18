"""
Adds conversion factor to mapping files if source unit is an alternate unit.

Requires target unit to be the primary unit. Existing conversion factor must be
set to 1 to avoid replacing manual conversion factors. Mapping file must already
conform to mapping format.
"""
import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import flowmappingpath, flowmapping_fields, log,\
    add_conversion_to_mapping

#Add source name here. The .csv mapping file with this name must be in the flowmapping directory
#None can be used to add conversions in all mapping files
source = 'ReCiPe2016'

if __name__ == '__main__':
    # Pull in mapping file
    mapping = fedelemflowlist.get_flowmapping(source)

    mapping_w_conversion = add_conversion_to_mapping(mapping)

    flowmapping_order = list(flowmapping_fields.keys())
    mapping_w_conversion =  mapping_w_conversion[flowmapping_order]

    for s in pd.unique( mapping_w_conversion['SourceListName']):
        mapping =  mapping_w_conversion[ mapping_w_conversion['SourceListName'] == s]
        mapping.to_csv(flowmappingpath + s + '.csv', index=False)
