"""Writes preferred flows to a JSON-LD archive in the output folder."""
import fedelemflowlist
from fedelemflowlist.globals import outputpath, flow_list_specs

if __name__ == '__main__':
    preferred_flows = fedelemflowlist.get_flows(preferred_only=True)
    ver = flow_list_specs['list_version']
    fedelemflowlist.write_jsonld(preferred_flows, outputpath /
                                 f"FedElemFlowList_{ver}_preferred.zip")
