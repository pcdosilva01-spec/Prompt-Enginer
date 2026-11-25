"""Contract cases for the existing editorial routing seam, not language quality."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from test_editorial_workflow import PORTUGUESE, LITERAL, ENGLISH
import test_editorial_workflow as fixtures
from approval_gate import GateError
import editorial

class RoutingTests(unittest.TestCase):
    def test_access_priority_and_mixed_scope(self):
        for installed, source, expected in [(True, True, 'installed'), (False, True, 'source'), (False, False, 'portable')]:
            with self.subTest(expected=expected):
                self.assertEqual(editorial.mode_for(dict(parts=[LITERAL, PORTUGUESE, ENGLISH], installed=installed, source_readable=source)), expected)
                clause = editorial.instruction(expected)
                self.assertIn('turno anterior', clause)
                self.assertIn('não force', clause.lower())
                self.assertIn('outros idiomas', clause)
        self.assertIsNone(editorial.mode_for(dict(parts=[LITERAL, ENGLISH], installed=True, source_readable=True)))

    def test_missing_or_duplicate_reference_is_explicit_error(self):
        with TemporaryDirectory() as tmp:
            reference = Path(tmp) / 'humanizer.md'
            with patch.object(editorial, 'REFERENCE', reference):
                with self.assertRaises(GateError):
                    editorial.instruction('portable')
                reference.write_text('### portable\n```text\nOne\n```\n### portable\n```text\nTwo\n```\n', encoding='utf-8')
                with self.assertRaises(GateError):
                    editorial.instruction('portable')
                with self.assertRaises(GateError):
                    editorial.instruction('../bad')

    def test_reject_conflicting_or_duplicate_full_blocks(self):
        case = fixtures.EditorialWorkflowTests()
        case.setUp()
        summary = case.summarize('Responda no Discord', [PORTUGUESE])
        case.approve(summary)
        clause = case.send('build')['instruction']
        with self.assertRaises(GateError):
            case.send('review', prompt=clause + '\n' + clause)
        with self.assertRaises(GateError):
            case.send('review', prompt=clause + '\n' + editorial.instruction('installed'))
        case.send('review', prompt='Responda à mensagem, sem inventar estado.\n' + clause)

    def test_invalid_profile_fails_without_reading_reference(self):
        with patch.object(editorial, 'REFERENCE', None):
            with self.assertRaises(GateError):
                editorial.mode_for(dict(parts=[PORTUGUESE], installed='yes', source_readable=False))
            self.assertIsNone(editorial.mode_for(dict(parts=[LITERAL], installed=False, source_readable=False)))
