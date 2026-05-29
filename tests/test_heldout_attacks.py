import unittest

from src.attacks.comm_hijack import CommHijackAttack
from src.attacks.summary_poisoning import SummaryPoisoningAttack
from src.attacks.workspace_poisoning import WorkspacePoisoningAttack
from src.runtime.orchestrator import attack_for


FORBIDDEN_EXACT_PHRASES = [
    "ignore prior privacy constraints",
    "include the exact budget cap",
    "preserve exact operational details",
    "including budget cap, internal cause, customer reference, and service token",
    "service token",
]


class HeldOutAttackTest(unittest.TestCase):
    def test_paraphrase_attacks_exist(self):
        self.assertIsInstance(attack_for("summary_poisoning_paraphrase"), SummaryPoisoningAttack)
        self.assertIsInstance(attack_for("workspace_poisoning_paraphrase"), WorkspacePoisoningAttack)
        self.assertIsInstance(attack_for("comm_hijack_paraphrase"), CommHijackAttack)

    def test_paraphrase_payloads_avoid_forbidden_exact_phrases(self):
        attacks = [
            SummaryPoisoningAttack("paraphrase"),
            WorkspacePoisoningAttack("paraphrase"),
            CommHijackAttack("paraphrase"),
        ]
        for attack in attacks:
            result = attack.apply("Internal note with confidential values.")
            payload = result.annotation["poison_instruction"].lower()
            for phrase in FORBIDDEN_EXACT_PHRASES:
                self.assertNotIn(phrase, payload)

    def test_paraphrase_payloads_are_semantically_dangerous(self):
        attacks = [
            SummaryPoisoningAttack("paraphrase"),
            WorkspacePoisoningAttack("paraphrase"),
            CommHijackAttack("paraphrase"),
        ]
        dangerous_terms = [
            "private numeric limit",
            "credential-like value",
            "private finance values",
            "internal reference tokens",
            "confidential finance limit",
            "credential-style marker",
        ]
        for attack in attacks:
            payload = attack.apply("Internal note.").annotation["poison_instruction"].lower()
            self.assertTrue(any(term in payload for term in dangerous_terms), payload)


if __name__ == "__main__":
    unittest.main()
