# Set global variables for flow list creation
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
flow_list_fields = {'Flowable':[{'dtype':'str'},{'required':True}],
                    'CAS No':[{'dtype':'str'},{'required':False}],
                    'Formula':[{'dtype':'str'},{'required':False}],
                    'Synonyms':[{'dtype':'str'},{'required':False}],
                    'Unit':[{'dtype':'str'},{'required':True}],
                    'Class':[{'dtype':'str'},{'required':True}],
                    'External Reference':[{'dtype':'str'},{'required':False}],
                    'Preferred':[{'dtype':'int'},{'required':False}],
                    'Context':[{'dtype':'str'},{'required':True}],
                    'Flow UUID':[{'dtype':'str'},{'required':True}],
                    'AltUnit':[{'dtype':'str'},{'required':False}],
                    'AltUnitConversionFactor':[{'dtype':'float'},{'required':False}]
                    }
flowmapping_fields = ['SourceListName',
                     'SourceFlowName',
                     'SourceFlowUUID',
                     'SourceFlowContext',
                     'SourceUnit',
                     'MatchCondition',
                     'ConversionFactor',
                     'TargetFlowName',
                     'TargetFlowUUID',
                     'TargetFlowContext',
                     'TargetUnit',
                     'Mapper',
                     'Verifier',
                     'LastUpdated']

log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

try:
    with open(modulepath + "flowlistspecs.json") as cfg:
        flow_list_specs = json.load(cfg)
except FileNotFoundError:
    log.info("Flow list specs not found. Create a flow list specs file.")


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
