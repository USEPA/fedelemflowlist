"""
Tests for that flows and mappings are written as expected to JSON-LD archives
"""
import unittest
import fedelemflowlist
from fedelemflowlist.globals import outputpath, log
import zipfile
import os

class TestWritingJSONLD(unittest.TestCase):

    def test_writing_flows(self):
        """Test that first 100 preferred flows are written to 100 files in JSON_LD archive
        """
        flowlist = fedelemflowlist.get_flows(preferred_only=False)
        #Test first 100
        flowlist = flowlist.iloc[0:100]
        try:
            flowlist_json_file =  outputpath+'test_FedElemFlowList_first100.zip'
            #Remove the test file if it already exists
            if os.path.exists(flowlist_json_file):
                os.remove(flowlist_json_file)
            fedelemflowlist.write_jsonld(flowlist,flowlist_json_file)
        except PermissionError:
            log.error("No permission to write to file " + flowlist_json_file)
        try:
            flowlist_json = zipfile.ZipFile(flowlist_json_file)
            test_extract_path = outputpath + 'test_FedElemFlowList_first100/'
            flowlist_json.extractall(test_extract_path)
            flows_path = test_extract_path + 'flows/'
            categories_path = test_extract_path + 'categories/'
            flow_files = os.listdir(flows_path)
            len_extracted_flow_files = len(flow_files)
            #Clean up
            for f in flow_files:
                os.remove(flows_path+f)
            category_files = os.listdir(categories_path)
            for f in category_files:
                os.remove(categories_path+f)
            os.removedirs(flows_path)
            os.removedirs(categories_path)
            os.removedirs(test_extract_path)
        except FileNotFoundError:
            log.error(flowlist_json_file + ' not found')
        self.assertEqual(100,len_extracted_flow_files)


if __name__ == '__main__':
    unittest.main()
