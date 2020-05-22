"""
Flow data were originally developed in Excel.

This script extracts those data and writes them to csv files. WARNING: This will
replace the existing input files The flow class files should match the class
names in the flowlistspecs.
"""

import pandas as pd
from fedelemflowlist.globals import inputpath, flow_list_specs

# Set directory where excel files..can put in same folder as csv input files

excel_dir = inputpath

if __name__ == '__main__':
    # Read in and write out needed sheets from flow class files
    for t in flow_list_specs["flow_classes"]:

        # Handle flowables first
        flowables_for_class = pd.read_excel(excel_dir + t + '.xlsx',
                                            sheet_name='Flowables', header=0)
        # Drop if the line is blank
        flowables_for_class = flowables_for_class.dropna(axis=0, how='all')

        flowables_for_class.to_csv(inputpath + t + 'Flowables.csv', index=False)

        class_primary_contexts = pd.read_excel(inputpath + t + '.xlsx',
                                               sheet_name='FlowablePrimaryContexts',
                                               header=0)
        class_primary_contexts = class_primary_contexts.dropna(axis=0, how='all')

        class_primary_contexts.to_csv(inputpath + t + 'FlowablePrimaryContexts.csv', index=False)
        # Try to extract alt unit files
        try:
            altlunits_for_class = pd.read_excel(excel_dir + t + '.xlsx',
                                                sheet_name='FlowableAltUnits', header=0)
            altlunits_for_class = altlunits_for_class.dropna(axis=0, how='all')
            altlunits_for_class.to_csv(inputpath + t + 'FlowableAltUnits.csv', index=False)
        except FileNotFoundError:
            continue

    contexts = pd.read_excel(excel_dir + 'Contexts.xlsx',
                             sheet_name='Contexts', na_values='N/A')  #
    contexts.to_csv(inputpath + 'Contexts.csv', index=False)

    SecondaryContextMembership = pd.read_excel(excel_dir + 'SecondaryContextMembership.xlsx',
                                               sheet_name='SecondaryContextMembership')  #
    SecondaryContextMembership.to_csv(inputpath + 'SecondaryContextMembership.csv', index=False)
