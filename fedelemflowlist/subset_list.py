# subset_list.py (fedelemflowlist)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions to filter a flow list for subsets
Functions correspond with a subset names stored in the subsets dictionary
"""

subsets = {"freshwater_resources":"get_freshwater_resource_flows"}


def get_freshwater_resource_flows(fl):
    """

    :param fl: df in standard flowlist format
    :return: df in standard flowlist format
    """
    flows = fl[fl["Flowable"]=="Water, fresh"]
    #! needs to be subset for resource flows
    return flows
