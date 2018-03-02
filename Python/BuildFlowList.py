#Assemble pieces to generate the elementary flow list

import pandas as pd
import iomb.util
import GenerateUUID  ## Alternative to dependency on IOMB

#Import by flow type
#Later can loop through by defined type

#chemicals = pd.read_csv('./input/Chemicals.csv',skiprows=1)
land = pd.read_csv('./input/Land_flows.csv',skiprows=1)
##minerals = pd.read_csv('Data/Minerals.csv')
#
energy = pd.read_csv('./input/Energy_flows.csv',skiprows=1)
fuels = pd.read_csv('./input/Fuel_flows.csv',skiprows=1)
flows = pd.concat([land,energy,fuels])

#Temp just to demo UUID creation
#flows = {'Flowable':['Carbon dioxide','Bauxite'],'Flow compartment':['air','ground'], 'Unit':['kg','kg']}
#flows = pd.DataFrame(flows)

#Add blank field for uuid
flows['uuid'] = None

#Loop through flows generating UUID for each
flowids = []
for index,row in flows.iterrows():
        flowid = iomb.util.make_uuid(row['Flowable'],row['Flow directionality'], row['Flow compartment'], row['Unit'])
        #flowid = GenerateUUID.fromFlowableContextUnit(row['flowable'], row['context'], row['unit'])
        print(flowid)
        flowids.append(flowid)
flows['uuid'] = flowids


#TO DOs
#Implement standaridize list fields
#Generate a compartment list and save to pickle

#Save it to csv
flows.to_csv('./output/ElementaryFlows.csv',index=False)

#Save to pickle
pd.to_pickle(flows,'./output/ElementaryFlowList')


