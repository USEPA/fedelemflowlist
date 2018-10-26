#Generate UUIDs for flows
#Uses UUID3 function from UUID package to generate IDs from strings

import uuid

def generate_flow_uuid(flowable,directionality,compartment,unit):
    flow = flowable + directionality + compartment + unit
    flowid = str(uuid.uuid3(uuid.NAMESPACE_OID,flow))
    return flowid

def generate_context_uuid(flow_class,directionality,compartment):
    context = flow_class + directionality + compartment
    contextid = str(uuid.uuid3(uuid.NAMESPACE_OID,context))
    return contextid


