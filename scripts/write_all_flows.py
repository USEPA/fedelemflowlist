"""Writes preferred flows to a JSON-LD archive in the output folder."""
import pandas as pd

import fedelemflowlist
from fedelemflowlist.globals import outputpath, flow_list_specs


if __name__ == '__main__':

    all_flows = fedelemflowlist.get_flows(preferred_only=False)
    ver = flow_list_specs['list_version']
    file = f"{outputpath}/FedElemFlowList_{ver}"
    fedelemflowlist.write_jsonld(all_flows, f"{file}_all.zip")
    with pd.ExcelWriter(f"{file}_all.xlsx",
                        options={'strings_to_urls':False}) as writer:
        all_flows.to_excel(writer, index=False)
