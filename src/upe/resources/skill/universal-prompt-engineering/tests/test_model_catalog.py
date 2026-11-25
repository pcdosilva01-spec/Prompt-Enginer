"""Regression coverage of the local documentary catalog; not provider verification."""
from datetime import date
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import test_interaction  # existing tests add the scripts directory to sys.path
from approval_gate import GateError
from model_catalog import read_family, expires, DIRECTORY

DAY = date(2026, 11, 25)

class CatalogTests(unittest.TestCase):
    def test_snapshot_inventory(self):
        keys = set()
        for path in sorted(DIRECTORY.glob('*.json')):
            data = read_family(path.stem, today=DAY)
            for row in data['models']:
                key = (data['surface'].casefold(), row['id'].casefold())
                self.assertNotIn(key, keys)
                keys.add(key)
                self.assertGreaterEqual(expires(row, DAY), DAY)
        self.assertEqual(len(keys), 44)

    def test_bad_evidence_reference_and_unsafe_family(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            data = json.loads((DIRECTORY / 'openai.json').read_text(encoding='utf-8'))
            data['models'][0]['sources'] = ['nonexistent']
            (directory / 'openai.json').write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaisesRegex(GateError, 'invalid evidence references'):
                read_family('openai', today=DAY, directory=directory)
            with self.assertRaisesRegex(GateError, 'Invalid catalog family'):
                read_family('../openai', today=DAY, directory=directory)

    def test_duplicate_key_rejected(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / 'openai.json').write_text('{"publisher":"x","publisher":"y"}', encoding='utf-8')
            with self.assertRaisesRegex(GateError, 'Duplicate JSON key'):
                read_family('openai', today=DAY, directory=directory)
