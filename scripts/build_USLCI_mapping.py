"""
Builds the mapping file for USLCI using input flowable and context mappings, alogn with
manual overrides when this automated approach fails
BEWARE this will replace the existing mapping file if it exists in /flowmapping
"""
import time
import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath,flowmappingpath, log, flowmapping_fields

base_name = 'USLCI_mapping_'
USLCI_ver = '2019Q4'
mapper = 'Ashley Edelen'
verifier = 'Troy Hottle'

if __name__ == '__main__':

    # Add in context matches. Assume these are in inputfolder with lcia_name+standardname.csv
    def get_manual_mappings(source, ftype):
        """
        Loads a csv mapping file
        :param source: source name
        :param ftype: 'Flowable' or 'Context'
        :return: mapping file
        """
        mappings = pd.read_csv(inputpath + base_name + ftype + '.csv')
        return mappings


    flowable_mappings = get_manual_mappings(base_name, 'flowables')
    context_mappings = get_manual_mappings(base_name, 'contexts')

    # Load full flow list to get all the contexts
    flowlist = fedelemflowlist.get_flows()
    flowlist_short = flowlist[['Flowable','Context','Flow UUID']]
    fl_mapping = pd.merge(flowable_mappings,
                                          flowlist_short,
                                          left_on=['TargetFlowName'],
                                          right_on=['Flowable'])

    len_flowable_matches = len(fl_mapping)
    log.info("Matches of USLCI flowables to flowlist flows: " + str(len_flowable_matches))
    fl_mapping = pd.merge(context_mappings,
                          fl_mapping,
                          left_on=['TargetFlowContext'],
                          right_on=['Context'])
    fl_mapping = fl_mapping.drop(columns=['Flowable', 'Context'])
    len_matches = len(fl_mapping)
    log.info("Matches of USLCI flowables and contexts to flowlist flows: " + str(len_matches))

    manual_overrides = get_manual_mappings(base_name, 'manual_overrides')
    fl_corresponding = flowlist_short[(flowlist_short['Context'].isin(manual_overrides['TargetFlowContext'])
                                             & flowlist_short['Flowable'].isin(manual_overrides['Target Name']))]
    log.info("Found " + str(len(fl_corresponding)) + " flowlist flows in manual overrides.")
    fl_mapping = fl_mapping[~fl_mapping['Flow UUID'].isin(fl_corresponding['Flow UUID'])]
    len_removed = len_matches - len(fl_mapping)
    log.info("Removed " + str(len_removed) + " records from mapping from manual overrides.")
    log.info("Mapping is now " + str(len(fl_mapping)) + " records.")
    #Bring in UUIDs for source flows
    src_uuids =  get_manual_mappings(base_name, 'UUIDs')
    #Join in with mapping
    fl_mapping = pd.merge(fl_mapping,src_uuids,on=['SourceFlowName','SourceFlowContext'])
    log.info("Add in source flow UUIDs.")
    log.info("Mapping is now " + str(len(fl_mapping)) + " records.")

    fl_mapping = fl_mapping.drop_duplicates()
    log.info("Droping duplicates.")
    log.info("Mapping is now " + str(len(fl_mapping)) + " records.")

    #Rename fields
    fl_mapping = fl_mapping.rename(columns={'Flow UUID':'TargetFlowUUID'})

    #If conversion factor is missing, assume 1
    fl_mapping.loc[fl_mapping['ConversionFactor'].isnull(),'ConversionFactor'] = 1

    #Add in missing fields
    fl_mapping['SourceListName'] = 'USLCIv' + USLCI_ver
    fl_mapping['Mapper'] = mapper
    fl_mapping['Verifier'] = verifier
    fl_mapping['LastUpdated'] = time.ctime()

    #Reorder
    fl_mapping = fl_mapping[flowmapping_fields.keys()]

    # Write them to a csv
    fl_mapping.to_csv(flowmappingpath + 'USLCI' + USLCI_ver + '.csv', index=False)
