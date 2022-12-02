"""
Combines all mapping files.

To help maintain consistency in future future mappings
output: xlsx in the mapping format.
"""

import fedelemflowlist
from fedelemflowlist.globals import outputpath


if __name__ == '__main__':
    mapping = fedelemflowlist.get_flowmapping()
    # the following line sets "=" so it has a space in front so it displays properly
    mapping.loc[mapping['MatchCondition'] == "=", 'MatchCondition'] = " ="
    mapping.to_excel(outputpath + '/All_Mappings.xlsx', index=False)
    