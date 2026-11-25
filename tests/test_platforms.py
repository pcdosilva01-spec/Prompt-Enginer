from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from upe.platforms import TARGETS, TargetError, resolve_skill_path


class TargetPathTests(unittest.TestCase):
    def test_user_targets_resolve_from_supplied_home(self):
        expected_roots = {
            "codex": Path(".agents/skills"),
            "claude-code": Path(".claude/skills"),
            "gemini-cli": Path(".gemini/skills"),
            "antigravity": Path(".gemini/config/skills"),
            "cursor": Path(".cursor/skills"),
            "copilot": Path(".copilot/skills"),
            "cline": Path(".cline/skills"),
            "roo-code": Path(".roo/skills"),
            "opencode": Path(".config/opencode/skills"),
        }
        with tempfile.TemporaryDirectory(prefix="home with spaces ") as temp:
            home = Path(temp)
            for target, relative in expected_roots.items():
                with self.subTest(target=target):
                    self.assertEqual(
                        resolve_skill_path(target, "user", home=home),
                        home / relative / "universal-prompt-engineering",
                    )

    def test_project_targets_resolve_inside_project(self):
        expected_roots = {
            "codex": Path(".agents/skills"),
            "claude-code": Path(".claude/skills"),
            "gemini-cli": Path(".gemini/skills"),
            "antigravity": Path(".agents/skills"),
            "cursor": Path(".cursor/skills"),
            "copilot": Path(".github/skills"),
            "cline": Path(".cline/skills"),
            "roo-code": Path(".roo/skills"),
            "opencode": Path(".opencode/skills"),
        }
        with tempfile.TemporaryDirectory(prefix="project with spaces ") as temp:
            project = Path(temp)
            for target, relative in expected_roots.items():
                with self.subTest(target=target):
                    self.assertEqual(
                        resolve_skill_path(target, "project", project_dir=project),
                        project / relative / "universal-prompt-engineering",
                    )

    def test_unknown_and_manual_targets_cannot_be_installed(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(TargetError):
                resolve_skill_path("unknown-agent", "user", home=Path(temp))
            with self.assertRaises(TargetError):
                resolve_skill_path("chatgpt-web", "user", home=Path(temp))

    def test_project_scope_requires_an_explicit_existing_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing project"
            with self.assertRaises(TargetError):
                resolve_skill_path("codex", "project", project_dir=missing)
            with self.assertRaises(TargetError):
                resolve_skill_path("codex", "project")

    def test_target_catalog_distinguishes_manual_use(self):
        self.assertIn("chatgpt-web", TARGETS)
        self.assertFalse(TARGETS["chatgpt-web"].installable)
        self.assertTrue(TARGETS["codex"].installable)
        self.assertTrue(TARGETS["claude-code"].documentation_url.startswith("https://"))


if __name__ == "__main__":
    unittest.main()
