"""Offline contract tests. Output parts and editorial decisions are host fixtures."""
from pathlib import Path
import tempfile
import unittest

from test_interaction import BRIEF, OFFER, REVIEW
from approval_gate import GateError
from interaction import Workflow


DISCORD = "Crie um prompt para um texto de apresentação de sugestões de um servidor Discord"
PROPOSAL = "Talvez abrir 2 canais, se houver aprovação. Não arquivar #ajuda."
PORTUGUESE = {"kind": "prose", "language": "pt-BR"}
LITERAL = {"kind": "literal", "language": "und"}
ENGLISH = {"kind": "prose", "language": "en"}


class EditorialWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.state = None

    def send(self, kind, directory=None, **fields):
        work, reply = Workflow.step(self.state, {"type": kind, **fields}, directory)
        self.state = work.to_dict()
        return reply

    def summarize(self, task, parts, *, installed=False, source=False, requirements=None):
        profile = dict(parts=parts, installed=installed, source_readable=source)
        self.send("understand", brief=BRIEF | {"task": task, "editorial": profile},
                  requirements=requirements or {"output": task})
        return self.send("present_summary", summary=f"1. Objetivo aprovado em seguida: {task}")

    def approve(self, summary):
        self.send("approval", actor="user", action="approve", digest=summary["digest"])

    def test_discord_portable_prompt_and_exact_txt_after_current_approval(self):
        summary = self.summarize(DISCORD, [PORTUGUESE], requirements={
            "audience": "Membros do servidor, em linguagem cordial e direta.",
            "proposal": PROPOSAL,
        })
        self.assertIn(PROPOSAL, summary["text"])
        self.send("approval", actor="user", action="ambiguous")
        with self.assertRaises(GateError):
            self.send("build")
        with self.assertRaises(GateError):
            self.send("deliver", packet={})
        self.approve(summary)
        instruction = self.send("build")["instruction"]
        self.assertNotIn(instruction, summary["text"])
        self.assertIn("Humanizer", instruction)
        self.assertNotIn("https://", instruction)
        for term in ("destinatário", "registro", "negações", "condições", "certeza", "comandos"):
            with self.subTest(term=term):
                self.assertIn(term, instruction.casefold())
        body = ("Apresente a proposta aos membros do servidor Discord em tom cordial e direto. "
                "Preserve a condição e a negativa.\nProposta fornecida: " + PROPOSAL)
        with self.assertRaises(GateError):
            self.send("review", prompt=body + "\nO engenheiro consultou a Humanizer.")
        prompt = body + "\n\n" + instruction
        self.send("review", prompt=prompt)
        packet = dict(prompt=prompt, digest=summary["digest"], recommendation=self.state["recommendation"],
                      format="native", native_supported=True, files_supported=True, offer=OFFER,
                      txt_path="prompt.txt", txt_link="./prompt.txt", review=REVIEW)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "prompt.txt"
            output.write_bytes(prompt.replace("2 canais", "3 canais").encode("utf-8"))
            with self.assertRaises(GateError):
                self.send("prepare_delivery", directory, packet=packet)
            output.write_bytes(prompt.encode("utf-8"))
            self.send("prepare_delivery", directory, packet=packet)
            result = self.send("deliver", directory, packet=packet)
            self.assertEqual(output.read_bytes(), result["native_prompt"].encode("utf-8"))
        self.assertEqual(result["native_prompt"], prompt)
        self.assertRegex(result["text"].casefold(), r"humanizer[^\n]*portátil|portátil[^\n]*humanizer")
        self.assertNotIn(instruction, result["text"])
        self.assertIn("Baixar prompt TXT", result["text"])
        self.assertEqual(result["text"].count("Verificado: "), 10)
        self.assertTrue(result["text"].endswith(OFFER))

    def test_confirmed_installation_or_pinned_source_in_reviewed_prompt(self):
        for installed, source in ((True, False), (True, True), (False, True)):
            with self.subTest(installed=installed, source=source):
                self.state = None
                summary = self.summarize("Revise o ofício em registro institucional.", [PORTUGUESE],
                                         installed=installed, source=source)
                self.approve(summary)
                clause = self.send("build")["instruction"]
                self.assertIn("humanizar-natural-ptbr", clause)
                if installed:
                    self.assertNotIn("https://", clause)
                else:
                    self.assertRegex(clause.lower(), r"github\.com/pcdosilva01-spec/humanizer-skill/tree/[0-9a-f]{40}")
                    self.assertIn("skills/humanizar-natural-ptbr/SKILL.md", clause)
                    self.assertIn("references/fidelidade.md", clause)
                with self.assertRaises(GateError):
                    self.send("review", prompt="O engenheiro consultou a Humanizer.")
                self.send("review", prompt="Preserve o registro institucional solicitado.\n" + clause)

    def test_only_target_prose_activates_editorial_instruction(self):
        cases = (
            ("Escreva código Python", [LITERAL]),
            ('Retorne apenas o JSON {"aviso":"Não autorizado"}', [{"kind": "literal", "language": "pt-BR"}]),
            ("Escreva um e-mail em inglês para o fórum", [ENGLISH]),
            ("Reescreva o artigo em português europeu", [{"kind": "prose", "language": "pt-PT"}]),
        )
        for task, parts in cases:
            with self.subTest(task=task):
                self.state = None
                self.approve(self.summarize(task, parts, installed=True))
                self.assertIsNone(self.send("build"))
                self.send("review", prompt=task)

    def test_change_to_mixed_formal_readme_invalidates_previous_approval(self):
        task = "Prepare README bilíngue com um exemplo de configuração."
        first = self.summarize(task, [ENGLISH, LITERAL], installed=True)
        self.approve(first)
        self.send("build")
        literals = 'npm ci\n{"quota":2,"can_publish":false}'
        second = self.summarize(task, [PORTUGUESE, ENGLISH, LITERAL], requirements={
            "voice": "Registro formal na versão brasileira. Mantenha o parágrafo em inglês.",
            "literal": literals,
        })
        self.assertIn(literals, second["text"])
        self.assertNotEqual(first["digest"], second["digest"])
        with self.assertRaises(GateError):
            self.send("approval", actor="user", action="approve", digest=first["digest"])
        self.approve(second)
        instruction = self.send("build")["instruction"]
        self.assertIn("outros idiomas", instruction)
        self.assertIn("dados estruturados", instruction)
        self.assertIn("registro", instruction)
        self.send("review", prompt="Use registro formal. Mantenha em inglês ‘Release notes’.\n"
                  + literals + "\n\n" + instruction)
