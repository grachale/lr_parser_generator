class Grammar:
    """Represents a general grammar with terminals, non-terminals, productions, and a start symbol.

    Attributes:
        terminals (List[str]): A list of terminal symbols.
        non_terminals (List[str]): A list of non-terminal symbols.
        productions (List[Tuple[str, List[str]]]): A list of production rules, each as a tuple (lhs, rhs).
        start_symbol (str): The start symbol of the grammar.
        augmented_start_symbol (str): The augmented start symbol used in parsing algorithms.
        production_numbers (dict): A dictionary mapping productions to their unique numbers.
    """

    def __init__(self, terminals, non_terminals, productions, start_symbol):
        """Initializes a Grammar with given terminals, non-terminals, productions, and a start symbol.

        Args:
            terminals (List[str]): List of terminal symbols.
            non_terminals (List[str]): List of non-terminal symbols.
            productions (List[Tuple[str, List[str]]]): List of production rules.
            start_symbol (str): The start symbol of the grammar.
        """
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.augmented_start_symbol = None
        self.production_numbers = None

    def augment_grammar(self):
        """Augments the grammar by adding a new start symbol and production.

        The new production is of the form S' -> S, where S is the original start symbol.
        This is done to facilitate LR parsing by providing a clear acceptance state.
        """
        self.augmented_start_symbol = self.start_symbol + "'"
        self.productions.insert(0, (self.augmented_start_symbol, [self.start_symbol]))
        self.non_terminals.insert(0, self.augmented_start_symbol)
        self.number_productions()

    def number_productions(self):
        """Assigns a unique number to each production in the grammar."""
        self.production_numbers = {}
        for idx, prod in enumerate(self.productions):
            # Use tuples for productions to make them hashable
            self.production_numbers[(prod[0], tuple(prod[1]))] = idx

    def get_production_number(self, prod):
        """Gets the production number for a given production.

        Args:
            prod (Tuple[str, List[str]]): The production rule as a tuple (lhs, rhs).

        Returns:
            int: The unique number assigned to the production, or None if not found.
        """
        return self.production_numbers.get((prod[0], tuple(prod[1])))
