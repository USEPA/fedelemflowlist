"""
Tests the stored flow list to provide quality assurance
"""
import unittest
import pandas as pd
import fedelemflowlist

"""
Hard-coded df of flows for testing UUID stability
Code to generate this list was:
fulllist = fedelemflowlist.get_flows()
fulllist_rand10 = fulllist.sample(n=10)
fulllist_rand10_selectcols = fulllist_rand10[['Flowable','Context','Unit','Flow UUID']].reset_index()[['Flowable','Context','Unit','Flow UUID']]
fulllist_rand10_selectcols.to_dict()
"""
existing_flow_list_sample = {'Flowable': {0: 'Copper octanoate',
                                          1: "3,3',4,4'-Tetrachlorodiphenyl ether",
                                          2: 'Ethyl oxalate',
                                          3: 'Disodium methanearsonate',
                                          4: '3,3-Dimethyl-2-butanol',
                                          5: 'Bis(trichloromethyl) sulfone',
                                          6: 'Ethopabate',
                                          7: 'Etrimfos',
                                          8: '2,3,6-Trichlorobenzoic acid',
                                          9: 'Nithiazide'},
                             'Context': {0: 'emission/ground/terrestrial/wetland',
                                         1: 'emission/water/fresh water body/lake/rural',
                                         2: 'emission/air/troposphere/rural',
                                         3: 'emission/ground/human-dominated/residential',
                                         4: 'emission/air/troposphere/rural/ground-level',
                                         5: 'emission/water/fresh water body',
                                         6: 'emission/air/troposphere/urban/low',
                                         7: 'emission/ground/human-dominated/industrial/urban',
                                         8: 'emission/air/troposphere/urban/low',
                                         9: 'emission/air/troposphere/very high'},
                             'Unit': {0: 'kg', 1: 'kg', 2: 'kg', 3: 'kg', 4: 'kg',
                                      5: 'kg', 6: 'kg', 7: 'kg', 8: 'kg', 9: 'kg'},
                             'Flow UUID': {0: '02fae442-4c98-3fec-a144-a357b64d4cde',
                                           1: '3a77e841-180d-31cf-9e1f-ef20cf8d9bd7',
                                           2: '275e3a0b-4344-33ba-bbf0-1f19ce300ae9',
                                           3: '4f69a922-09fb-3f16-a102-369dd5a3c96f',
                                           4: '32b0de65-5a98-35a0-a2fb-e1de9a7853f9',
                                           5: '7dd1af7b-5e71-3e07-81b0-1a732a54f55e',
                                           6: '37ecfb9c-dfeb-3ea6-a737-e899012200bf',
                                           7: 'e9e56675-d754-38d4-8d6b-ff60691f3e19',
                                           8: '74d1f82c-2af6-365d-9346-17b1e981e9be',
                                           9: 'f08ce166-60e5-3d27-937d-d351b62d8569'}}
existing_flow_sample = pd.DataFrame(existing_flow_list_sample)

def get_required_flowlist_fields():
    """Gets required field names for Flow List
    :return:list of required fields
    """
    from fedelemflowlist.globals import flow_list_fields
    required_fields = []
    for k, v in flow_list_fields.items():
        if v[1]['required']:
            required_fields.append(k)
    return required_fields

class TestFlowList(unittest.TestCase):

    def setUp(self):
        """Get flowlist used for all tests
        """
        self.flowlist = fedelemflowlist.get_flows()


    def test_UUID_stability(self):
        """Checks that UUIDs in currently served list are identical to old UUIDs
        """
        merge_new_and_existing = pd.merge(existing_flow_sample, self.flowlist,
                                          on=['Flowable', 'Context', 'Unit'])
        self.assertEqual(set(merge_new_and_existing['Flow UUID_x']),
                         set(merge_new_and_existing['Flow UUID_y']))


    def test_no_nas_in_required_fields(self):
        """Checks that no flows have na values in required fields
        """
        required_fields = get_required_flowlist_fields()
        flowlist_w_required = self.flowlist[required_fields]
        nas_in_required = flowlist_w_required.dropna()
        self.assertEqual(len(flowlist_w_required), len(nas_in_required))


if __name__ == '__main__':
    unittest.main()
