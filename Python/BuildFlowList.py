#Assemble pieces to generate the elementary flow list

import pandas as pd
import iomb.util
#import GenerateUUID  ## Alternative to dependency on IOMB

#Import by flow type
#chemicals = pd.read_csv('Data/Chemicals.csv')
##minerals = pd.read_csv('Data/Minerals.csv')
#flows = pd.concat([chemicals,minerals])

#Temp just to demo UUID creation
flows = {'flowable':['Carbon dioxide','Bauxite'],'context':['air','ground'], 'unit':['kg','kg']}
flows = pd.DataFrame(flows)

#Add blank field for uuid
flows['uuid'] = None

#Loop through flows generating UUID for each
flowids = []
for index,row in flows.iterrows():
        flowid = iomb.util.make_uuid(row['flowable'], row['context'], row['unit'])
        #flowid = GenerateUUID.fromFlowableContextUnit(row['flowable'], row['context'], row['unit'])
        print(flowid)
        flowids.append(flowid)
flows['uuid'] = flowids


#TO DOs
#Implement standaridize list fields


