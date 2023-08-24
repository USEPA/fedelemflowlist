"""Writes preferred flows to a JSON-LD archive in the output folder."""
import pandas as pd

import fedelemflowlist
from fedelemflowlist.globals import outputpath, flow_list_specs


if __name__ == '__main__':

    all_flows = fedelemflowlist.get_flows(preferred_only=False)
    ver = flow_list_specs['list_version']
    file = outputpath / f"FedElemFlowList_{ver}_all.zip"
    fedelemflowlist.write_jsonld(all_flows, file)
    with pd.ExcelWriter(f"{file}_all.xlsx",
                        # engine='xlsxwriter',
                        # engine_kwargs={
                        #     'options': {'strings_to_urls': False}}
                                       ) as writer:
        all_flows.to_excel(writer, index=False)
