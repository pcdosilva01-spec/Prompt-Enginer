import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT.parents[1] / "DOSSIER_ENGENHARIA_DE_PROMPTS"
SOURCE = SOURCE_PATH if SOURCE_PATH.is_dir() else None
sys.path.insert(0, str(ROOT / "scripts"))
import package_skill
from verify_package import verify


class PackageTests(unittest.TestCase):
    def test_package_metadata_links_and_manifests(self):
        self.assertEqual(verify(ROOT, SOURCE), [])

    def test_original_dossier_contains_fourteen_verified_files(self):
        manifest = json.loads((ROOT / "references/original_dossier/ORIGINALS_SHA256.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest), 14)
        for name, digest in manifest.items():
            self.assertEqual(hashlib.sha256((ROOT / "references/original_dossier" / name).read_bytes()).hexdigest(), digest)

    def test_openai_ui_metadata_matches_reviewed_fields(self):
        metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Universal Prompt Engineering"', metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotIn("allowed-tools", metadata)

    def test_archive_write_failure_preserves_previous_zip(self):
        real_zip_file = package_skill.zipfile.ZipFile

        class FailingZipWriter:
            def __init__(self, path, mode="r", **kwargs):
                self.archive = real_zip_file(path, mode, **kwargs)

            def __enter__(self):
                self.archive.__enter__()
                return self

            def __exit__(self, *args):
                return self.archive.__exit__(*args)

            def write(self, *args, **kwargs):
                raise OSError("simulated archive write failure")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            skill_root = temp_root / "skill"
            skill_root.mkdir()
            (skill_root / "SKILL.md").write_text("test", encoding="utf-8")
            output = temp_root / "skill.zip"
            previous_zip = b"previous verified archive"
            output.write_bytes(previous_zip)

            with patch.object(package_skill, "ROOT", skill_root), patch.object(package_skill, "OUTPUT", output), patch.object(package_skill, "verify", return_value=[]), patch.object(package_skill.zipfile, "ZipFile", FailingZipWriter):
                with redirect_stderr(io.StringIO()):
                    self.assertEqual(package_skill.main(), 1)

            self.assertEqual(output.read_bytes(), previous_zip)
            self.assertEqual(list(temp_root.glob(".protected.zip.*.tmp")), [])

    def test_archive_rejects_symlink_before_verification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            skill_root = temp_root / "skill"
            skill_root.mkdir()
            (skill_root / "SKILL.md").write_text("test", encoding="utf-8")
            (skill_root / "external.txt").write_text("external target", encoding="utf-8")
            original_is_symlink = Path.is_symlink

            def pretend_external_symlink(path):
                return path.name == "external.txt" or original_is_symlink(path)

            with patch.object(Path, "is_symlink", pretend_external_symlink), patch.object(package_skill, "verify", side_effect=AssertionError("verification read a package containing a symlink")):
                with self.assertRaisesRegex(ValueError, "symlink"):
                    package_skill.build_archive(skill_root, temp_root / "skill.zip")

    def test_archive_rejects_symlink_output_without_following_it(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            skill_root = temp_root / "skill"
            skill_root.mkdir()
            (skill_root / "SKILL.md").write_text("test", encoding="utf-8")
            output = temp_root / "protected.zip"
            output.write_bytes(b"external target")
            original_is_symlink = Path.is_symlink

            def pretend_zip_symlink(path):
                return path.name == "protected.zip" or original_is_symlink(path)

            with patch.object(Path, "is_symlink", pretend_zip_symlink), patch.object(package_skill, "verify", side_effect=AssertionError("verification ran before output path safety check")):
                with self.assertRaisesRegex(ValueError, "output.*symlink"):
                    package_skill.build_archive(skill_root, output)


if __name__ == "__main__":
    unittest.main()
