import unittest
from src.grammars.grammar import Grammar


class TestGrammar(unittest.TestCase):

    def setUp(self):
        """Set up a sample grammar for testing."""
        self.terminals = ['a', 'b']
        self.non_terminals = ['S', 'A']
        self.productions = [
            ('S', ['A', 'b']),
            ('A', ['a'])
        ]
        self.start_symbol = 'S'
        self.grammar = Grammar(self.terminals, self.non_terminals, self.productions, self.start_symbol)

    def test_initialization(self):
        """Test if the grammar initializes correctly."""
        self.assertEqual(self.grammar.terminals, self.terminals)
        self.assertEqual(self.grammar.non_terminals, self.non_terminals)
        self.assertEqual(self.grammar.productions, self.productions)
        self.assertEqual(self.grammar.start_symbol, self.start_symbol)
        self.assertIsNone(self.grammar.augmented_start_symbol)
        self.assertIsNone(self.grammar.production_numbers)

    def test_augment_grammar(self):
        """Test augmenting the grammar."""
        self.grammar.augment_grammar()
        expected_augmented_start_symbol = "S'"
        self.assertEqual(self.grammar.augmented_start_symbol, expected_augmented_start_symbol)
        self.assertIn((expected_augmented_start_symbol, [self.start_symbol]), self.grammar.productions)
        self.assertIn(expected_augmented_start_symbol, self.grammar.non_terminals)

    def test_number_productions(self):
        """Test assigning unique numbers to productions."""
        self.grammar.augment_grammar()
        self.grammar.number_productions()
        self.assertIsNotNone(self.grammar.production_numbers)
        self.assertEqual(len(self.grammar.production_numbers), len(self.grammar.productions))
        for idx, prod in enumerate(self.grammar.productions):
            self.assertEqual(self.grammar.production_numbers[(prod[0], tuple(prod[1]))], idx)

    def test_get_production_number(self):
        """Test getting the production number for a given production."""
        self.grammar.augment_grammar()
        prod_to_test = ('S', ['A', 'b'])
        prod_number = self.grammar.get_production_number(prod_to_test)
        self.assertIsNotNone(prod_number)
        self.assertEqual(prod_number, self.grammar.production_numbers[(prod_to_test[0], tuple(prod_to_test[1]))])

    def test_invalid_production_number(self):
        """Test getting a production number for an invalid production."""
        self.grammar.augment_grammar()
        invalid_prod = ('B', ['a', 'b'])  # Not in the grammar
        self.assertIsNone(self.grammar.get_production_number(invalid_prod))


if __name__ == '__main__':
    unittest.main()
