#Adapted from https://github.com/USEPA/IO-Model-Builder/blob/master/iomb/olca/__init__.py

#Not fully functional yet this is just a planned approach for writing the json-ld

import json
import logging as log
import zipfile as zipf
import pandas as pd

#import list here from python pickle into pandas dataframe
elemflowlist = pd.read_pickle('./output/ElementaryFlowList')
#compartments = pd.read_pickle('./output/Compartments')

#merge with list

zip_file = './output/testflowlistjson-ld.zip'

pack = zipf.ZipFile(zip_file, mode='a', compression=zipf.ZIP_DEFLATED)

#loop through rows, writing each elementary flow to the pack
for index, row in elemflowlist.iterrows():
    write_elemetary_flows(row,pack)
pack.close()


def write_elemetary_flows(flow: pd.Series, pack: zipf.ZipFile):
    unit = flow['unit']
    if unit is None:
        log.error('unknown unit %s in flow %s')
    f = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Flow",
        "@id": flow['uuid'],
        "name": flow['flowable'],
        #"cas": flow['cas'],
        "flowType": "ELEMENTARY_FLOW",
        "flowProperties": [{
            "@type": "FlowPropertyFactor",
            "referenceFlowProperty": True,
            "conversionFactor": 1.0,
            "flowProperty": {
                "@type": "FlowProperty",
                "name": "",
                "@id": ""}
            }]}
    compartment = flow['context']
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