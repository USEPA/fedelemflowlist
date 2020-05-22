"""Writes preferred flows to a JSON-LD archive in the output folder."""
import fedelemflowlist
from fedelemflowlist.globals import outputpath, flow_list_specs

if __name__ == '__main__':
    preferred_flows = fedelemflowlist.get_flows(preferred_only=True)
    fedelemflowlist.write_jsonld(preferred_flows,
                                 outputpath + 'FedElemFlowList_' +
                                 flow_list_specs['list_version'] + '_preferred.zip')
