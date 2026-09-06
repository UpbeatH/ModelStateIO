import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("prepare_mbpp_tasks", HERE / "prepare_mbpp_tasks.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PrepareTasksTest(unittest.TestCase):
    def test_deduplicates_and_hides_heldout_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.jsonl"
            with source.open("w", encoding="utf-8") as stream:
                for index in range(400):
                    prompt = "Task {}\n\nTest cases:\nassert f({}) == {}".format(index, index, index)
                    stream.write(json.dumps({"prompt": prompt, "llm_steps": ["forbidden"]}) + "\n")
                stream.write(json.dumps({"prompt": "Task 0\n\nTest cases:\nassert f(0) == 0"}) + "\n")
            development = root / "development.jsonl"
            heldout = root / "heldout.json"
            self.assertEqual(MODULE.prepare([source], development, heldout), (300, 100))
            rows = [json.loads(line) for line in development.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 300)
            self.assertNotIn("llm_steps", rows[0])
            receipt = json.loads(heldout.read_text(encoding="utf-8"))
            self.assertFalse(receipt["content_disclosed"])
            self.assertEqual(len(receipt["ordered_prompt_sha256"]), 100)


if __name__ == "__main__":
    unittest.main()
