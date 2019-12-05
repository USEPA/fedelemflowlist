"""
Tests the stored flow mappings to provide quality assurance
"""
import unittest
import pandas as pd
import fedelemflowlist

def get_required_flowmapping_fields():
    """Gets required field names for Flow Mappingt
    :return:list of required fields
    """
    from fedelemflowlist.globals import flowmapping_fields
    required_fields = []
    for k, v in flowmapping_fields.items():
        if v[1]['required']:
            required_fields.append(k)
    return required_fields

class TestFlowMappings(unittest.TestCase):

    def setUp(self):
        """Get flowlist used for all tests
        """
        self.flowmappings = fedelemflowlist.get_flowmapping()
        self.flowlist = self.flowlist = fedelemflowlist.get_flows()

    def test_no_nas_in_required_fields(self):
        """Checks that no flows have na values in required fields
        """
        required_fields = get_required_flowmapping_fields()
        flowmappings_w_required = self.flowmappings[required_fields]
        nas_in_required = flowmappings_w_required.dropna()
        self.assertEqual(len(flowmappings_w_required), len(nas_in_required))

    def test_targetflowinfo_matches_flows_in_list(self):
        """Checks that target flow information in the mapping files matches a flow in the flowlist
        """
        flowmapping_targetinfo = self.flowmappings[['TargetFlowName', 'TargetFlowUUID',
                                                    'TargetFlowContext', 'TargetUnit']]
        flowmapping_targetinfo.columns = ['Flowable', 'Flow UUID', 'Context', 'Unit']
        flowmappings_w_flowlist = pd.merge(flowmapping_targetinfo,self.flowlist)
        # To identify flowmapping flows not in list
        missing_flows = flowmapping_targetinfo[~flowmapping_targetinfo['Flow UUID'].isin(flowmappings_w_flowlist['Flow UUID'])]
        self.assertEqual(len(flowmapping_targetinfo), len(flowmappings_w_flowlist))


if __name__ == '__main__':
    unittest.main()
