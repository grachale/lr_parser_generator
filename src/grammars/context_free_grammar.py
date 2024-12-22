from src.grammars.grammar import Grammar


class ContextFreeGrammar(Grammar):
    """Represents a context-free grammar (CFG) and includes methods for computing FIRST and FOLLOW sets.

    Inherits from the Grammar class.

    Attributes:
        first (dict): Dictionary storing FIRST sets for terminals and non-terminals.
        follow (dict): Dictionary storing FOLLOW sets for non-terminals.
    """

    def __init__(self, terminals, non_terminals, productions, start_symbol):
        """Initializes a ContextFreeGrammar with the given grammar components.

        Args:
            terminals (List[str]): List of terminal symbols.
            non_terminals (List[str]): List of non-terminal symbols.
            productions (List[Tuple[str, List[str]]]): List of production rules.
            start_symbol (str): The start symbol of the grammar.
        """
        super().__init__(terminals, non_terminals, productions, start_symbol)
        self.first = None
        self.follow = None

    def compute_first(self):
        """Computes the FIRST sets for all symbols in the grammar.

        The FIRST set of a symbol is the set of terminals that can appear at the beginning
        of some string derived from that symbol.
        """
        self.first = {symbol: set() for symbol in self.non_terminals + self.terminals}

        # Initialize FIRST sets for terminals
        for terminal in self.terminals:
            self.first[terminal].add(terminal)

        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.productions:
                first_before = self.first[lhs].copy()

                # Compute FIRST(lhs) based on FIRST(rhs)
                if rhs == ['ε']:
                    self.first[lhs].add('ε')
                else:
                    counter_of_epsilon = 0
                    for symbol in rhs:
                        self.first[lhs].update(self.first[symbol] - {'ε'})
                        if 'ε' not in self.first[symbol]:
                            break
                        else:
                            counter_of_epsilon += 1

                    # If all symbols in RHS can derive ε, add ε to FIRST(lhs)
                    if counter_of_epsilon == len(rhs):
                        self.first[lhs].add('ε')

                if first_before != self.first[lhs]:
                    changed = True

    def compute_follow(self):
        """Computes the FOLLOW sets for all non-terminals in the grammar.

        The FOLLOW set of a non-terminal is the set of terminals that can appear immediately
        to the right of that non-terminal in some sentential form.
        """
        self.follow = {symbol: set() for symbol in self.non_terminals}

        # Add end-of-input symbol '$' to FOLLOW(start symbol)
        self.follow[self.start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.productions:
                trailer = self.follow[lhs].copy()
                for symbol in reversed(rhs):
                    if symbol in self.non_terminals:
                        before = self.follow[symbol].copy()
                        self.follow[symbol].update(trailer)

                        if 'ε' in self.first[symbol]:
                            trailer.update(self.first[symbol] - {'ε'})
                        else:
                            trailer = self.first[symbol]

                        if before != self.follow[symbol]:
                            changed = True
                    elif symbol in self.terminals:
                        trailer = self.first[symbol]
