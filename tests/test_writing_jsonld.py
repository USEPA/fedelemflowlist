"""
Tests for that flows and mappings are written as expected to JSON-LD archives.
"""
import unittest
from pathlib import Path
import fedelemflowlist
from fedelemflowlist.globals import outputpath, log
import zipfile


class TestWritingJSONLD(unittest.TestCase):
    """Add docstring."""

    def test_writing_flows(self):
        """Test that first 100 flows are written to 100 files in JSON_LD archive."""
        flowlist = fedelemflowlist.get_flows(preferred_only=False)
        #Test first 100
        flowlist = flowlist.iloc[0:100]
        try:
            flowlist_json_file =  outputpath / 'test_FedElemFlowList_first100.zip'
            # Remove the test file if it already exists
            if flowlist_json_file.exists():
                flowlist_json_file.unlink()
            fedelemflowlist.write_jsonld(flowlist,flowlist_json_file)
        except PermissionError:
            log.error("No permission to write to file " + flowlist_json_file)
        try:
            flowlist_json = zipfile.ZipFile(flowlist_json_file)
            test_extract_path = outputpath / 'test_FedElemFlowList_first100'
            flowlist_json.extractall(test_extract_path)
            flows_path = test_extract_path / 'flows'
            categories_path = test_extract_path / 'categories'
            len_extracted_flow_files = len(list(Path(flows_path).rglob('*')))
            # Clean up
            for f in Path.iterdir(flows_path):
                Path.unlink(flows_path / f)
            for f in Path.iterdir(categories_path):
                Path.unlink(categories_path / f)
            Path.rmdir(flows_path)
            Path.rmdir(categories_path)
            Path.rmdir(test_extract_path)
        except FileNotFoundError:
            log.error(flowlist_json_file + ' not found')
        self.assertEqual(100, len_extracted_flow_files)


if __name__ == '__main__':
    unittest.main()
