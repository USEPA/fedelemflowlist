import fedelemflowlist
from fedelemflowlist.analysis.flow_list_analysis import *
from fedelemflowlist.globals import outputpath

all_flows = fedelemflowlist.get_flows()
#preferred_flows = all_flows[all_flows['Preferred']==True]

all_flows_counts = count_flows_by_class(all_flows)

all_flows_counts.to_csv(outputpath+'all_flows_counts.csv',index=False)