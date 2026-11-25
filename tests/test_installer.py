from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from upe.integrity import bundled_skill_path, write_manifest
from upe.installer import (
    InstallationConflict,
    InstallationStateError,
    install_skill,
    uninstall_skill,
    update_skill,
    verify_installation,
)


def copy_bundle(destination: Path) -> Path:
    shutil.copytree(
        bundled_skill_path(), destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return destination


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="upe test with spaces ")
        self.root = Path(self.temp.name)
        self.source = copy_bundle(self.root / "universal-prompt-engineering")
        self.destination = self.root / "Agent workspace" / ".agents" / "skills" / "universal-prompt-engineering"
        self.state = self.root / "user state"

    def tearDown(self):
        self.temp.cleanup()

    def test_clean_install_copies_verified_skill_and_receipt(self):
        result = install_skill(self.source, self.destination, self.state, version="test-version")
        self.assertEqual(result.action, "installed")
        self.assertTrue((self.destination / "SKILL.md").is_file())
        self.assertTrue(verify_installation(self.destination, self.state).valid)

    def test_reinstall_is_idempotent(self):
        install_skill(self.source, self.destination, self.state, version="test-version")
        result = install_skill(self.source, self.destination, self.state, version="test-version")
        self.assertEqual(result.action, "unchanged")

    def test_dry_run_has_no_filesystem_side_effects(self):
        result = install_skill(self.source, self.destination, self.state, version="test-version", dry_run=True)
        self.assertEqual(result.action, "would install")
        self.assertFalse(self.destination.exists())
        self.assertFalse(self.state.exists())

    def test_unmanaged_existing_skill_is_not_overwritten(self):
        self.destination.mkdir(parents=True)
        custom = self.destination / "SKILL.md"
        custom.write_text("user content", encoding="utf-8")
        with self.assertRaises(InstallationConflict):
            install_skill(self.source, self.destination, self.state, version="test-version")
        self.assertEqual(custom.read_text(encoding="utf-8"), "user content")

    def test_install_refuses_symlinked_parent(self):
        outside = self.root / "outside"
        outside.mkdir()
        link = self.root / "linked parent"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symlinks unavailable: {exc}")
        target = link / "skills" / "universal-prompt-engineering"
        with self.assertRaises(InstallationConflict):
            install_skill(self.source, target, self.state, version="test-version")
        self.assertFalse((outside / "skills").exists())

    def test_installer_guard_refuses_a_link_component_reported_by_platform(self):
        blocked = self.root / "blocked parent"
        target = blocked / "skills" / "universal-prompt-engineering"
        real_check = __import__("upe.installer", fromlist=["_is_linklike"])._is_linklike
        with patch("upe.installer._is_linklike", side_effect=lambda path: path == blocked or real_check(path)):
            with self.assertRaises(InstallationConflict):
                install_skill(self.source, target, self.state, version="test-version")

    def test_update_replaces_only_files_unchanged_since_managed_install(self):
        install_skill(self.source, self.destination, self.state, version="1")
        skill_md = self.source / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\nUpdate marker.\n", encoding="utf-8")
        write_manifest(self.source)
        result = update_skill(self.source, self.destination, self.state, version="2")
        self.assertEqual(result.action, "updated")
        self.assertIn("Update marker.", (self.destination / "SKILL.md").read_text(encoding="utf-8"))
        self.assertTrue(verify_installation(self.destination, self.state).valid)

    def test_update_refuses_to_overwrite_user_modified_managed_file(self):
        install_skill(self.source, self.destination, self.state, version="1")
        installed = self.destination / "README.md"
        installed.write_text("user customization", encoding="utf-8")
        skill_md = self.source / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\nUpdate marker.\n", encoding="utf-8")
        write_manifest(self.source)
        with self.assertRaises(InstallationConflict):
            update_skill(self.source, self.destination, self.state, version="2")
        self.assertEqual(installed.read_text(encoding="utf-8"), "user customization")

    def test_uninstall_removes_only_managed_files_and_preserves_extra_user_files(self):
        install_skill(self.source, self.destination, self.state, version="1")
        extra = self.destination / "my-notes.txt"
        extra.write_text("keep", encoding="utf-8")
        result = uninstall_skill(self.destination, self.state)
        self.assertEqual(result.action, "uninstalled")
        self.assertTrue(extra.is_file())
        self.assertEqual(extra.read_text(encoding="utf-8"), "keep")
        self.assertFalse((self.destination / "SKILL.md").exists())

    def test_uninstall_preserves_modified_managed_files_and_receipt(self):
        install_skill(self.source, self.destination, self.state, version="1")
        modified = self.destination / "SKILL.md"
        modified.write_text("user edit", encoding="utf-8")
        with self.assertRaises(InstallationConflict):
            uninstall_skill(self.destination, self.state)
        self.assertEqual(modified.read_text(encoding="utf-8"), "user edit")
        self.assertTrue(any((self.state / "installations").glob("*.json")))

    def test_uninstall_refuses_symlinked_managed_parent_without_touching_external_file(self):
        install_skill(self.source, self.destination, self.state, version="1")
        scripts = self.destination / "scripts"
        outside = self.root / "outside scripts"
        outside.mkdir()
        external = outside / "approval_gate.py"
        external.write_text("user data", encoding="utf-8")
        for child in scripts.iterdir():
            child.unlink()
        scripts.rmdir()
        try:
            scripts.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symlinks unavailable: {exc}")
        with self.assertRaises(InstallationConflict):
            uninstall_skill(self.destination, self.state)
        self.assertEqual(external.read_text(encoding="utf-8"), "user data")

    def test_malformed_or_missing_receipt_never_deletes_files(self):
        self.destination.mkdir(parents=True)
        keep = self.destination / "SKILL.md"
        keep.write_text("unmanaged", encoding="utf-8")
        with self.assertRaises(InstallationStateError):
            uninstall_skill(self.destination, self.state)
        self.assertEqual(keep.read_text(encoding="utf-8"), "unmanaged")


if __name__ == "__main__":
    unittest.main()
