"""
Adds conversion factor to mapping files if source unit is an alternate unit
Requires target unit to be the primary unit
Existing conversion factor must be set to 1 to avoid replacing manual conversion factors
Mapping file must already conform to mapping format
"""
import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import flowmappingpath, flowmapping_fields, log

#Add source name here. The .csv mapping file with this name must be in the flowmapping directory
#None can be used to update UUIDs in all mapping files
source = 'ReCiPe2016'

if __name__ == '__main__':
    # Pull in mapping file
    mapping = fedelemflowlist.get_flowmapping(source)
    conversions = fedelemflowlist.get_alt_conversion()
    # merge in conversion factors where source unit = alternate unit
    mapping_w_conversion = pd.merge(mapping, conversions, how='left',
                                  left_on=['TargetFlowName', 'SourceUnit', 'TargetUnit'],
                                  right_on=['Flowable', 'AltUnit', 'Unit'])
    # update conversion factor where current conversion is 1 and the updated conversion exists
    converted1 = mapping_w_conversion['InverseConversionFactor'].notnull() 
    converted2 = mapping_w_conversion['ConversionFactor']==1
    mapping_w_conversion['Convert']=converted1 & converted2
    mapping_w_conversion.loc[(mapping_w_conversion['Convert']==True), 
                             'ConversionFactor']=mapping_w_conversion['InverseConversionFactor']
    converted = mapping_w_conversion['Convert'].sum()
    log.info('added conversion factors for ' + str(converted) + ' flows')
    mapping_w_conversion = mapping_w_conversion.drop(columns=['Flowable','Unit',
                                                         'AltUnit','AltUnitConversionFactor',
                                                         'InverseConversionFactor', 'Convert'])
    flowmapping_order = list(flowmapping_fields.keys())
    mapping_w_conversion =  mapping_w_conversion[flowmapping_order]

    for s in pd.unique( mapping_w_conversion['SourceListName']):
        mapping =  mapping_w_conversion[ mapping_w_conversion['SourceListName'] == s]
        mapping.to_csv(flowmappingpath + s + '.csv', index=False)
