#

import fedelemflowlist

flows = fedelemflowlist.get_flows()
len(flows)
#C:\Users\wesle\AppData\Local\Programs\Python\Python37\lib\code.py:74: DtypeWarning: Columns (3,5) have mixed types. Specify dtype option on import or set low_memory=False.
#  self.runcode(code)
#304161

flows = fedelemflowlist.get_flows(preferred_only=True)
len(flows)
#6478

mapping = fedelemflowlist.get_flowmapping(source=['TRI'])


fedelemflowlist.write_jsonld(flows,'work/preferredflows-jsonld-22May.zip')

