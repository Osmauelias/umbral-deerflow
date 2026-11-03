"""No network: verify Cloud runner never spends without --execute."""
import contextlib
import io
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch
import cloud_smoke

class CloudWorkerContractTests(unittest.TestCase):
    def test_default_is_no_spend(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = cloud_smoke.main([])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue())["expected_artifact"], cloud_smoke.OUTPUT)
        self.assertIn("separately from ChatGPT Plus", output.getvalue())

    def test_specs_are_unambiguous(self):
        for part in ("leading zeros", "internal spaces", "UMB-00123",
                     "test_normalizar_folio.py", "test_output.txt", "ZIP"):
            self.assertIn(part, cloud_smoke.TASK)

    def test_requires_api_key_to_execute(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with self.assertRaisesRegex(RuntimeError, "Missing local OPENAI_API_KEY"):
                cloud_smoke.run_worker("gpt-6.1-sol", Path("/tmp/umbral_not_running.zip"))

if __name__ == "__main__":
    unittest.main()
