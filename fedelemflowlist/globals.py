#Set global variables for flow list creation
import sys
import os
import json

try: modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError: modulepath = 'fedelemflowlist/'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'
flowmappingpath = modulepath + 'flowmapping/'

import logging as log
log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

try:
    with open(modulepath +"flowlistspecs.json") as cfg:
        flow_list_specs = json.load(cfg)
except FileNotFoundError:
    log.info("Flow list specs not found. Create a flow list specs file.")


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

