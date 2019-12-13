"""
For mapping data were originally developed in Excel where flowables. This was developed specifically
for the USLCI mapping. This script extracts those data and writes them to csv files.
WARNING: This will replace the existing input files
"""

import pandas as pd
from fedelemflowlist.globals import flowmappingpath, flow_list_specs

# Set directory where excel file resides and where we will write out to
excel_dir = flowmappingpath
file_name = 'USLCI_mapping'

#A dictionary of names of data types and sheet names from the Excel file to extract them from
name_sheet_dict = {'flowables': 'Flow mappings',
                   'contexts': 'Context mappings',
                   'UUIDs':'Flow UUIDs',
                   'manual_overrides': 'Manual mapping overrides'}

if __name__ == '__main__':

        for n,v in name_sheet_dict.items():
            df = pd.read_excel(excel_dir + file_name + '.xlsx',
                                            sheet_name=v, header=0, na_values="#N/A")
            df = df.dropna(axis=0, how='all')
            df.to_csv(flowmappingpath + file_name + '_' + n + '.csv', index=False)


