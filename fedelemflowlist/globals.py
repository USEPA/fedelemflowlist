#Set global variables for flow list creation
import sys
import os

try: modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError: modulepath = 'fedelemflowlist/'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'
flowmappingpath = modulepath + 'flowmapping/'

import logging as log
log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

#list_version_no = '0.1' #Must be numeric
#flow_types = {'Energy':'resource', 'Fuel':'resource', 'Land':'resource', 'Chemicals':'emission', 'Groups':'emission'}

list_version_no = '0.3e' #Must be numeric
#flow_classes = ['Biological','Chemicals','Energy', 'Fuel', 'Geological','Groups','Land','Water','Other']
flow_classes = ['Chemicals']

def convert_to_lower(x):
    x = str(x)
    x = str.lower(x)
    return x

def as_path(*args: str) -> str:
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).strip().lower())
    return "/".join(strings)

