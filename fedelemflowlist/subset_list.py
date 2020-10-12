# subset_list.py (fedelemflowlist)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions to filter a flow list for subsets
Functions correspond with a subset names stored in the subsets dictionary
"""

import pandas as pd
from fedelemflowlist.globals import inputpath

subsets = {"freshwater_resources":"get_freshwater_resource_flows",
           "water_resources":"get_water_resource_flows",
           "land_use":"get_land_use_flows",
           "mineral_resources":"get_mineral_resource_flows",
           "energy":"get_energy_flows",
           "metal_emissions":"get_metal_emission_flows",
           "HAP":"get_hazardous_air_pollutant_flows"}


def get_subsets() -> list():
    """
    Returns a list of all availabile inventory subsets

    return: list of inventory subsets
    """
    list_of_inventories = list(subsets)
    return list_of_inventories

def get_freshwater_resource_flows(fl):
    """
    Subsets the flow list for all freshwater resource flows,
    excluding resource/air

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Flowable"]=="Water, fresh"]
    flows = flows[flows["Context"].str.startswith("resource")]
    flows = flows[~flows["Context"].str.startswith("resource/air")]

    return flows

def get_water_resource_flows(fl):
    """
    Subsets the flow list for all water resource flows,
    excluding resource/air

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Flowable"].str.startswith("Water")]
    flows = flows[flows["Context"].str.startswith("resource")]
    flows = flows[~flows["Context"].str.startswith("resource/air")]

    return flows


def get_land_use_flows(fl):
    """
    Subsets the flow list for all land use resource flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Class"]=="Land"]
    
    return flows

def get_mineral_resource_flows(fl):
    """
    Subsets the flow list for all mineral resource flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Class"]=="Geological"]
    flows = flows[flows["Context"].str.startswith("resource")]
    flows = flows[~flows["Flowable"].str.contains(" ore")]
    flows = flows[flows["Unit"]=="kg"]
    
    return flows

def get_energy_flows(fl):
    """
    Subsets the flow list for all energy flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Unit"]=="MJ"]
    flows = flows[flows["Context"].str.startswith("resource")]
        
    return flows

def get_metal_emission_flows(fl):
    """
    Subsets the flow list for all emissions of metals

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Context"].str.startswith("emission")]
    #TODO Update with list of metals
        
    return flows

def get_hazardous_air_pollutant_flows(fl):
    """
    Subsets the flow list for all HAP emissions

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Context"].str.startswith("emission/air")]
    haps = pd.read_csv(inputpath+'HAP_flows.csv', usecols=['Flowable'])
    # HAPs sourced from EPA via script write_HAP_flows.py
    # https://www.epa.gov/haps/initial-list-hazardous-air-pollutants-modifications
    flows = flows[flows['Flowable'].isin(haps.Flowable)]
            
    return flows
    