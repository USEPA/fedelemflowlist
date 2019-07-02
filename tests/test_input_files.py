"""
Tests for input files used to build flow list to provide quality assurance
"""
import unittest
from fedelemflowlist.flowlist import read_in_flowclass_file, import_secondary_context_membership
from fedelemflowlist.globals import flow_list_specs
from fedelemflowlist.contexts import contexts, compartment_classes

class TestInputFiles(unittest.TestCase):

    def test_flowables_match_primary_context_flowables(self):
        """For each flow class, tests that flowables in Flowables match those
         in FlowablePrimaryContexts
        """
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            primarycontexts = read_in_flowclass_file(c_, "FlowablePrimaryContexts")
            flowables_in_flowables = set(flowables['Flowable'])
            flowables_in_primary_contexts = set(primarycontexts['Flowable'])
            self.assertEqual(flowables_in_flowables, flowables_in_primary_contexts)

    def test_altunitflowables_in_flowables(self):
        """For each flow class, test flowables in AltUnits are defined in Flowables
        """
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            try:
                altunits_for_class = read_in_flowclass_file(c_, 'FlowableAltUnits')
                flowables_in_flowables = set(flowables['Flowable'])
                flowables_in_altunits = set(altunits_for_class['Flowable'])
                self.assertTrue(flowables_in_altunits.issubset(flowables_in_flowables))
            except FileNotFoundError:
                altunits_for_class = None

    def test_compartment_classes_match(self):
        """Test that compartment classes in Contexts and Secondary Context
        Membership match those in flow list specs
        """
        context_classes = set(contexts.columns)
        flowlistspecs_classes = set(compartment_classes)
        self.assertEqual(flowlistspecs_classes, context_classes)
        secondary_context_membership = import_secondary_context_membership()
        secondary_membership_classes = secondary_context_membership.columns
        secondary_membership_classes = secondary_membership_classes.drop(['FlowClass',
                                                                          'ContextPreferred'])
        secondary_membership_classes = set(secondary_membership_classes)
        self.assertEqual(flowlistspecs_classes, secondary_membership_classes)

if __name__ == '__main__':
    unittest.main()
