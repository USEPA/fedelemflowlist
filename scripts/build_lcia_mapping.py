"""
Builds the mapping file for LCIA methods.

Using input flowable and context mappings, and the lcia_formatter
Requires lciafmt from lcia_formatter (https://github.com/USEPA/lciaformatter)
BEWARE this will replace the existing mapping file if it exists in /flowmapping.
"""

import pandas as pd
from fedelemflowlist.globals import inputpath_mapping, flowmappingpath, \
    add_uuid_to_mapping, add_conversion_to_mapping

# Options: 'TRACI2.1', 'ReCiPe2016', 'ImpactWorld+, 'IPCC'
lcia_name = 'IPCC'


if __name__ == '__main__':
    ## Bring in flowables and contexts from the lcia_formatter
    import lciafmt
    lcia_lciafmt = lciafmt.get_method(lcia_name, endpoint = False)
    lcia_endpoint = lciafmt.get_method(lcia_name, endpoint = True)
    lcia_lciafmt = lcia_lciafmt.append(lcia_endpoint, ignore_index = True)
   
    # Keep only flowable and category
    lcia_lciafmt = lcia_lciafmt[['Flowable', 'Context']]
    lcia_lciafmt = lcia_lciafmt.drop_duplicates()

    # Add in context matches. Assume these are in inputfolder with lcia_name+standardname.csv
    def get_manual_mappings(source, ftype):
        """
        Loads a csv mapping file
        :param source: source name
        :param ftype: 'Flowable' or 'Context'
        :return: mapping file
        """
        mappings = pd.read_csv(inputpath_mapping / f'{source}{ftype}Mappings.csv')
        return mappings

    context_mappings = get_manual_mappings(lcia_name, 'Context')
    lciafmt_w_context_mappings = pd.merge(lcia_lciafmt, context_mappings,
                                          left_on='Context',
                                          right_on='SourceFlowContext')
    # Drop duplicate field
    lciafmt_w_context_mappings = lciafmt_w_context_mappings.drop(columns=['Context'])

    # Add in flowable matches. Assume these are in inputfolder with lcia_name+standardname.csv
    flowable_mappings = get_manual_mappings(lcia_name, 'Flowable')
    
    left_field = 'Flowable'
    right_field = 'SourceFlowName'
    columns_to_drop = ['Flowable']
    
    if lcia_name == 'ReCiPe2016':
        # Make all flowables lowercase to resolve case sensitivity issues in ReCiPe
        flowable_mappings['SourceFlowName_low'] = flowable_mappings['SourceFlowName'].str.lower()
        lciafmt_w_context_mappings['Flowable_low']=lciafmt_w_context_mappings['Flowable'].str.lower()
        left_field = 'Flowable_low'
        right_field = 'SourceFlowName_low'
        columns_to_drop.extend([left_field,right_field])
        
    lciafmt_w_context_flowable_mappings = pd.merge(lciafmt_w_context_mappings,
                                                   flowable_mappings,
                                                   left_on = left_field,
                                                   right_on = right_field)

    # Drop duplicate field
    lciafmt_w_context_flowable_mappings = lciafmt_w_context_flowable_mappings.drop(columns=columns_to_drop)

    # Add LCIA name and missing fields
    lciafmt_w_context_flowable_mappings['SourceListName'] = lcia_name
    lciafmt_w_context_flowable_mappings['ConversionFactor'] = 1
    lciafmt_w_context_flowable_mappings['SourceFlowUUID'] = None
    
    # Add conversion factors
    lciafmt_w_context_flowable_mappings = add_conversion_to_mapping(lciafmt_w_context_flowable_mappings)
    
    # Merge LCIA with Flowlist
    lcia_mappings = add_uuid_to_mapping(lciafmt_w_context_flowable_mappings)
   
    # Sort to maintain mapping file consistency
    lcia_mappings.sort_values(by=['SourceFlowName','SourceFlowContext'],
                              inplace=True, ignore_index=True)

    # Write them to a csv
    lcia_mappings.to_csv(flowmappingpath / f'{lcia_name}.csv', index=False)
