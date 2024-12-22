import unittest
from src.grammars.context_free_grammar import ContextFreeGrammar


class TestContextFreeGrammar(unittest.TestCase):

    def setUp(self):
        """Set up reusable grammars for testing."""
        # Simple grammar
        self.simple_productions = [
            ('S', ['A', 'b']),
            ('A', ['a']),
            ('A', ['ε'])
        ]
        self.simple_grammar = ContextFreeGrammar(['a', 'b'], ['S', 'A'], self.simple_productions, 'S')

        # Complex grammar
        self.complex_productions = [
            ('S', ['A', 'a']),
            ('S', ['b', 'S']),
            ('A', ['c', 'A', 'd']),
            ('A', ['B']),
            ('B', ['f', 'S']),
            ('B', ['ε']),
        ]
        self.complex_grammar = ContextFreeGrammar(['a', 'b', 'c', 'f'], ['S', 'A', 'B'], self.complex_productions, 'S')

        # Arithmetic expression grammar
        self.arithmetic_productions = [
            ('E', ['T', 'E2']),
            ('E2', ['+', 'T', 'E2']),
            ('E2', ['ε']),
            ('T', ['F', 'T2']),
            ('T2', ['*', 'F', 'T2']),
            ('T2', ['ε']),
            ('F', ['(', 'E', ')']),
            ('F', ['id']),
        ]
        self.arithmetic_grammar = ContextFreeGrammar(
            ['+', '*', '(', ')', 'id'],
            ['E', 'E2', 'T', 'T2', 'F'],
            self.arithmetic_productions,
            'E'
        )

    def test_compute_first_augmented(self):
        """Test computing FIRST set for a simple augmented grammar."""
        self.simple_grammar.augment_grammar()
        self.simple_grammar.compute_first()

        expected_first = {
            "S'": {'a', 'b'},
            'S': {'a', 'b'},
            'A': {'a', 'ε'},
            'a': {'a'},
            'b': {'b'},
        }

        self.assertEqual(self.simple_grammar.first, expected_first)

    def test_compute_first_non_augmented(self):
        """Test computing FIRST set for a complex grammar without augmentation."""
        self.complex_grammar.compute_first()

        expected_first = {
            'S': {'a', 'b', 'c', 'f'},
            'A': {'f', 'c', 'ε'},
            'B': {'f', 'ε'},
            'a': {'a'},
            'b': {'b'},
            'c': {'c'},
            'f': {'f'}
        }

        self.assertEqual(self.complex_grammar.first, expected_first)

    def test_compute_first_arithmetic_expression(self):
        """Test computing FIRST set for an arithmetic expression grammar."""
        self.arithmetic_grammar.compute_first()

        expected_first = {
            'E': {'(', 'id'},
            'E2': {'+', 'ε'},
            'T': {'(', 'id'},
            'T2': {'*', 'ε'},
            'F': {'id', '('},
            '+': {'+'},
            '*': {'*'},
            '(': {'('},
            ')': {')'},
            'id': {'id'}
        }

        self.assertEqual(self.arithmetic_grammar.first, expected_first)

    def test_compute_follow_arithmetic_expression(self):
        """Test computing FOLLOW set for an arithmetic expression grammar."""
        self.arithmetic_grammar.compute_first()
        self.arithmetic_grammar.compute_follow()

        expected_follow = {
            'E': {')', '$'},
            'E2': {')', '$'},
            'T': {'+', ')', '$'},
            'T2': {'+', ')', '$'},
            'F': {'*', '+', ')', '$'},
        }

        self.assertEqual(self.arithmetic_grammar.follow, expected_follow)

    def test_augment_grammar(self):
        """Test augmentation of a grammar."""
        self.simple_grammar.augment_grammar()

        augmented_productions = [
            ("S'", ['S']),
            ('S', ['A', 'b']),
            ('A', ['a']),
            ('A', ['ε'])
        ]

        self.assertEqual(self.simple_grammar.productions, augmented_productions)
        self.assertEqual(self.simple_grammar.augmented_start_symbol, "S'")
        self.assertIn("S'", self.simple_grammar.non_terminals)


if __name__ == '__main__':
    unittest.main()
