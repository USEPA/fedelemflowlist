import pandas as pd
import fedelemflowlist as fl
from fedelemflowlist.globals import outputpath

CDDmapping = fl.get_flowmapping('CDDLCI')

CDDUUIDs = list(pd.unique(CDDmapping['TargetFlowUUID']))

all_flows = fl.get_flows()
CDDflows = all_flows[all_flows['Flow UUID'].isin(CDDUUIDs)]

len(CDDflows)

fl.write_jsonld(CDDflows,outputpath+'CDDflowsandmappings.zip',CDDmapping)