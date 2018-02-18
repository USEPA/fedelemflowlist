#Generate UUIDs for flows
#Uses UUID3 function from UUID package to generate IDs from strings

import uuid

def c(flowable, context, unit):
    flow = flowable + context + unit
    flowid = str(uuid.uuid3(uuid.NAMESPACE_OID,flow))
    return flowid

