import pandas as pd
import os

try: modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError: modulepath = 'fedelemflowlist/'

output_dir = modulepath + 'output/'

#Returns the most recent flows list as a dataframe by default
def get_flowlist(version=None,format='df'):
    if version is None:
        list = identify_most_recent_list()
    else:
        list = 'FedElemFlowList_' + version
    #Get it as a dataframe
    list_file = output_dir + list + '.csv'
    if format == 'df':
        flowlist = pd.read_csv(list_file,header=0)
    return flowlist

def list_flowlists():
    files = os.listdir(output_dir)
    flowslists = []
    for name in files:
        if name.endswith(".csv"):
            n = name.strip('.csv')
            flowslists.append(n)
    return flowslists

def identify_most_recent_list(list_type='any'):
   flowlists =  list_flowlists()

   #temp
   return str(flowlists[0])



