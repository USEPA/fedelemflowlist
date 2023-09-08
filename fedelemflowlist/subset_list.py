# subset_list.py (fedelemflowlist)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions to filter a flow list for subsets
Functions correspond with a subset names stored in the subsets dictionary
"""

import pandas as pd
import fedelemflowlist
from fedelemflowlist.globals import inputpath

subsets = {"freshwater_resources":"get_freshwater_resource_flows",
           "water_resources":"get_water_resource_flows",
           "land_use":"get_land_use_flows",
           "USGS_mineral_resources":"get_USGS_mineral_resource_flows",
           "energy":"get_energy_flows",
           "renewable_energy":"get_renewable_energy_flows",
           "nonrenewable_energy":"get_nonrenewable_energy_flows",  
           "USDA_CUS_pesticides":"get_USDA_CUS_pesticides",
           "HAP":"get_hazardous_air_pollutant_flows"}

inventory_unit = {"freshwater_resources":"kg",
                  "water_resources":"kg",
                  "land_use":"m2*a",
                  "USGS_mineral_resources":"kg",
                  "energy":"MJ",
                  "renewable_energy":"MJ",
                  "nonrenewable_energy":"MJ",
                  "USDA_CUS_pesticides":"kg",
                  "HAP":"kg"}

def get_subsets() -> list():
    """
    Returns a list of all availabile inventory subsets

    return: list of inventory subsets
    """
    list_of_inventories = list(subsets)
    return list_of_inventories

def get_inventory_unit(subset):
    """
    Returns the inventory unit for the selected subset
    :param subset: dictionary key
    return: (str) unit for inventory method.
    """
    unit = inventory_unit[subset]
    return unit    
    
    
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


def get_USGS_mineral_resource_flows(fl):
    """
    Subsets the flow list for all mineral resource flows from USGS MCS

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    usgs = fedelemflowlist.get_flowmapping('USGS_MCS')
    usgs = list(usgs['TargetFlowName'].drop_duplicates())
    flows = fl[fl["Flowable"].isin(usgs)]
    flows = flows[flows["Context"].str.startswith("resource")]
    
    return flows

def get_energy_flows(fl):
    """
    Subsets the flow list for all energy flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    list_of_flows = ['Uranium','Biomass','Hardwood','Softwood','Wood']
    flows = fl[(fl["Unit"]=="MJ") | (fl['Flowable'].isin(list_of_flows))]
    #Peat is captured in USGS_mineral_resource_flows so exclude here
    flows = flows[flows['Flowable']!='Peat']
    flows = flows[flows["Context"].str.startswith("resource")]
        
    return flows

def get_renewable_energy_flows(fl):
    """
    Subsets the flow list for all renewable energy flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    fl = get_energy_flows(fl) 
    renewables_class = ['Biological','Energy']
    flows = fl[fl["Class"].isin(renewables_class)]
        
    return flows

def get_nonrenewable_energy_flows(fl):
    """
    Subsets the flow list for all nonrenewable energy flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    fl = get_energy_flows(fl) 
    renewables_class = ['Biological','Energy']
    flows = fl[~fl["Class"].isin(renewables_class)]
        
    return flows

def get_hazardous_air_pollutant_flows(fl):
    """
    Subsets the flow list for all HAP emissions based on list of flows from
    EPA.

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Context"].str.startswith("emission/air")]
    haps = pd.read_csv(inputpath / 'HAP_flows.csv', usecols=['Flowable'])
    # HAPs sourced from EPA via script write_HAP_flows.py
    # https://www.epa.gov/haps/initial-list-hazardous-air-pollutants-modifications
    flows = flows[flows['Flowable'].isin(haps.Flowable)]
            
    return flows

def get_USDA_CUS_pesticides(fl):
    """
    Subsets the flow list for all pesticide emissions as identified in the USDA
    Chemical Use Survey.

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    pesticides = fedelemflowlist.get_flowmapping('USDA_CUS')
    pesticides = pesticides[['TargetFlowUUID']].drop_duplicates()
    flows = fl[fl["Flow UUID"].isin(pesticides['TargetFlowUUID'])]
    return flows

    