"""Set common variables for use in package"""
import sys
import os
import json
import logging as log

try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'fedelemflowlist/'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'
flowmappingpath = modulepath + 'flowmapping/'

flow_list_fields = {'Flowable': [{'dtype': 'str'}, {'required': True}],
                    'CAS No': [{'dtype': 'str'}, {'required': False}],
                    'Formula': [{'dtype': 'str'}, {'required': False}],
                    'Synonyms': [{'dtype': 'str'}, {'required': False}],
                    'Unit': [{'dtype': 'str'}, {'required': True}],
                    'Class': [{'dtype': 'str'}, {'required': True}],
                    'External Reference': [{'dtype': 'str'}, {'required': False}],
                    'Preferred': [{'dtype': 'int'}, {'required': False}],
                    'Context': [{'dtype': 'str'}, {'required': True}],
                    'Flow UUID': [{'dtype': 'str'}, {'required': True}],
                    'AltUnit': [{'dtype': 'str'}, {'required': False}],
                    'AltUnitConversionFactor': [{'dtype': 'float'}, {'required': False}]
                    }
flowmapping_fields = {'SourceListName': [{'dtype': 'str'}, {'required': True}],
                      'SourceFlowName': [{'dtype': 'str'}, {'required': True}],
                      'SourceFlowUUID': [{'dtype': 'str'}, {'required': False}],
                      'SourceFlowContext': [{'dtype': 'str'}, {'required': True}],
                      'SourceUnit': [{'dtype': 'str'}, {'required': True}],
                      'MatchCondition': [{'dtype': 'str'}, {'required': False}],
                      'ConversionFactor': [{'dtype': 'float'}, {'required': False}],
                      'TargetFlowName': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowUUID': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowContext': [{'dtype': 'str'}, {'required': True}],
                      'TargetUnit': [{'dtype': 'str'}, {'required': True}],
                      'Mapper': [{'dtype': 'str'}, {'required': False}],
                      'Verifier': [{'dtype': 'str'}, {'required': False}],
                      'LastUpdated': [{'dtype': 'str'}, {'required': False}]}

log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

flow_list_specs = {
    "list_version": "1.0.3",
    "flow_classes": ["Biological", "Chemicals", "Energy", "Geological", "Groups", "Land", "Other", "Water"],
    "primary_context_classes": ["Directionality", "Environmental Media"],
    "secondary_context_classes": ["Vertical Strata", "Land Use", "Human-Dominated", "Terrestrial", "Aquatic Feature",
                                  "Indoor", "Population Density", "Release Height"]
}

def convert_to_lower(x):
    """Convert string to lower case

    :param x: string
    :return: string
    """
    x = str(x)
    x = str.lower(x)
    return x


def as_path(*args: str) -> str:
    """Converts strings to lowercase path-like string
    Take variable order of string inputs
    :param args: variable-length of strings
    :return: string
    """
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).strip().lower())
    return "/".join(strings)
