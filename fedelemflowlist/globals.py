#Set global variables for flow list creation

inputpath = 'fedelemflowlist/input/'
outputpath = 'fedelemflowlist/output/'
flowmappingpath = 'fedelemflowlist/flowmapping'
context_fields = ['Directionality','Compartment']

list_version_no = '0.1' #Must be numeric

flow_types = {'Energy':'resource', 'Fuel':'resource', 'Land':'resource', 'Chemicals':'emission', 'Groups':'emission'}