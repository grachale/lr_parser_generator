from src.items.item import Item


class LR1Item(Item):
    """Represents an LR(1) item used in parsing algorithms.

    An LR(1) item extends an LR(0) item by including a set of lookahead symbols.
    It is used in LR(1) and LALR(1) parsers to determine reductions based on the current
    input symbol, in addition to the position of the dot in the right-hand side (RHS).

    Attributes:
        lhs (str): The left-hand side (non-terminal) of the production.
        rhs (List[str]): The right-hand side of the production, represented as a list of symbols.
        dot_position (int): The position of the dot (`•`) in the RHS, indicating how much of the production
            has been processed.
        lookaheads (Set[str]): A set of lookahead symbols that determine when this item can be reduced.

    Methods:
        __eq__(other):
            Checks if two LR(1) items are equal based on their `lhs`, `rhs`, `dot_position`, and `lookaheads`.
        __hash__():
            Generates a hash value for the LR(1) item, allowing it to be used in sets and dictionaries.
        __repr__():
            Returns a string representation of the LR(1) item, showing the dot in the appropriate position
            and the set of lookahead symbols.
    """

    def __init__(self, lhs, rhs, dot_position=0, lookaheads=None):
        """Initializes an LR(1) item with the given left-hand side, right-hand side,
        dot position, and lookahead symbols.

        Args:
            lhs (str): The left-hand side (non-terminal) of the production.
            rhs (List[str]): The right-hand side of the production.
            dot_position (int, optional): The position of the dot in the RHS. Defaults to 0.
            lookaheads (Set[str], optional): A set of lookahead symbols. Defaults to an empty set.
        """
        super().__init__(lhs, rhs, dot_position)
        self.lookaheads = set(lookaheads) if lookaheads else set()

    def __eq__(self, other):
        """Checks if this LR(1) item is equal to another LR(1) item.

        Args:
            other (LR1Item): The other LR(1) item to compare with.

        Returns:
            bool: True if both items have the same `lhs`, `rhs`, `dot_position`, and `lookaheads`; False otherwise.
        """
        return (super().__eq__(other) and
                self.lookaheads == other.lookaheads)

    def __hash__(self):
        """Generates a hash value for the LR(1) item.

        The hash value is computed based on the `lhs`, `rhs`, `dot_position`, and sorted `lookaheads`.

        Returns:
            int: The hash value for the LR(1) item.
        """
        return hash((self.lhs, tuple(self.rhs), self.dot_position, tuple(sorted(self.lookaheads))))

    def __repr__(self):
        """Generates a string representation of the LR(1) item.

        The representation includes the `lhs`, the `rhs` with the dot (`•`) inserted at the `dot_position`,
        and the set of lookahead symbols.

        Returns:
            str: A string representation of the LR(1) item, e.g., "A -> • B C, {a, b}".
        """
        rhs_with_dot = self.rhs[:]
        rhs_with_dot.insert(self.dot_position, '•')
        la = ','.join(self.lookaheads)
        return f"{self.lhs} -> {' '.join(rhs_with_dot)}, {{{la}}}"
