#Produces a list of substances with selected fields from EPA lists of interests; combines and writes to csv
import requests
import pandas as pd
import json

#SRS web service docs at https://cdxnodengn.epa.gov/cdx-srs-rest/
#Base URL for queries
base =  'https://cdxnodengn.epa.gov/cdx-srs-rest/'
substancesbylistname = 'substances/list_acronym/'
baseurl = base+substancesbylistname


#See all lists
#https://cdxnodengn.epa.gov/cdx-srs-rest/reference/substance_lists
#Selected
programlists = ['TRIPS','SPECIATE','EIS','PCS']

# Only keep fields of interest
fieldstokeep = ['epaName', 'systematicName', 'currentCasNumber', 'internalTrackingNumber', 'subsKey',
                'substanceType']
alllistsdf = pd.DataFrame(columns=fieldstokeep)
alllistsdf['program_acronym'] = None
alllistsdf['srs_link'] = None
#also add in a field to identify the df


#SRS  substance URL
srs_url = 'https://iaspub.epa.gov/sor_internet/registry/substreg/searchandretrieve/substancesearch/search.do?details=displayDetails&selectedSubstanceId='

#Loop through, return the list, convert to df, select fields of interest, identify list, write to existing df
for p in programlists:
    url = baseurl+p
    programlistjson = requests.get(url).json()
    programlistdf = pd.DataFrame(programlistjson)
    # See first ten
    programlistdf.head(10)
    programlistdf = programlistdf[fieldstokeep]
    programlistdf['srs_link'] = srs_url + programlistdf['subsKey']
    programlistdf.loc[:,'program_acronym'] = p
    alllistsdf = pd.concat([alllistsdf,programlistdf],ignore_index=True)


#Filter out non-chemicals
alllistsdf = alllistsdf[alllistsdf['substanceType']=='Chemical Substance']

#TO DO
#Check this list against LCI-primer output for these sources (where applicable) to see if this is complete
#Need to determine compartments for flows

#Write final list to pickle and csv
pd.to_pickle(alllistsdf,'./output/SubstancesfromSRSbyProgram')
alllistsdf.to_csv('SubstancesfromSRSbyProgram.csv', index=False)

