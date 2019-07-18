import pandas as pd

def count_flows_by_class(flowlist):
    """Counts all and preferred flows by class

    :param flowlist: A FlowList in standard format
    :return: pandas df with 'Class','No. of Flows','No. of Preferred Flows'
    """
    fl_all = flowlist.groupby(['Class'])['Flow UUID'].count().reset_index()
    fl_pref = flowlist.groupby(['Class'])['Preferred'].sum().reset_index()
    fl_combined = pd.merge(fl_all,fl_pref,on=['Class'])
    fl_combined = fl_combined.rename(columns={'Flow UUID':'No. of Flows','Preferred':'No. of Preferred Flows'})
    total_row = {'Class':'TOTAL','No. of Flows':fl_combined['No. of Flows'].sum(),'No. of Preferred Flows':fl_combined['No. of Preferred Flows'].sum()}
    fl_combined = fl_combined.append(total_row,ignore_index=True)
    return fl_combined


