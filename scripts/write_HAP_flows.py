"""Generates a list of HAP emissions from EPA to store locally"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath

url = 'https://www.epa.gov/haps/initial-list-hazardous-air-pollutants-modifications'


def extract_table():
    resp=requests.get(url)
    if resp.status_code==200: 
        df = pd.DataFrame(columns=['CAS No','HAP'])
        soup=BeautifulSoup(resp.text,'html.parser')     
        table=soup.find("table")
        table_rows = table.findAll('tr')
        for row in table_rows:
            td = row.findAll('td')
            data = [i.text for i in td]
            if len(data) == 2:
                df.loc[len(df)] = data
        return df
    else: 
        print("Error") 

def modify_CAS(df):
    "Returns CAS with dash"
    right = df['CAS No'].str[-1:]
    mid = df['CAS No'].str[-3:-1]
    left = df['CAS No'].str[:-3]
    df['CAS No'] = left +'-'+mid+'-'+right
    return df

def modify_list(df):
    modifications = ['Caprolactam (See Modification)',
                     'Hydrogen sulfide (See Modification)',
                     'Methyl ethyl ketone (2-Butanone) (See Modification)',
                     ]
    df=df[~df['HAP'].isin(modifications)]
    return df
    
if __name__ == '__main__':
    
    df = extract_table()
    df = modify_list(df)
    df = modify_CAS(df)
    fl = fedelemflowlist.get_flows()
    fl = fl[fl['Context']=='emission/air']
    fl.drop(columns=['Context','Flow UUID','AltUnit','AltUnitConversionFactor'],
            inplace=True)

    merged_df = df.merge(fl,how='left',on='CAS No')
    merged_df.loc[merged_df['CAS No']=='--0','CAS No'] = None
    
    # for flows unmatched by CAS, remove extraneous data within flow name
    # and match on flowable (case insensitive)
    no_match = merged_df.loc[merged_df['Flowable'].isnull()]
    no_match[['f1','f2']]=no_match['HAP'].str.split("\(",expand=True)
    no_match['f3']=no_match['f1'].str.strip().str[-1:].str.isnumeric()
    no_match.loc[no_match['f3'], 'f1'] = no_match['f1'].str[:-2]
    no_match['HAP2']=no_match['f1'].str.strip()
    no_match.drop(columns=['f1','f2','f3'],inplace=True)
    
    no_match['HAP_lower']=no_match['HAP2'].str.lower()
    name_match = no_match[['HAP','HAP_lower']]
    fl['Flowable_lower']=fl['Flowable'].str.lower()
    name_match = name_match.merge(fl,how='left',left_on='HAP_lower',
                              right_on='Flowable_lower')
    name_match.drop(columns=['HAP_lower','Flowable_lower'], inplace=True)
    
    # update the merged dataframe with name matches
    merged_df.dropna(subset=['Flowable'], inplace=True)
    merged_df = pd.concat([merged_df,name_match],ignore_index=True)
    
    merged_df.to_csv(inputpath+'HAP_flows.csv', index=False)