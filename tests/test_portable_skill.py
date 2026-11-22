import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1] / ".agents/skills/seo-machine"


class PortableSkillTests(unittest.TestCase):
    def test_supplied_article_uses_real_modules_and_never_overwrites_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            article = workspace / "article.md"
            article.write_text("# How to plan content\n\nPlan useful content for your readers. Leverage clear examples.")
            command = [sys.executable, str(SKILL / "scripts/analyze_file.py"),
                       str(article), "--keyword", "how to plan content", "--output", "report.json"]
            run = subprocess.run(command, cwd=workspace, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            report = json.loads((workspace / "report.json").read_text())
            self.assertEqual(report["word_count"], len(article.read_text().split()))
            self.assertEqual(report["provider_data"], "not_collected")
            self.assertFalse(report["ranking_or_citation_lift_established"])
            self.assertEqual(report["scrubbing_observations"]["ai_phrases_replaced"], 1)
            self.assertIn("quality", report)
            self.assertIn("intent", report)
            before = (workspace / "report.json").read_bytes()
            self.assertNotEqual(subprocess.run(command, cwd=workspace, capture_output=True).returncode, 0)
            self.assertEqual((workspace / "report.json").read_bytes(), before)

    def test_readiness_reports_missing_setup_without_disclosing_credentials(self):
        result = subprocess.run([sys.executable, str(SKILL / "scripts/preflight.py")],
                                env={**os.environ, "DATAFORSEO_LOGIN": "synthetic-secret-login",
                                     "DATAFORSEO_PASSWORD": "synthetic-secret-password"},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        ready = json.loads(result.stdout)
        self.assertTrue(ready["environment_configuration"]["dataforseo"])
        self.assertFalse(ready["provider_access_verified"])
        self.assertNotIn("synthetic-secret", result.stdout)


if __name__ == "__main__":
    unittest.main()
