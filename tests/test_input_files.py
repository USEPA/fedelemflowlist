"""Tests for input files used to build flow list to provide quality assurance."""
import unittest
import pandas as pd
from fedelemflowlist.flowlist import read_in_flowclass_file, import_secondary_context_membership
from fedelemflowlist.globals import flow_list_specs,log
from fedelemflowlist.contexts import contexts, compartment_classes

class TestInputFiles(unittest.TestCase):
    """Add docstring."""

    def test_flowables_match_primary_context_flowables(self):
        """
        For each flow class, tests that flowables in Flowables match those in
        FlowablePrimaryContexts.
        """
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            primarycontexts = read_in_flowclass_file(c_, "FlowablePrimaryContexts")
            flowables_in_flowables = set(flowables['Flowable'])
            flowables_in_primary_contexts = set(primarycontexts['Flowable'])
            self.assertEqual(flowables_in_flowables, flowables_in_primary_contexts)

    def test_duplicate_flowables(self):
        """For each flow class, tests for duplicate flowable names."""
        duplicates = 0
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            flowables_in_flowables = set(flowables['Flowable'])
            class_duplicates = len(flowables.index) - len(flowables_in_flowables)
            if class_duplicates > 0:
                log.debug('duplicate flowables in '+ c_)
                duplicates = duplicates + class_duplicates
        self.assertTrue(duplicates==0,'Duplicate flowables')
        
    def test_altunit_files_match_flowables(self):
        """For each flow class, test flowables in AltUnits are defined in Flowables."""
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            flowables_w_unit = flowables[['Flowable','Unit']]
            try:
                altunits_for_class = read_in_flowclass_file(c_, 'FlowableAltUnits')
                #First make sure reference units here match those in the flowables file
                flowables_in_flowables = set(flowables['Flowable'])
                flowables_in_altunits = set(altunits_for_class['Flowable'])
                self.assertTrue(flowables_in_altunits.issubset(flowables_in_flowables))
                #May sure ref units are the same in both files
                altunits_w_unit = altunits_for_class[['Flowable','Reference Unit']]
                merge_units = pd.merge(flowables_w_unit, altunits_w_unit, left_on=['Flowable','Unit'],
                                       right_on=['Flowable','Reference Unit'])
                #The merge should have found a row for every row in altunits
                self.assertEqual(len(altunits_w_unit),len(merge_units))
            except FileNotFoundError:
                altunits_for_class = None

    def test_units_are_olcaunits(self):
        """Test that units are openlca reference units."""
        import olca.units as olcaunits
        
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            # Get units and test that they are olca ref units
            ref_units = pd.unique(flowables['Unit'])
            for unt in ref_units:
                olcaref = olcaunits.unit_ref(unt)
                if olcaref is None:
                    log.debug(unt + ' in Flowables for class ' + c_ + ' is not an olca ref unit')
                self.assertIsNotNone(olcaref)
            try:
                altunits_for_class = read_in_flowclass_file(c_, 'FlowableAltUnits')
                alt_units_with_ref = list(altunits_for_class['Alternate Unit']) + list(
                    altunits_for_class['Reference Unit'])
                alt_units_with_ref_unique = set(alt_units_with_ref)
                for unt in alt_units_with_ref_unique:
                    olcaref = olcaunits.unit_ref(unt)
                    if olcaref is None:
                        log.debug(unt + ' in alt units for class ' + c_ + ' is not an olca ref unit')
                    self.assertIsNotNone(olcaref)
            except FileNotFoundError:
                altunits_for_class = None


    def test_compartment_classes_match(self):
        """
        Test that compartment classes in Contexts and Secondary Context
        Membership match those in flow list specs.
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

    def test_synonyms_in_flowables(self):
        """Checks synonyms for bad characters."""
        for c_ in flow_list_specs["flow_classes"]:
            flowables = read_in_flowclass_file(c_, "Flowables")
            synonyms = list(flowables['Synonyms'].dropna())
            for v in synonyms:
                if '\n' in v or '\r' in v:
                    self.fail('Bad characters in synonymns: ' + v)

if __name__ == '__main__':
    unittest.main()
