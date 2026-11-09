from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from repo_ready_check.cli import audit_repo, render_text


class AuditRepoTests(unittest.TestCase):
    def test_complete_repository_scores_one_hundred(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            (root / ".github" / "ISSUE_TEMPLATE" / "bug.yml").write_text("name: Bug\n", encoding="utf-8")
            (root / ".github" / "pull_request_template.md").write_text("# Checklist\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_demo.py").write_text("pass\n", encoding="utf-8")

            report = audit_repo(root)

            self.assertEqual(report["score"], 100)
            self.assertEqual(report["next_actions"], [])

    def test_empty_repository_reports_actions(self) -> None:
        with TemporaryDirectory() as directory:
            report = audit_repo(directory)

            self.assertEqual(report["score"], 0)
            self.assertEqual(len(report["next_actions"]), 10)
            self.assertIn("README", render_text(report))


if __name__ == "__main__":
    unittest.main()
