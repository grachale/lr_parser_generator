# GLOBAL IMPORTS
from src.parsers.lr0_parser import LR0Parser


class SLR1Parser(LR0Parser):
    """Implements the SLR(1) parser for constructing parsing tables and parsing input strings.

    The SLR(1) parser extends the LR(0) parser by using FOLLOW sets to resolve reduce actions.
    It uses the canonical collection of LR(0) items and computes FOLLOW sets for non-terminals
    to construct the ACTION and GOTO tables.

    Attributes:
        grammar (ContextFreeGrammar): The context-free grammar used by the parser.
        action (dict): The ACTION table used in SLR(1) parsing, mapping (state, symbol) pairs to actions.
        goto_table (dict): The GOTO table used in SLR(1) parsing, mapping (state, non-terminal) pairs to states.
        states (dict): A dictionary mapping item sets to state numbers.
        transitions (dict): A dictionary storing state transitions for the parser.
        C (list): The canonical collection of item sets used in constructing the parsing tables.

    Methods:
        construct_parsing_table():
            Constructs the ACTION and GOTO tables for the SLR(1) parser, resolving reduce actions using FOLLOW sets.
    """

    def __init__(self, context_free_grammar):
        """Initializes the SLRParser with a context-free grammar.

        This method computes the FOLLOW sets for all non-terminals in the grammar and
        initializes the data structures for the ACTION and GOTO tables.

        Args:
            context_free_grammar (ContextFreeGrammar): The context-free grammar to be used by the parser.
        """
        super().__init__(context_free_grammar)
        self.grammar.compute_follow()

    def construct_parsing_table(self):
        """Constructs the ACTION and GOTO tables for the SLR(1) parser.

        The ACTION table maps (state, terminal) pairs to parser actions (shift, reduce, or accept).
        Reduce actions are determined using FOLLOW sets for the corresponding non-terminal.

        Raises:
            ValueError: If there is a conflict during the construction of the parsing tables.
        """
        # Construct ACTION table
        for I in self.C:
            state_no = self.states[frozenset(I)]
            for item in I:
                # Shift action
                if item.dot_position < len(item.rhs):
                    symbol = item.rhs[item.dot_position]
                    if symbol in self.grammar.terminals:
                        next_state = self.transitions.get((state_no, symbol))
                        if next_state is not None:
                            action_key = (state_no, symbol)
                            action_value = ('shift', next_state)
                            if action_key in self.action and self.action[action_key] != action_value:
                                print(f"Conflict at state {state_no}, symbol {symbol}")
                            self.action[action_key] = action_value
                # Reduce or Accept action
                else:
                    # Accept action
                    if item.lhs == self.grammar.augmented_start_symbol:
                        self.action[(state_no, '$')] = ('accept',)
                    # Reduce action
                    else:
                        for follow_symbol in self.grammar.follow[item.lhs]:
                            action_key = (state_no, follow_symbol)
                            action_value = ('reduce', item.lhs, item.rhs)
                            if action_key in self.action and self.action[action_key] != action_value:
                                print(f"Conflict at state {state_no}, symbol {follow_symbol}")
                            self.action[action_key] = action_value
            # Construct GOTO table
            for A in self.grammar.non_terminals:
                next_state = self.transitions.get((state_no, A))
                if next_state is not None:
                    self.goto_table[(state_no, A)] = next_state
