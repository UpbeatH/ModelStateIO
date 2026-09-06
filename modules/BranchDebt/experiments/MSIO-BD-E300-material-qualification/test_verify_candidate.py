import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("verify_candidate", HERE / "verify_candidate.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VerifyCandidateTest(unittest.TestCase):
    def test_extracts_fenced_python_and_tests(self):
        self.assertEqual(MODULE.extract_code("```python\ndef f(): return 1\n```"), "def f(): return 1\n")
        self.assertEqual(MODULE.extract_tests("Do it\nTest cases:\nassert f() == 1"), "assert f() == 1\n")

    def test_frozen_exit_classification(self):
        self.assertEqual(MODULE.classify(0), "pass")
        self.assertEqual(MODULE.classify(31), "assertion_minor")
        self.assertEqual(MODULE.classify(32), "assertion_major")
        self.assertEqual(MODULE.classify(21), "syntax_failure")
        self.assertEqual(MODULE.classify(124), "timeout_failure")
        self.assertEqual(MODULE.classify(99), "sandbox_failure")


if __name__ == "__main__":
    unittest.main()
