"""No API calls or Docker required to test token parsing."""
import unittest
from token_audit import extract, summarize

class TokenAuditTests(unittest.TestCase):
    def test_only_usage_lines_are_parsed(self):
        text = ("ignored private field\n"
                "LLM token usage: input=10500 output=417 total=10917\n"
                "LLM token usage: input=42100 output=9 total=42109")
        self.assertEqual(extract(text), [
            {"input": 10500, "output": 417, "total": 10917},
            {"input": 42100, "output": 9, "total": 42109},
        ])

    def test_large_calls_are_flagged(self):
        result = summarize(extract("LLM token usage: input=42100 output=9 total=42109"), 10, 12000)
        self.assertEqual(result["calls_over_threshold"], 1)
        self.assertFalse(result["model_attribution_available"])

    def test_missing_logs_are_not_success(self):
        self.assertEqual(summarize([], 20, 12000)["status"], "NO_DATA")

if __name__ == "__main__":
    unittest.main()
