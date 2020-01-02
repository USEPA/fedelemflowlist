"""
Uses fedelemflowlist analysis functions to perform and export basic analysis
"""
import fedelemflowlist
from fedelemflowlist.analysis.flow_list_analysis import count_flows_by_class,\
    count_flowables_by_class, list_contexts
from fedelemflowlist.globals import outputpath

if __name__ == '__main__':
    flowlist = fedelemflowlist.get_flows()
    preferred_flows = flowlist[flowlist['Preferred'] == 1]

    all_flows_counts = count_flows_by_class(flowlist)
    all_flows_counts.to_csv(outputpath + 'all_flows_counts.csv', index=False)

    flowable_counts = count_flowables_by_class(flowlist)
    flowable_counts.to_csv(outputpath + 'flowable_counts.csv', index=False)

    contexts = list_contexts(flowlist)
    contexts.to_csv(outputpath + 'all_contexts.csv', index=False)

    preferred_contexts = list_contexts(preferred_flows)
    preferred_contexts.to_csv(outputpath + 'preferred_contexts.csv', index=False)
