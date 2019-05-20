#Generate UUIDs for flows
#Uses UUID3 function from UUID package to generate IDs from strings

import uuid
from fedelemflowlist.globals import as_path

def generate_flow_uuid(flowable,directionality,compartment,unit):
    flow = flowable + directionality + compartment + unit
    flowid = str(uuid.uuid3(uuid.NAMESPACE_OID,flow))
    return flowid

def generate_context_uuid(*args: str):
    context = as_path(*args)
    contextid = str(uuid.uuid3(uuid.NAMESPACE_OID,context))
    return contextid

def make_uuid(*args: str) -> str:
    path = as_path(*args)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))


