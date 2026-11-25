from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import tools.build_release as release_builder
from tools.build_release import build
from tools.check_distribution import _check_manifest, _zip_files


class ReleaseArchiveTests(unittest.TestCase):
    def test_builds_verified_skill_and_source_archives_without_overwriting(self):
        with tempfile.TemporaryDirectory(prefix="upe release with spaces ") as temp:
            output = Path(temp)
            paths = build(output)
            skill_zip, source_zip, skill_hash, source_hash = paths
            self.assertTrue(skill_zip.is_file())
            self.assertTrue(source_zip.is_file())
            skill_files = _zip_files(skill_zip)
            errors = _check_manifest(skill_files, "universal-prompt-engineering/", skill_zip.name)
            self.assertEqual(errors, [])
            self.assertIn("universal-prompt-engineering/SKILL.md", skill_files)
            source_files = _zip_files(source_zip)
            self.assertIn(
                "Prompter-Silva-local-candidate/src/upe/resources/skill/universal-prompt-engineering/SKILL.md",
                source_files,
            )
            self.assertNotIn(
                "Prompter-Silva-local-candidate/push_force_Prompter-Silva.bat",
                source_files,
            )
            for artifact in (skill_zip, source_zip):
                with zipfile.ZipFile(artifact) as archive:
                    self.assertIsNone(archive.testzip())
            self.assertNotIn("Prompter-Silva-local-candidate/docs/history/v1.0.1/README.md", source_files)
            self.assertNotIn(
                "Prompter-Silva-local-candidate/docs/research/DOSSIER_ENGENHARIA_DE_PROMPTS/README.md",
                source_files,
            )
            self.assertFalse(any(name.startswith("Prompter-Silva-local-candidate/dist/") for name in source_files))
            legacy_zip = "Prompter-Silva-local-candidate/SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS.zip"
            self.assertIn(legacy_zip, source_files)
            self.assertEqual(source_files[legacy_zip], (ROOT / "SKILL_UNIVERSAL_ENGENHARIA_DE_PROMPTS.zip").read_bytes())
            with self.assertRaises(FileExistsError):
                build(output)
            self.assertEqual(skill_hash.read_text(encoding="ascii").split()[0], __import__("hashlib").sha256(skill_zip.read_bytes()).hexdigest())
            self.assertEqual(source_hash.read_text(encoding="ascii").split()[0], __import__("hashlib").sha256(source_zip.read_bytes()).hexdigest())

    def test_failed_archive_build_cleans_only_its_partial_outputs(self):
        real_zip_file = zipfile.ZipFile

        class FailingZipWriter:
            def __init__(self, path, mode="r", **kwargs):
                self.archive = real_zip_file(path, mode, **kwargs)

            def __enter__(self):
                self.archive.__enter__()
                return self

            def __exit__(self, *args):
                return self.archive.__exit__(*args)

            def writestr(self, *args, **kwargs):
                raise OSError("injected archive write failure")

        with tempfile.TemporaryDirectory(prefix="upe failed release ") as temp:
            output = Path(temp)
            with patch.object(release_builder.zipfile, "ZipFile", FailingZipWriter):
                with self.assertRaisesRegex(OSError, "injected archive write failure"):
                    build(output)
            self.assertEqual(list(output.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
