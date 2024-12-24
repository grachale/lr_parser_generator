import unittest
from src.parsers.lalr1_parser import LALR1Parser
from src.items.lr1_item import LR1Item
from src.grammars.context_free_grammar import ContextFreeGrammar


class TestLALR1Parser(unittest.TestCase):

    def setUp(self):
        """Set up the grammar for LALR(1) parser testing."""
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
        self.parser = LALR1Parser(context_free_grammar=self.grammar)

    def test_merge_states(self):
        """Test merging of states with identical LR(0) cores."""
        self.parser.items()
        initial_state_count = len(self.parser.C)
        self.parser.merge_states()
        merged_state_count = len(self.parser.C)

        # Ensure states are merged, reducing the total count
        self.assertLess(merged_state_count, initial_state_count)

    def test_items(self):
        """Test the construction of the canonical collection of LALR(1) items."""
        self.parser.items()
        self.parser.construct_parsing_table()

        # Check initial merged state set
        initial_item_set = self.parser.C[0]
        self.assertIn(
            LR1Item("S'", ["S"], 0, {'$'}),
            initial_item_set
        )

    def test_parse_valid_input(self):
        """Test parsing a valid input string using the LALR(1) parser."""
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
