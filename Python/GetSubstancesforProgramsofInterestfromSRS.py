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
#also add in a field to identify the df

#Loop through, return the list, convert to df, select fields of interest, identify list, write to existing df
for p in programlists:
    url = baseurl+p
    programlistjson = requests.get(url).json()
    programlistdf = pd.DataFrame(programlistjson)
    # See first ten
    #programlistdf.head(10)
    programlistdf = programlistdf[fieldstokeep]
    programlistdf.loc[:,'program_acronym'] = p
    alllistsdf = pd.concat([alllistsdf,programlistdf],ignore_index=True)


#Write final list to csv
alllistsdf.to_csv('SubstancesfromSRSbyProgram.csv', index=False)

