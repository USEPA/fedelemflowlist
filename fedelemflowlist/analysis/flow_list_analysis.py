"""
Functions to perform analysis of a flow list
"""
import pandas as pd


def count_flows_by_class(flowlist):
    """Counts all and preferred flows by class

    :param flowlist: A FlowList in standard format
    :return: pandas df with 'Class','No. of Flows','No. of Preferred Flows'
    """
    fl_all = flowlist.groupby(['Class'])['Flow UUID'].count().reset_index()
    fl_pref = flowlist.groupby(['Class'])['Preferred'].sum().reset_index()
    fl_combined = pd.merge(fl_all, fl_pref, on=['Class'])
    fl_combined = fl_combined.rename(columns={'Flow UUID': 'No. of Flows',
                                              'Preferred': 'No. of Preferred Flows'})
    total_flows = fl_combined['No. of Flows'].sum()
    fl_combined['Percent of Flows'] = fl_combined['No. of Flows'].\
        apply(lambda x: str((x / total_flows) * 100) + '%')
    total_row = {'Class': 'TOTAL', 'No. of Flows': total_flows,
                 'No. of Preferred Flows': fl_combined['No. of Preferred Flows'].sum()}
    fl_combined = fl_combined.append(total_row, ignore_index=True)
    return fl_combined


def list_contexts(flowlist):
    """Displays list of contexts along with 1 if the context is present for that flowclass.
    Can send a preferred list or
        :param flowlist: A FlowList in standard format
    :return: pandas df with 'Context',plus columns for all flow classes
    """
    contexts = flowlist[['Context', 'Class']]
    contexts = contexts.drop_duplicates()
    contexts['Num'] = 1
    context_counts = contexts.pivot_table(index='Context', columns='Class',
                                          values='Num', aggfunc='count',
                                          fill_value='0').reset_index()
    return context_counts


def count_flowables_by_class(flowlist):
    """
    Counts flowables by class
    :param flowlist: A FlowList in standard format
    :return: pandas df with 'Class' and counts of unique flowables
    """
    flowables_by_class = flowlist[['Class', 'Flowable']]
    flowables_by_class = flowables_by_class.drop_duplicates()
    flowables_by_class_count = flowables_by_class.groupby('Class')['Flowable'].count().reset_index()
    total = flowables_by_class_count['Flowable'].sum()
    flowables_by_class_count['Percent'] = flowables_by_class_count['Flowable'].apply(
        lambda x: str((x / total) * 100) + '%')
    total_row = {'Class': 'TOTAL', 'Flowable': total}
    flowables_by_class_count = flowables_by_class_count.append(total_row, ignore_index=True)
    return flowables_by_class_count
