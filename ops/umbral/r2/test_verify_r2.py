"""Offline tests for the R2 executor: no Docker daemon or OpenAI API required."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from verify_r2 import FILES, SUBDIR, check_folder, discover, docker_command, main, receipt

class R2VerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.folder = (self.repo / "backend" / ".deer-flow" / "users" / "u" /
                       "threads" / "t" / "user-data" / "workspace" / SUBDIR)
        self.folder.mkdir(parents=True)
        for f in FILES:
            (self.folder / f).write_text("# fake data for testing the verifier\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_discovers_real_thread_layout(self):
        self.assertEqual(discover(self.repo), [self.folder])

    def test_receipt_includes_digests(self):
        data = receipt(self.folder, "FILES_FOUND_TESTS_NOT_RUN")
        self.assertEqual(set(data["files"]), set(FILES))
        self.assertEqual(len(data["files"][FILES[0]]["sha256"]), 64)
        self.assertEqual(data["isolation"]["model_requests"], 0)

    def test_docker_isolation(self):
        args = docker_command(self.folder)
        for requirement in ("none", "--read-only", "no-new-privileges", "--cap-drop",
                            "ALL", "65534:65534", "256m"):
            self.assertIn(requirement, args)
        self.assertNotIn("--privileged", args)

    def test_dry_run_does_not_claim_tests_passed(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            status = main(["--repo", str(self.repo), "--dry-run"])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(stdout.getvalue())["status"],
                         "FILES_FOUND_TESTS_NOT_RUN")

    def test_rejects_recreated_artifacts(self):
        fake = self.repo / "other"
        fake.mkdir()
        with self.assertRaises(ValueError):
            check_folder(fake)

if __name__ == "__main__":
    unittest.main()
