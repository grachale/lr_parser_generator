import unittest
from src.parsers.slr1_parser import SLR1Parser
from src.grammars.context_free_grammar import ContextFreeGrammar


class TestGrammarParser(unittest.TestCase):

    def setUp(self):
        """Set up the grammar for the test cases."""
        terminals = ["a", "(", ")", "+"]
        non_terminals = ["S", "E", "T"]
        productions = [
            ("S", ["E"]),
            ("E", ["E", "+", "T"]),
            ("E", ["T"]),
            ("T", ["a"]),
            ("T", ["(", "E", ")"])
        ]
        start_symbol = "S"
        self.grammar = ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)
        self.grammar.augment_grammar()
        self.grammar.compute_first()
        self.grammar.compute_follow()
        self.parser = SLR1Parser(context_free_grammar=self.grammar)

    def test_parse_valid_input(self):
        """Test parsing a valid input string."""
        self.parser.items()
        self.parser.construct_parsing_table()

        configurations = self.parser.parse(["a", "+", "a"])

        # Validate parsing configurations
        self.assertGreater(len(configurations), 0)
        self.assertEqual(configurations[-1][2], ('accept',))  # Ensure input is accepted

    def test_parse_invalid_input(self):
        """Test parsing an invalid input string."""
        self.parser.items()
        self.parser.construct_parsing_table()

        configurations = self.parser.parse(["a", "a"])

        self.assertIsNone(configurations)


if __name__ == "__main__":
    unittest.main()
