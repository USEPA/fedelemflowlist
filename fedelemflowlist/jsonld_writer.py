#Adapted from https://github.com/USEPA/IO-Model-Builder/blob/master/iomb/olca/__init__.py

import json
import logging as log
import zipfile as zipf
import pandas as pd
import time

from fedelemflowlist.globals import outputpath,list_version_no

def write_flow_list_to_jsonld(elemflowlist):
    zip_file = outputpath + 'Flows_' + list_version_no + '_json-ld.zip'
    pack = zipf.ZipFile(zip_file, mode='a', compression=zipf.ZIP_DEFLATED)
    #loop through rows, writing each elementary flow to the pack
    for index, row in elemflowlist.iterrows():
        write_elemetary_flows(row,pack)
    pack.close()

def write_elemetary_flows(flow: pd.Series, pack: zipf.ZipFile):
    unit = flow['Unit']
    if unit is None:
        log.error('unknown unit %s in flow %s')
    f = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Flow",
        "@id": flow['Flow UUID'],
        "name": flow['Flowable'],
        "cas": flow['CAS No'],
        "version": list_version_no,
        #Need to  determine time
        #"lastChange": time.time()
        #Category
        #"category:":{
        #"categoryPath":["Elementary flows",flow['Directionality'],flow['Compartment']]
        #},
        "flowType": "ELEMENTARY_FLOW",
        "flowProperties": [{
            "@type": "FlowPropertyFactor",
            "referenceFlowProperty": True,
            "conversionFactor": 1.0,
            "flowProperty": {
                "@type": "FlowProperty",
                "name": flow['Flow quality'],
                "@id": flow["Quality UUID"]}
            }]}
    #compartment = flow['Context UUID']
    #look up compartment id
    #compartmentid = compartments[compartments['name'] == compartment, uuid]
    #if compartment is not None:
    #    f["category"] = {"@type": "Category", "@id":compartmentid }
    dump(f, 'flows', pack)

def dump(obj: dict, folder: str, pack: zipf.ZipFile):
    """ dump writes the given dictionary to the zip-file under the given folder.
    """
    uid = obj.get('@id')
    if uid is None or uid == '':
        log.error('No @id for object %s in %s', obj, folder)
        return
    path = '%s/%s.json' % (folder, obj['@id'])
    s = json.dumps(obj)
    pack.writestr(path, s)