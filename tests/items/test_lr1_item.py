import unittest
from src.items.lr0_item import LR0Item
from src.items.lr1_item import LR1Item

class TestLR1Item(unittest.TestCase):

    def test_initialization(self):
        """Test the initialization of an LR1Item."""
        item = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"a", "b"})
        self.assertEqual(item.lhs, "A")
        self.assertEqual(item.rhs, ["B", "C"])
        self.assertEqual(item.dot_position, 1)
        self.assertEqual(item.lookaheads, {"a", "b"})

    def test_default_lookaheads(self):
        """Test that the lookaheads default to an empty set."""
        item = LR1Item(lhs="A", rhs=["B", "C"])
        self.assertEqual(item.lookaheads, set())

    def test_equality(self):
        """Test equality of two LR1Items."""
        item1 = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"a", "b"})
        item2 = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"b", "a"})
        item3 = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"c"})
        self.assertEqual(item1, item2)
        self.assertNotEqual(item1, item3)

    def test_hash(self):
        """Test the hash implementation."""
        item1 = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"a", "b"})
        item2 = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"b", "a"})
        item3 = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"c"})
        self.assertEqual(hash(item1), hash(item2))
        self.assertNotEqual(hash(item1), hash(item3))

    def test_repr(self):
        """Test the string representation of an LR1Item."""
        item = LR1Item(lhs="A", rhs=["B", "C"], dot_position=1, lookaheads={"a", "b"})
        repr_result = repr(item)
        # Check basic structure of representation
        self.assertTrue(repr_result.startswith("A -> B • C"))
        self.assertIn("{a,b}".strip(), repr_result.replace(" ", ""))

    def test_empty_rhs_and_lookaheads(self):
        """Test an LR1Item with an empty RHS and no lookaheads."""
        item = LR1Item(lhs="A", rhs=[], dot_position=0, lookaheads=set())
        self.assertEqual(repr(item), "A -> •, {}")
        self.assertEqual(hash(item), hash(("A", (), 0, ())))

if __name__ == "__main__":
    unittest.main()
