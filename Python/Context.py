#Read in context csv

import pandas as pd
import iomb.util

# Compartments
contexts = pd.read_csv('./input/Context.csv')

#Generate UUID
contextids = []
for index,row in contexts.iterrows():
        contextid = iomb.util.make_uuid(row['Directionality'],row['Compartment'])
        #flowid = GenerateUUID.fromFlowableContextUnit(row['Directionality'],row['Compartment']))
        #print(flowid)
        contextids.append(contextid)
contexts['uuid'] = contextids


pd.to_pickle(contexts,'./output/Context')