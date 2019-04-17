import pandas as pd
from fedelemflowlist.globals import inputpath,outputpath,list_version_no,flow_types,context_fields

compartments_all = pd.read_excel(inputpath+'Compartments.xlsx',sheet_name='Compartments',na_values='N/A') #
compartments_all.head(50)

#Get levels for max number of compartments
max_compartments = len(compartments_all.columns)
compartment_levels = ['c_'+ str(c) for c in range(0,max_compartments)]

#Drop duplicates just as a check
compartments_all = compartments_all.drop_duplicates()

rows_as_list = list()
for index,row in compartments_all.iterrows():
    row_list = row.values
    row_list_na_removed = [x for x in row.values if str(x) != 'nan']
    rows_as_list.append(row_list_na_removed)

#Used this clean list with no NAs, generate UUIDs
from fedelemflowlist.uuid_generators import generate_context_uuid
compartment_uuids = list()
for r in rows_as_list:
    #Pass the uuid function the list as a series of string arguments
    compartment_uuid = generate_context_uuid(*r)
    compartment_uuids.append(compartment_uuid)

rows_as_list_with_nans = rows_as_list

#Add NAs now to end to make lists equal length
for r in rows_as_list_with_nans:
    for i in range(0,max_compartments-len(r)):
        r.append(None)

compartments = pd.DataFrame(rows_as_list_with_nans,columns=compartment_levels)

compartments = compartments.sort_values(by=compartment_levels)

compartments.to_csv('work/compartments_16April.csv',index=False)

#Are they unique
len(compartments)
len(compartments.drop_duplicates())

