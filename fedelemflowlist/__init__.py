# __init__.py (fedelemflowlist)
# !/usr/bin/env python3
# coding=utf-8
"""fedelemflowlist

Allows retrieval of the Federal LCA Commons flow list and mapping files
in standard pandas dataframe formats, defined within format specs
"""

from pathlib import Path
import pandas as pd
from fedelemflowlist.flowlist import read_in_flowclass_file
from fedelemflowlist.globals import flowmappingpath, flow_list_specs,\
    log, load_flowlist
import fedelemflowlist.jsonld as jsonld
from fedelemflowlist.subset_list import subsets
import fedelemflowlist.subset_list as subset_list

def get_flows(preferred_only=None, subset=None, download_if_missing=True):
    """Gets a flow list in a standard format

    Returns the full master flow list unless preferred flows is lists
    :param preferred_only: Boolean for whether preferred flows are desired or not
    :param subset: str, a possible subset of flows
    :param download_if_missing: bool, False to force local generation,
        True to download from remote if not found locally
    :return: standard Flow List dataframe
    """
    flows = load_flowlist(download_if_missing=download_if_missing)
    if preferred_only:
        flows = flows[flows['Preferred'] == 1]
    if subset is not None:
        try:
            flows = getattr(subset_list,subsets[subset])(flows)
        except KeyError:
            log.error(f'Subset {subset} not found.')
            flows = None
    return flows


def get_flowmapping(source=None):
    """Gets a flow mapping in standard format

    Looks for a dataframe of the mapping file specific to the source
    If a source list is provided, it returns only the desired mappings
    Returns an error if specified source does not equal the source name
    :param source: Name of source list in
    :return: standard Flow Mapping dataframe
    """
    flowmappings = pd.DataFrame()
    if source is not None:
        if isinstance(source, 'str'):
            source = [source]
        for f in source:
            mapping_file = flowmappingpath / f'{f}.csv'
            try:
                flowmapping = pd.read_csv(mapping_file, header=0)
                flowmappings = pd.concat([flowmappings, flowmapping])
            except FileNotFoundError:
                log.warn(f'No mapping file found for {f}')
    else:
        for name in flowmappingpath.iterdir():
            if name.suffix == '.csv':
                flowmapping = pd.read_csv(flowmappingpath / name, header=0)
                flowmappings = pd.concat([flowmappings, flowmapping])
    return flowmappings


def write_jsonld(flows, path: Path, mappings=None):
    """ Writes a standard openLCA JSON-LD zip archive with elementary flows and optionally
     flowmappings

    :param flows: standard pd Flow List dataframe, generally from get_flows()
    :param path: path and filename with .zip extention, e.g. 'c:users/mai/fedcommonsflows.zip'
    :param mappings: standard pd Flow Mapping dataframe , generally from get_flowmapping()
    :return: writes out .zip file
    """
    writer = jsonld.Writer(flow_list=flows, flow_mapping=mappings)
    writer.write_to(path)

def get_alt_conversion():
    """returns a dataframe of all flowables with altunits and alt conversion factors
    sourced direclty from input files and so can reference multiple alt units per flowable"""
    altflowlist = pd.DataFrame()
    for t in flow_list_specs["flow_classes"]:
        try:
            altunits_for_class = read_in_flowclass_file(t, 'FlowableAltUnits')
            altunits_for_class = altunits_for_class.drop_duplicates()
            altflowlist = pd.concat([altflowlist,altunits_for_class],ignore_index=True)
        except FileNotFoundError:
            altunits_for_class = None # Do nothing
    altflowlist = (altflowlist
                   .drop(columns=['External Reference'])
                   .rename(columns={'Conversion Factor': 'AltUnitConversionFactor',
                                    'Alternate Unit': 'AltUnit',
                                    'Reference Unit': 'Unit'})
                   )
    # generate InverseConversionFactor for converting from alt unit to primary unit
    altflowlist['InverseConversionFactor']=1/altflowlist['AltUnitConversionFactor']
    # round to 6 decimals
    altflowlist = altflowlist.round({'InverseConversionFactor':6})
    return altflowlist
