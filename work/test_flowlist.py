import fedelemflowlist
all_flows = fedelemflowlist.get_flowlist(version='0.3')


import fedelemflowlist.jsonld as jsonld
writer = jsonld.Writer(flow_list=all_flows)
writer.write_to('work/FedElemFlowList_0.3_jsonld.zip')

