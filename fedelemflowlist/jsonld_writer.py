#Adapted from iomb.olca, currently at https://github.com/USEPA/IO-Model-Builder/blob/master/iomb/olca/__init__.py
#For now this does not pack olca unit groups and flows properties, but just links to the relevant flow properties in the current olca data

import json
import zipfile as zipf
import pandas as pd
import os
import time

from fedelemflowlist.globals import outputpath,list_version_no

#Taken from an exported json-ld file. For the context.json file
context_info = {"@vocab":"http://openlca.org/schema/v1.1/",
                "@base":"http://openlca.org/schema/v1.1/",
                "modelType":{"@type":"@vocab"},
                "flowPropertyType":{"@type":"@vocab"},
                "flowType":{"@type":"@vocab"},
                "distributionType":{"@type":"@vocab"},
                "parameterScope":{"@type":"@vocab"},
                "allocationType":{"@type":"@vocab"},
                "defaultAllocationMethod":{"@type":"@vocab"},
                "allocationMethod":{"@type":"@vocab"},
                "processType":{"@type":"@vocab"},
                "riskLevel":{"@type":"@vocab"}}

#Taken from an exported json-ld file. For the context.json file
elementary_flows_category = {"@context":"http://greendelta.github.io/olca-schema/context.jsonld",
                                 "@type":"Category",
                                 "@id":"f318fa60-bae9-361f-ad5a-5066a0e2a9d1",
                                 "name":"Elementary flows",
                                 "modelType":"FLOW"}

resource_flow_category = {"@context":"http://greendelta.github.io/olca-schema/context.jsonld",
                          "@type":"Category",
                          "@id":"3095c63c-7962-4086-a0d7-df4fd38c2e68",
                          "name":"resource",
                          "category":{"@type":"Category",
                                      "@id":"f318fa60-bae9-361f-ad5a-5066a0e2a9d1",
                                      "name":"Elementary flows"},
                          "modelType":"FLOW"}
emission_flow_category = {"@context":"http://greendelta.github.io/olca-schema/context.jsonld",
                          "@type":"Category",
                          "@id":"c2433915-9ca3-3933-a64d-68d67e3e3281",
                          "name":"emission",
                          "category": {"@type": "Category",
                                       "@id": "f318fa60-bae9-361f-ad5a-5066a0e2a9d1",
                                       "name": "Elementary flows"},
                          "modelType":"FLOW"}

def write_flow_list_to_jsonld(elemflowlist,contexts):
    zip_file = outputpath + 'FedElemFlowList_' + list_version_no + '_json-ld.zip'
    #Need to remove existing file if it exists
    if(os.path.exists(zip_file)):
        os.remove(zip_file)
    pack = zipf.ZipFile(zip_file, mode='a', compression=zipf.ZIP_DEFLATED)
    #loop through rows, writing each elementary flow to the pack
    for index, row in elemflowlist.iterrows():
        write_elemetary_flows(row,pack)
    for index, row in contexts.iterrows():
        write_compartment_categories(row,pack)
    write_directionality_categories(pack)
    contexts_json = json.dumps(context_info)
    pack.writestr('context.json', contexts_json)
    pack.close()

def write_elemetary_flows(flow: pd.Series, pack: zipf.ZipFile):
    unit = flow['Unit']
    if unit is None:
        print('unknown unit %s in flow %s')
    f = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Flow",
        "@id": flow['Flow UUID'],
        "name": flow['Flowable'],
        "cas": flow['CAS No'],
        "formula": flow['Formula'],
        "version": list_version_no,
        #Need to  determine time
        #"lastChange": time.time()
        #Category
        "category:": {"@type":"Category",
                      "@id": flow["Compartment UUID"],
                      "name": flow["Compartment"]},
        "flowType": "ELEMENTARY_FLOW",
        "flowProperties": [{
            "@type": "FlowPropertyFactor",
            "referenceFlowProperty": True,
            "flowProperty": {
                "@type": "FlowProperty",
                "name": flow['Flow quality'],
                "@id": flow["Quality UUID"]},
            "conversionFactor": 1.0
            }]
    }
    dump(f, 'flows', pack)

def write_compartment_categories(category,pack):
    #loop through contexts to create context for compartments
    c = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": "Category",
            "@id": category['Compartment UUID'],
            "name": category["Compartment"],
            "modelType": "FLOW"
        }
    if category["Directionality"]=="resource":
        c["category"] = {
            "@type": "Category",
            "@id": resource_flow_category["@id"],
            "name": resource_flow_category["name"]
        }
    elif category["Directionality"]=="emission":
        c["category"] = {
            "@type": "Category",
            "@id": emission_flow_category["@id"],
            "name": emission_flow_category["name"]
        }
    dump(c,'categories',pack)

def write_directionality_categories(pack):
    dump(resource_flow_category,'categories',pack)
    dump(emission_flow_category,'categories',pack)
    dump(elementary_flows_category,'categories',pack)

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

