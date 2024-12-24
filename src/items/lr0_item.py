class LR0Item:
    """Represents an LR(0) item used in parsing algorithms.

    An LR(0) item is a construct used in LR parsers (LR(0), SLR(1), LALR(1), LR(1)) to represent
    a production rule along with a dot (`•`) that indicates the current position in the right-hand side (RHS)
    of the production.

    Attributes:
        lhs (str): The left-hand side (non-terminal) of the production.
        rhs (List[str]): The right-hand side of the production, represented as a list of symbols.
        dot_position (int): The position of the dot (`•`) in the RHS, indicating how much of the production
            has been processed. The dot starts at position 0 by default.

    Methods:
        __eq__(other):
            Checks if two items are equal based on their `lhs`, `rhs`, and `dot_position`.
        __hash__():
            Generates a hash value for the item, allowing it to be used in sets and dictionaries.
        __repr__():
            Returns a string representation of the item, showing the dot in the appropriate position.
    """

    def __init__(self, lhs, rhs, dot_position=0):
        """Initializes an Item with the given left-hand side, right-hand side, and dot position.

        Args:
            lhs (str): The left-hand side (non-terminal) of the production.
            rhs (List[str]): The right-hand side of the production.
            dot_position (int, optional): The position of the dot in the RHS. Defaults to 0.
        """
        self.lhs = lhs
        self.rhs = rhs
        self.dot_position = dot_position

    def __eq__(self, other):
        """Checks if this item is equal to another item.

        Args:
            other (LR0Item): The other item to compare with.

        Returns:
            bool: True if both items have the same `lhs`, `rhs`, and `dot_position`; False otherwise.
        """
        return (self.lhs == other.lhs and
                self.rhs == other.rhs and
                self.dot_position == other.dot_position)

    def __hash__(self):
        """Generates a hash value for the item.

        Returns:
            int: The hash value computed based on `lhs`, `rhs`, and `dot_position`.
        """
        return hash((self.lhs, tuple(self.rhs), self.dot_position))

    def __repr__(self):
        """Generates a string representation of the item.

        The representation includes the `lhs`, the `rhs` with the dot (`•`) inserted at the `dot_position`.

        Returns:
            str: A string representation of the item, e.g., "A -> • B C".
        """
        rhs_with_dot = self.rhs[:]
        rhs_with_dot.insert(self.dot_position, '•')
        return f"{self.lhs} -> {' '.join(rhs_with_dot)}"
