"""
Builds the mapping file for ReCiPe using input flowable and context mappings,
and recipe from the lcia_formatter
Requires lciafmt from lcia_formatter (https://github.com/USEPA/lciaformatter)
BEWARE this will replace the existing mapping file if it exists in /flowmapping
"""

import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath, flowmappingpath

lcia_name = 'ReCiPe2016'

if __name__ == '__main__':
    ## Bring in ReCiPe flowables and contexts from the lcia_formatter
    import lciafmt

    lcia_lciafmt = lciafmt.get_method('ReCiPe 2016')
   
    # Keep only flowable and category
    lcia_lciafmt = lcia_lciafmt[['Flowable', 'Context']]
    lcia_lciafmt = lcia_lciafmt.drop_duplicates()
    len(lcia_lciafmt)

    # Add in context matches. Assume these are in inputfolder with lcia_name+standardname.csv
    def get_manual_mappings(source, ftype):
        """
        Loads a csv mapping file
        :param source: source name
        :param ftype: 'Flowable' or 'Context'
        :return: mapping file
        """
        mappings = pd.read_csv(inputpath + source + ftype + 'Mappings.csv')
        return mappings


    context_mappings = get_manual_mappings(lcia_name, 'Context')
    lciafmt_w_context_mappings = pd.merge(lcia_lciafmt, context_mappings,
                                          left_on='Context',
                                          right_on='SourceFlowContext')
    # Drop duplicate field
    lciafmt_w_context_mappings = lciafmt_w_context_mappings.drop(columns=['Context'])
    len(lciafmt_w_context_mappings)

    # Add in flowable matches. Assume these are in inputfolder with lcia_name+standardname.csv
    flowable_mappings = pd.read_csv(inputpath + lcia_name + 'FlowableMappings.csv')
    len(flowable_mappings)
    # Make all flowables lowercase to resolve case sensitivity issues in ReCiPe
    flowable_mappings['SourceFlowName_low'] = flowable_mappings['SourceFlowName'].str.lower()
    lciafmt_w_context_mappings['Flowable_low']=lciafmt_w_context_mappings['Flowable'].str.lower()
    lciafmt_w_context_flowable_mappings = pd.merge(lciafmt_w_context_mappings,
                                                   flowable_mappings,
                                                   left_on='Flowable_low',
                                                   right_on='SourceFlowName_low')
    # Drop duplicate field
    lciafmt_w_context_flowable_mappings = lciafmt_w_context_flowable_mappings.drop(columns=['Flowable','SourceFlowName_low','Flowable_low'])
    len(lciafmt_w_context_flowable_mappings)

    # Merge LCIA with Flowlist
    # Load full flow list to get all the contexts
    flowlist = fedelemflowlist.get_flows()
    flowlist = flowlist[['Flowable', 'Context', 'Unit', 'Flow UUID', 'Preferred']]
    lcia_mappings = pd.merge(lciafmt_w_context_flowable_mappings, flowlist,
                             left_on=['TargetFlowName', 'TargetFlowContext', 'TargetUnit'],
                             right_on=['Flowable', 'Context', 'Unit'])

    # Clean up the mappings
    lcia_mappings = lcia_mappings.drop(columns=['Flowable', 'Context',
                                                'Unit', 'Note', 'Map method', 'Preferred'])
    lcia_mappings = lcia_mappings.rename(columns={'Flow UUID': 'TargetFlowUUID'})

    # Add LCIA name and missing fields
    lcia_mappings['SourceListName'] = lcia_name
    lcia_mappings['ConversionFactor'] = 1
    lcia_mappings['SourceFlowUUID'] = None
    len(lcia_mappings)

    # pulls all exisiting alternate units for flowables and assigns conversion
    # factor where source unit is an alternate unit
    alt_unit_list = fedelemflowlist.get_alt_conversion()
    lcia_mappings = lcia_mappings.merge(alt_unit_list,how='left',
                                        left_on=['TargetFlowName','SourceUnit', 'TargetUnit'],right_on=['Flowable','AltUnit','Unit'])
    lcia_mappings['ConversionFactor'].update(lcia_mappings['InverseConversionFactor'])
    lcia_mappings = lcia_mappings.drop(columns=['Flowable','Unit',
                                                'AltUnit','AltUnitConversionFactor',
                                                'InverseConversionFactor'])
            
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
    lcia_mappings = lcia_mappings[flowmapping_order]
    # Write them to a csv
    lcia_mappings.to_csv(flowmappingpath + lcia_name + '.csv', index=False)
