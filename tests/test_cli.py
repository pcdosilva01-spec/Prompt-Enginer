from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from upe.cli import main


class CliTests(unittest.TestCase):
    def test_help_lists_real_commands(self):
        output = StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as raised:
            main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        for command in ("install", "update", "uninstall", "doctor", "verify", "list-targets", "version"):
            self.assertIn(command, output.getvalue())

    def test_version_command_reports_package_version(self):
        output = StringIO()
        with redirect_stdout(output):
            result = main(["version"])
        self.assertEqual(result, 0)
        self.assertIn("upe-skill", output.getvalue())

    def test_list_targets_marks_manual_interfaces(self):
        output = StringIO()
        with redirect_stdout(output):
            result = main(["list-targets"])
        self.assertEqual(result, 0)
        self.assertIn("codex", output.getvalue())
        self.assertIn("chatgpt-web", output.getvalue())
        self.assertIn("manual", output.getvalue().lower())

    def test_install_dry_run_does_not_create_user_files(self):
        with tempfile.TemporaryDirectory(prefix="cli home with spaces ") as temp:
            home = Path(temp)
            with redirect_stdout(StringIO()):
                result = main(["install", "codex", "--home", str(home), "--dry-run"])
            self.assertEqual(result, 0)
            self.assertFalse((home / ".agents" / "skills").exists())


if __name__ == "__main__":
    unittest.main()
