import unittest
from src.items.lr0_item import LR0Item


class TestLR0Item(unittest.TestCase):

    def test_initialization(self):
        """Test the initialization of an LR0Item."""
        item = LR0Item(lhs="A", rhs=["B", "C"], dot_position=1)
        self.assertEqual(item.lhs, "A")
        self.assertEqual(item.rhs, ["B", "C"])
        self.assertEqual(item.dot_position, 1)

    def test_default_dot_position(self):
        """Test that the dot position defaults to 0."""
        item = LR0Item(lhs="A", rhs=["B", "C"])
        self.assertEqual(item.dot_position, 0)

    def test_equality(self):
        """Test equality of two LR0Items."""
        item1 = LR0Item(lhs="A", rhs=["B", "C"], dot_position=1)
        item2 = LR0Item(lhs="A", rhs=["B", "C"], dot_position=1)
        item3 = LR0Item(lhs="A", rhs=["B", "D"], dot_position=1)
        self.assertEqual(item1, item2)
        self.assertNotEqual(item1, item3)

    def test_hash(self):
        """Test the hash implementation."""
        item1 = LR0Item(lhs="A", rhs=["B", "C"], dot_position=1)
        item2 = LR0Item(lhs="A", rhs=["B", "C"], dot_position=1)
        item3 = LR0Item(lhs="A", rhs=["B", "D"], dot_position=1)
        self.assertEqual(hash(item1), hash(item2))
        self.assertNotEqual(hash(item1), hash(item3))

    def test_repr(self):
        """Test the string representation of an LR0Item."""
        item = LR0Item(lhs="A", rhs=["B", "C"], dot_position=1)
        self.assertEqual(repr(item), "A -> B • C")

        item = LR0Item(lhs="A", rhs=["B", "C"], dot_position=2)
        self.assertEqual(repr(item), "A -> B C •")

    def test_empty_rhs(self):
        """Test an LR0Item with an empty RHS."""
        item = LR0Item(lhs="A", rhs=[], dot_position=0)
        self.assertEqual(repr(item), "A -> •")
        self.assertEqual(hash(item), hash(("A", (), 0)))


if __name__ == "__main__":
    unittest.main()
