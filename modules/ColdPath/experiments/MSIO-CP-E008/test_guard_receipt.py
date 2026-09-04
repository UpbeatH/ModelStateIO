import unittest
from guard_receipt import evaluate


class GuardReceiptTest(unittest.TestCase):
    def test_no_process(self):
        receipt = evaluate("no-process", [(0.0, [])], {"memory_used_mib": 0})
        self.assertEqual(receipt["decision"], "PASS")

    def test_transient_settles(self):
        receipt = evaluate("transient-fixture", [(0.0, [{"pid": 1, "cmd": "fixture"}]), (5.0, [])], {})
        self.assertEqual(receipt["decision"], "SETTLED")

    def test_persistent_is_no_go(self):
        receipt = evaluate("persistent-fixture", [(0.0, [{"pid": 1, "cmd": "fixture"}]), (5.0, [{"pid": 1, "cmd": "fixture"}])], {})
        self.assertEqual(receipt["decision"], "NO_GO")


if __name__ == "__main__":
    unittest.main()
