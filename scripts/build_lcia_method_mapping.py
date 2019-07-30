"""
Builds the mapping file for TRACI2.1 using input flowable and context mappings, and TRACI2.1 from the lcia_formatter
Requires lciafmt from lcia_formatter (https://github.com/USEPA/lciaformatter)
BEWARE this will replace the existing mapping file if it exists in /flowmapping
"""

import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath,flowmappingpath

lcia_name = 'TRACI2.1'


if __name__ == '__main__':
    ## Bring in TRACI flowables and contexts from the lcia_formatter
    import lciafmt
    lcia_lciafmt = lciafmt.get_method('Traci 2.1')
    # Keep only flowable and category
    lcia_lciafmt = lcia_lciafmt[['Flow', 'Flow category']]
    lcia_lciafmt = lcia_lciafmt.drop_duplicates()
    len(lcia_lciafmt)

    traci_lciafmt_contexts = pd.Series(pd.unique(lcia_lciafmt['Flow category']))
    #export and map these to Fed Commons flow list contexts
    #traci_lciafmt_contexts.to_csv('work/TRACI_lciafmt_contexts.csv',index=False)

    # Add in context matches. Assume these are in inputfolder with lcia_name+standardname.csv
    def get_manual_mappings(source,type):
        mappings = pd.read_csv(inputpath+source+type+'Mappings.csv')
        return mappings

    context_mappings = get_manual_mappings(lcia_name,type='Context')
    lciafmt_w_context_mappings = pd.merge(lcia_lciafmt, context_mappings, left_on='Flow category', right_on='SourceFlowContext')
    #Drop duplicate field
    lciafmt_w_context_mappings = lciafmt_w_context_mappings.drop(columns=['Flow category'])
    len(lciafmt_w_context_mappings)

    # Add in flowable matches. Assume these are in inputfolder with lcia_name+standardname.csv
    flowable_mappings = pd.read_excel(inputpath+lcia_name+'FlowableMappings.xlsx')
    flowable_mappings = flowable_mappings[flowable_mappings['SourceFlowName'].notnull()]
    len(flowable_mappings)
    lciafmt_w_context_flowable_mappings = pd.merge(lciafmt_w_context_mappings,flowable_mappings,left_on='Flow',right_on='SourceFlowName')
    # Drop duplicate field
    lciafmt_w_context_flowable_mappings = lciafmt_w_context_flowable_mappings.drop(columns='Flow')
    len(lciafmt_w_context_flowable_mappings)

    # Merge LCIA with Flowlist
    #Load full flow list to get all the contexts
    flowlist = fedelemflowlist.get_flows()
    flowlist = flowlist[['Flowable','Context','Unit','Flow UUID','Preferred']]
    lcia_mappings = pd.merge(lciafmt_w_context_flowable_mappings,flowlist,left_on=['TargetFlowName','TargetFlowContext','TargetUnit'],right_on=['Flowable','Context','Unit'])

    #Clean up the mappings
    lcia_mappings = lcia_mappings.drop(columns=['Flowable','Context','Unit','Note','Map method','Preferred'])
    lcia_mappings = lcia_mappings.rename(columns={'Flow UUID':'TargetFlowUUID'})

    # Add LCIA name and missing fields
    lcia_mappings['SourceListName'] = lcia_name
    lcia_mappings['ConversionFactor'] = 1
    lcia_mappings['SourceFlowUUID'] = None
    len(lcia_mappings)

    #Reorder the mappings
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
    lcia_mappings =lcia_mappings[flowmapping_order]
    #Write them to a csv
    lcia_mappings.to_csv(flowmappingpath+lcia_name+'.csv',index=False)


