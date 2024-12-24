import unittest
from unittest.mock import Mock
from src.parsers.lr_parser import LRParser


class TestLRParser(unittest.TestCase):

    def setUp(self):
        """Set up a mock context-free grammar for testing."""
        self.mock_grammar = Mock()
        self.mock_grammar.augment_grammar = Mock()
        self.mock_grammar.compute_first = Mock()

    def test_initialization(self):
        """Test that LRParser initializes properly and calls augment_grammar and compute_first."""

        class ConcreteLRParser(LRParser):
            def items(self):
                pass

            def construct_parsing_table(self):
                pass

        parser = ConcreteLRParser(context_free_grammar=self.mock_grammar)

        # Ensure grammar augmentation and FIRST set computation were called
        self.mock_grammar.augment_grammar.assert_called_once()
        self.mock_grammar.compute_first.assert_called_once()

        # Check initial attributes
        self.assertEqual(parser.grammar, self.mock_grammar)
        self.assertEqual(parser.action, {})
        self.assertEqual(parser.goto_table, {})
        self.assertEqual(parser.states, {})
        self.assertEqual(parser.transitions, {})
        self.assertEqual(parser.C, [])

    def test_parse_method(self):
        """Test the parse method with a simple mocked parser setup."""

        class ConcreteLRParser(LRParser):
            def items(self):
                pass

            def construct_parsing_table(self):
                pass

        parser = ConcreteLRParser(context_free_grammar=self.mock_grammar)
        parser.action = {
            (0, 'a'): ('shift', 1),
            (1, '$'): ('accept',)
        }
        parser.goto_table = {}

        configurations = parser.parse(['a'])

        # Validate the parsing configurations
        self.assertEqual(len(configurations), 2)

        # First configuration
        self.assertEqual(configurations[0], ([0], ['a', '$'], ('shift', 1)))

        # Second configuration
        self.assertEqual(configurations[1], ([0, 1], ['$'], ('accept',)))

    def test_parse_complex_grammar(self):
        """Test the parse method with a more complex grammar setup."""

        class ConcreteLRParser(LRParser):
            def items(self):
                pass

            def construct_parsing_table(self):
                pass

        parser = ConcreteLRParser(context_free_grammar=self.mock_grammar)
        parser.action = {
            (0, 'id'): ('shift', 1),
            (1, '+'): ('shift', 2),
            (2, 'id'): ('shift', 3),
            (3, '$'): ('reduce', 'E', ['id', '+', 'id']),
            (4, '$'): ('accept',),
        }
        parser.goto_table = {
            (0, 'E'): 4
        }

        configurations = parser.parse(['id', '+', 'id'])

        # Validate the parsing configurations
        self.assertEqual(len(configurations), 5)

        # First configuration
        self.assertEqual(configurations[0], ([0], ['id', '+', 'id', '$'], ('shift', 1)))

        # Second configuration
        self.assertEqual(configurations[1], ([0, 1], ['+', 'id', '$'], ('shift', 2)))

        # Third configuration
        self.assertEqual(configurations[2], ([0, 1, 2], ['id', '$'], ('shift', 3)))

        # Fourth configuration
        self.assertEqual(configurations[3], ([0, 1, 2, 3], ['$'], ('reduce', 'E', ['id', '+', 'id'])))

        # Fifth configuration (acceptance)
        self.assertEqual(configurations[4], ([0, 4], ['$'], ('accept',)))


if __name__ == "__main__":
    unittest.main()
