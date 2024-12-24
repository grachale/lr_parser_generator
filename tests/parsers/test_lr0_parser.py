import unittest
from src.items.lr0_item import LR0Item
from src.parsers.lr0_parser import LR0Parser
from src.grammars.context_free_grammar import ContextFreeGrammar


class TestLR0Parser(unittest.TestCase):

    def setUp(self):
        """Set up a real context-free grammar for testing."""
        terminals = ["a", "b"]
        non_terminals = ["S", "A"]
        productions = [
            ("S'", ["S"]),
            ("S", ["A", "b"]),
            ("A", ["a"]),
        ]
        start_symbol = "S"  # Define the start symbol of the grammar
        self.grammar = ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)
        self.grammar.augment_grammar()
        self.grammar.compute_first()
        self.parser = LR0Parser(context_free_grammar=self.grammar)

    def test_closure(self):
        """Test the closure computation for a set of LR(0) items."""
        items = {LR0Item("S'", ["S"], 0)}
        closure_result = self.parser.closure(items)

        expected_items = {
            LR0Item("S'", ["S"], 0),
            LR0Item("S", ["A", "b"], 0),
            LR0Item("A", ["a"], 0),
        }
        self.assertEqual(closure_result, expected_items)

    def test_goto(self):
        """Test the GOTO computation for a set of LR(0) items and a symbol."""
        items = {
            LR0Item("S'", ["S"], 0),
            LR0Item("S", ["A", "b"], 0),
            LR0Item("A", ["a"], 0),
        }
        closure_result = self.parser.closure(items)
        goto_result = self.parser.goto(closure_result, "a")

        expected_items = {
            LR0Item("A", ["a"], 1),
        }
        self.assertEqual(goto_result, expected_items)

    def test_items(self):
        """Test the construction of the canonical collection of LR(0) items."""
        self.parser.items()

        # Check the canonical collection (C)
        self.assertGreater(len(self.parser.C), 0)
        self.assertIn(
            LR0Item("S'", ["S"], 0),
            self.parser.C[0],
        )

    def test_construct_parsing_table(self):
        """Test the construction of ACTION and GOTO tables."""
        self.parser.items()
        self.parser.construct_parsing_table()

        # Check GOTO table
        self.assertIn((0, "A"), self.parser.goto_table)


if __name__ == "__main__":
    unittest.main()
