import os
import unittest

from sysdiagnose.parsers.networkextension import NetworkExtensionParser
from tests import SysdiagnoseTestCase


class TestParsersNetworkExtension(SysdiagnoseTestCase):
    def test_networkextension(self):
        for case_id, _case in self.sd.cases().items():
            with self.subTest(case_id=case_id, ios_version=_case.get("ios_version")):
                p = NetworkExtensionParser(self.sd.config, case=_case)

                if not p.is_compatible():
                    self.skipTest(f"Parser {p.module_name} not compatible with iOS {_case.get('ios_version')}")

                files = p.get_log_files()
                if not files:
                    self.fail(
                        f"No log files found for {case_id}: parser {p.module_name}, iOS {_case.get('ios_version')}"
                    )

                p.save_result(force=True)
                self.assertTrue(os.path.isfile(p.output_file))

                result = p.get_result()
                self.assertTrue("Version" in result)
                self.assert_result_summary_consistent(p, result)

    def test_is_compatible_without_case_model(self):
        """A case whose metadata carries no "model" must not crash is_compatible()."""
        case = {"case_id": "networkextension-no-model", "ios_version": "16.0"}
        p = NetworkExtensionParser(self.sd.config, case=case)
        self.assertIsNone(p.case_model)
        self.assertIsInstance(p.is_compatible(), bool)


if __name__ == "__main__":
    unittest.main()
