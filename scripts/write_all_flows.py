"""
Writes preferred flows to a JSON-LD archive in the output folder
"""
import fedelemflowlist
from fedelemflowlist.globals import outputpath,flow_list_specs


if __name__ == '__main__':

    all_flows = fedelemflowlist.get_flows(preferred_only=False)
    fedelemflowlist.write_jsonld(all_flows,outputpath+'FedElemFlowList_'+flow_list_specs['list_version']+'_all.zip')
    all_flows.to_excel(outputpath+'FedElemFlowList_'+flow_list_specs['list_version']+'_all.xlsx',index=False)
