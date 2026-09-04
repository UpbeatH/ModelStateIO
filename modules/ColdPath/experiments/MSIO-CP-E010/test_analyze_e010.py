import json, tempfile, unittest
from pathlib import Path
from analyze_e010 import analyze

def receipt(trial, mode, value=2.5):
    return {'trial': trial, 'mode': mode, 'time_to_ok_s': value}

class AnalyzerTest(unittest.TestCase):
    def write(self, rows):
        d = tempfile.TemporaryDirectory(); path = Path(d.name)
        for i, row in enumerate(rows): (path / f'{i}.receipt.json').write_text(json.dumps(row), encoding='utf-8')
        return d, path
    def rows(self):
        return [receipt(f'b{b}-p{p}-{m}', m, 2.0 + 0.01 * p) for b, (m1, m2, m3) in enumerate([('mmap','none','dio')]*6, 1) for p, m in enumerate((m1,m2,m3), 1)]
    def test_valid_identity(self):
        d, path = self.write(self.rows()); self.assertEqual(analyze(path, 'MSIO-CP-E009R1')['experiment'], 'MSIO-CP-E009R1'); d.cleanup()
    def test_mixed_trial_rejected(self):
        rows = self.rows(); rows[0]['trial'] = 'old-E007-b1-p1-mmap'; d, path = self.write(rows)
        with self.assertRaises(ValueError): analyze(path, 'MSIO-CP-E009R1')
        d.cleanup()
    def test_incomplete_rejected(self):
        d, path = self.write(self.rows()[:-1])
        with self.assertRaises(ValueError): analyze(path, 'MSIO-CP-E009R1')
        d.cleanup()

