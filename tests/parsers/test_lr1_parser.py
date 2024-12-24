import unittest
from src.items.lr1_item import LR1Item
from src.parsers.lr1_parser import LR1Parser
from src.grammars.context_free_grammar import ContextFreeGrammar


class TestLR1Parser(unittest.TestCase):

    def setUp(self):
        """Set up the grammar for LR(1) parser testing."""
        terminals = ["a", "+", "(", ")"]
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
        self.parser = LR1Parser(context_free_grammar=self.grammar)

    def test_items(self):
        """Test the construction of the canonical collection of LR(1) items."""
        self.parser.items()

        self.assertGreater(len(self.parser.C), 0)

        # Check initial item set
        initial_item_set = self.parser.C[0]
        self.assertIn(LR1Item("S'", ["S"], 0, {'$'}), initial_item_set)

    def test_parse_valid_input(self):
        """Test parsing a valid input string using the LR(1) parser."""
        self.parser.items()
        self.parser.construct_parsing_table()
        configurations = self.parser.parse(["a", "+", "a"])
        self.assertGreater(len(configurations), 0)
        self.assertEqual(configurations[-1][2], ('accept',))

    def test_parse_invalid_input(self):
        """Test parsing an invalid input string."""
        self.parser.items()
        self.parser.construct_parsing_table()
        configurations = self.parser.parse(["a", "+"])
        self.assertIsNone(configurations)


if __name__ == "__main__":
    unittest.main()
