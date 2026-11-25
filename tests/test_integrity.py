from pathlib import Path
import shutil
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from upe.integrity import bundled_skill_path, verify_skill, write_manifest


def copy_bundle(destination: Path) -> Path:
    source = bundled_skill_path()
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return destination


class SkillIntegrityTests(unittest.TestCase):
    def test_bundled_skill_manifest_and_required_content_verify(self):
        result = verify_skill()
        self.assertTrue(result.valid, result.errors)
        self.assertGreaterEqual(result.checked_files, 50)

    def test_skill_entrypoint_references_the_bundled_knowledge_index(self):
        content = (bundled_skill_path() / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/KNOWLEDGE_INDEX.md", content)
        self.assertNotIn("../KNOWLEDGE_INDEX.md", content)
        self.assertNotIn("../workflows/", content)

    def test_research_dossier_copy_matches_embedded_original_hashes(self):
        skill = bundled_skill_path()
        manifest = json.loads(
            (skill / "references/original_dossier/ORIGINALS_SHA256.json").read_text(encoding="utf-8")
        )
        research = ROOT / "DOSSIER_ENGENHARIA_DE_PROMPTS"
        self.assertEqual(len(manifest), 14)
        for filename, expected in manifest.items():
            original = skill / "references" / "original_dossier" / filename
            copy = research / filename
            self.assertTrue(copy.is_file(), filename)
            import hashlib
            self.assertEqual(hashlib.sha256(copy.read_bytes()).hexdigest(), expected, filename)
            self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), expected, filename)

    def test_manifest_detects_changed_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = copy_bundle(Path(temp) / "universal-prompt-engineering")
            (root / "SKILL.md").write_text("tampered", encoding="utf-8")
            result = verify_skill(root)
            self.assertFalse(result.valid)
            self.assertTrue(any("hash mismatch" in item for item in result.errors))

    def test_manifest_detects_missing_and_unlisted_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = copy_bundle(Path(temp) / "universal-prompt-engineering")
            (root / "templates/optimized_prompt.md").unlink()
            (root / "user-added.txt").write_text("extra", encoding="utf-8")
            result = verify_skill(root)
            self.assertFalse(result.valid)
            self.assertTrue(any("missing" in item for item in result.errors))
            self.assertTrue(any("unlisted" in item for item in result.errors))

    def test_manifest_writer_omits_caches_and_itself(self):
        with tempfile.TemporaryDirectory() as temp:
            root = copy_bundle(Path(temp) / "universal-prompt-engineering")
            cache = root / "scripts/__pycache__"
            cache.mkdir()
            (cache / "noise.pyc").write_bytes(b"cache")
            count = write_manifest(root)
            result = verify_skill(root)
            self.assertTrue(result.valid, result.errors)
            self.assertEqual(count, result.checked_files)
            self.assertFalse(any("__pycache__" in item for item in result.errors))

    def test_manifest_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = copy_bundle(Path(temp) / "universal-prompt-engineering")
            manifest = root / "MANIFEST.sha256"
            manifest.write_text("0" * 64 + "  ../outside.txt\n", encoding="utf-8")
            result = verify_skill(root)
            self.assertFalse(result.valid)
            self.assertTrue(any("unsafe manifest path" in item for item in result.errors))


if __name__ == "__main__":
    unittest.main()
