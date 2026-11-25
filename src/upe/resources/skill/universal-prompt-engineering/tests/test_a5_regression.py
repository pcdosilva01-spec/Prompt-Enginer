"""Contract regressions fixed before a5 implementation; no model execution."""
import unittest
from unittest.mock import patch
import test_interaction as old
import test_editorial_workflow as fixtures
from approval_gate import GateError
from model_selection import recommend
from model_catalog import read_family, DIRECTORY
import editorial


class A5Regression(unittest.TestCase):
    def test_inactive_rejects_full_recipient_instructions(self):
        for parts in ([fixtures.LITERAL], [fixtures.ENGLISH]):
            for mode in ('installed', 'source', 'portable'):
                with self.subTest(parts=parts, mode=mode):
                    case = fixtures.EditorialWorkflowTests()
                    case.setUp()
                    case.approve(case.summarize('Produza apenas a saída classificada.', parts))
                    self.assertIsNone(case.send('build'))
                    with self.assertRaises(GateError):
                        case.send('review', prompt='Produza a saída.\n\n' + editorial.instruction(mode))
                    case.send('review', prompt='Produza a saída. O nome Humanizer é dado literal.')

    def test_inactive_clean_review_does_not_load_editorial_reference(self):
        case = fixtures.EditorialWorkflowTests()
        case.setUp()
        case.approve(case.summarize('Escreva em inglês.', [fixtures.ENGLISH]))
        with patch.object(editorial, '_blocks', side_effect=AssertionError('unexpected load')):
            self.assertIsNone(case.send('build'))
            case.send('review', prompt='Write the answer in English.')

    def test_rejected_api_effort_not_selected_automatically(self):
        for model in ('gpt-6.2-astra', 'gpt-6.2-sol'):
            with self.subTest(model=model):
                brief = old.BRIEF | {'platform':'OpenAI API'}
                invalid = old.fixture_candidate(model, platform='OpenAI API', reasoning='none', economy=True)
                valid = old.fixture_candidate(model, platform='OpenAI API', reasoning='medium')
                result = recommend(brief, [invalid, valid])
                self.assertEqual(result['primary']['reasoning'], 'medium')
                self.assertNotEqual(result['alternative']['reasoning'], 'none')
                result = recommend(brief | {'chosen_model':model,'chosen_reasoning':'none'}, [invalid, valid])
                self.assertFalse(result['primary']['sufficient'])
                self.assertEqual(result['brief']['chosen_reasoning'], 'none')
                self.assertNotEqual(result['primary']['reasoning'], 'medium')

    def test_does_not_transfer_api_rejection_to_codex(self):
        row = old.fixture_candidate('gpt-6.2-sol', reasoning='none')
        result = recommend(old.BRIEF, [row])
        self.assertEqual(result['primary']['reasoning'], 'none')
        # This synthetic input is not evidence that Codex accepts none.

    def test_reject_duplicate_mode_block_in_reference(self):
        # A malformed source must not silently yield a second instruction.
        content = editorial.REFERENCE.read_text(encoding='utf-8')
        content = content.replace('### source\n', '### source\n', 1).replace('\n```\n\n### portable', '\n```\n```text\nSecond\n```\n\n### portable', 1)
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as tmp:
            ref = Path(tmp) / 'humanizer.md'
            ref.write_text(content, encoding='utf-8')
            with patch.object(editorial, 'REFERENCE', ref), self.assertRaises(GateError):
                editorial.instruction('source')
