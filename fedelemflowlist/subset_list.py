# subset_list.py (fedelemflowlist)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions to filter a flow list for subsets
Functions correspond with a subset names stored in the subsets dictionary
"""

subsets = {"freshwater_resources":"get_freshwater_resource_flows",
           "land_use":"get_land_use_flows"}


def get_freshwater_resource_flows(fl):
    """
    Subsets the flow list for all freshwater resource flows

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Flowable"]=="Water, fresh"]
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