"""
Builds the mapping file for TRACI2.1 using input flowable and context mappings, and TRACI2.1 from the lcia_formatter
Requires lciafmt from lcia_formatter
"""

import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath,flowmappingpath

lcia_name = 'TRACI2.1'

## Bring in TRACI flowables and contexts from the lcia_formatter
import lciafmt
lcai_lciafmt = lciafmt.get_traci()
# Keep only flowable and category
lcai_lciafmt = lcai_lciafmt[['Flow', 'Flow category']]
lcai_lciafmt = lcai_lciafmt.drop_duplicates()
len(lcai_lciafmt)

traci_lciafmt_contexts = pd.Series(pd.unique(lcai_lciafmt['Flow category']))
#export and map these to Fed Commons flow list contexts
#traci_lciafmt_contexts.to_csv('work/TRACI_lciafmt_contexts.csv',index=False)

# Add in context matches
def get_manual_mappings(source,type):
    mappings = pd.read_csv(inputpath+source+type+'Mappings.csv')
    return mappings

context_mappings = get_manual_mappings(lcia_name,type='Context')
lciafmt_w_context_mappings = pd.merge(lcai_lciafmt,context_mappings,left_on='Flow category',right_on='SourceFlowContext')
#Drop duplicate field
lciafmt_w_context_mappings = lciafmt_w_context_mappings.drop(columns=['Flow category'])
len(lciafmt_w_context_mappings)

# Add in flowable matches
flowable_mappings = pd.read_excel(inputpath+lcia_name+'FlowableMappings.xlsx')
flowable_mappings = flowable_mappings[flowable_mappings['SourceFlowName'].notnull()]
len(flowable_mappings)
lciafmt_w_context_flowable_mappings = pd.merge(lciafmt_w_context_mappings,flowable_mappings,left_on='Flow',right_on='SourceFlowName')
# Drop duplicate field
lciafmt_w_context_flowable_mappings = lciafmt_w_context_flowable_mappings.drop(columns='Flow')
len(lciafmt_w_context_flowable_mappings)

#Import the excel file with flowable mappings
#Put excel file in main repository directory for this to work
#traci_mappings = pd.read_excel('TRACImapping.xlsx',sheet_name='TRACImapping')
#len(traci_mappings)
#unique_flows = traci_mappings['SourceFlowName']
#drop non-matches
#traci_mappings = traci_mappings[traci_mappings['SourceFlowName'].notnull()]
#len(traci_mappings)

""" Create standard contexts for TRACI
media_dict = {'Air':'emission/air',
              'Ground':'emission/ground',
              'Water':'emission/water'}

media_cols = list(media_dict.keys())
media_cols.append('Flow Class')
media_cols.append('SourceFlowName')
traci_mappings_flowable_media = traci_mappings[media_cols]

cols_to_keep = ['Class','TargetFlowName','TargetUnit','MatchCondition','SourceFlowName','SourceUnit','Mapper','Verifier']
traci_mappings_w_primary_context = pd.DataFrame(columns=cols_to_keep)
for index, row in traci_mappings.iterrows():
    for x in media_dict.keys():
        if row[x] != 0:
            pattern = media_dict[x]
            traci_mappings_w_primary_context = traci_mappings_w_primary_context.append({'Class':row['Flow Class'],'SourceFlowName':row['SourceFlowName'],'PrimaryContext':pattern},ignore_index=True)
len(traci_mappings_w_primary_context)
"""


# Merge LCIA with Flowlist

#Load full flow list to get all the contexts
flowlist = fedelemflowlist.get_flows()
flowlist = flowlist[['Flowable','Context','Unit','Flow UUID','Preferred']]


"""
class_contexts = flowlist.drop_duplicates(subset=['Class','Context'],keep='first')
class_contexts = class_contexts[['Class','Context']]

import re
primary_w_secondary_contexts = pd.DataFrame(columns=['Class','PrimaryContext','SourceFlowContext'])
for index,row in class_contexts.iterrows():
    for k,v in media_dict.items():
        context = row['Context']
        if re.search(v,context):
            primary_w_secondary_contexts = primary_w_secondary_contexts.append({'Class':row['Class'],'PrimaryContext':v,'Context':context},ignore_index=True)
"""

#Merge lcia with flow list
lcia_mappings = pd.merge(lciafmt_w_context_flowable_mappings,flowlist,left_on=['TargetFlowName','TargetFlowContext','TargetUnit'],right_on=['Flowable','Context','Unit'])

#Clean up the mappings
lcia_mappings = lcia_mappings.drop(columns=['Flowable','Context','Unit','Note','Map method','Preferred'])

lcia_mappings = lcia_mappings.rename(columns={'Flow UUID':'TargetFlowUUID'})

# Add LCIA name
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
lcia_mappings.to_csv(flowmappingpath+lcia_name+'.csv',index=False)


