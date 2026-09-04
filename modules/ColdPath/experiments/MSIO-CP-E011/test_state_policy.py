import unittest
from state_policy import classify

class StatePolicyTest(unittest.TestCase):
    def test_warm_accept(self):
        self.assertEqual(classify('natural_warm', 'normal_process_start', True)['decision'], 'ACCEPT')
    def test_forbidden_cold_no_go(self):
        self.assertEqual(classify('explicit_cold', 'drop_caches', True)['decision'], 'NO_GO')
    def test_unknown_abstain(self):
        self.assertEqual(classify('unknown', 'unspecified', False)['decision'], 'ABSTAIN')

