"""
Combines all mapping files to help maintain consistency in future future mappings
output: csv in the mapping format
"""

import fedelemflowlist
from fedelemflowlist.globals import outputpath


if __name__ == '__main__':
    mapping = fedelemflowlist.get_flowmapping()
    mapping.to_csv(outputpath + 'All_Mappings.csv', index=False)