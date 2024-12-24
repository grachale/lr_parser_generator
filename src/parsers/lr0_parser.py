# GLOBAL IMPORTS
from collections import deque

# LOCAL IMPORTS
from src.items.lr0_item import LR0Item
from src.parsers.lr_parser import LRParser


class LR0Parser(LRParser):
    """Implements the LR(0) parser for constructing parsing tables and parsing input strings.

    The LR(0) parser builds the canonical collection of LR(0) items, constructs the ACTION
    and GOTO tables, and uses them to parse input strings. It is a subclass of the abstract
    `LRParser` class and implements methods specific to LR(0) parsing.

    Attributes:
        grammar (ContextFreeGrammar): The context-free grammar used by the parser.
        action (dict): The ACTION table used in LR(0) parsing, mapping (state, symbol) pairs to actions.
        goto_table (dict): The GOTO table used in LR(0) parsing, mapping (state, non-terminal) pairs to states.
        states (dict): A dictionary mapping item sets to state numbers.
        transitions (dict): A dictionary storing state transitions for the parser.
        C (list): The canonical collection of item sets used in constructing the parsing tables.

    Methods:
        items():
            Constructs the canonical collection of LR(0) items.
        closure(items):
            Computes the closure of a set of LR(0) items.
        goto(items, symbol):
            Computes the GOTO set for a given set of LR(0) items and a grammar symbol.
        construct_parsing_table():
            Constructs the ACTION and GOTO tables for the LR(0) parser.
    """

    def items(self):
        """Constructs the canonical collection of LR(0) items.

        The canonical collection is built using the closure and goto operations. Each set of
        items corresponds to a state in the parsing table.

        Raises:
            ValueError: If there is a conflict during the construction of the canonical collection.
        """
        initial_item = LR0Item(self.grammar.augmented_start_symbol, [self.grammar.start_symbol], 0)
        I0 = self.closure(set([initial_item]))
        self.C.append(I0)
        self.states[frozenset(I0)] = 0
        queue = deque([I0])

        while queue:
            I = queue.popleft()
            state_no = self.states[frozenset(I)]
            symbols = set()
            for item in I:
                if item.dot_position < len(item.rhs):
                    symbols.add(item.rhs[item.dot_position])
            for X in symbols:
                goto_I_X = self.goto(I, X)
                if goto_I_X:
                    goto_I_X_frozenset = frozenset(goto_I_X)
                    if goto_I_X_frozenset not in self.states:
                        self.states[goto_I_X_frozenset] = len(self.C)
                        self.C.append(goto_I_X)
                        queue.append(goto_I_X)
                    self.transitions[(state_no, X)] = self.states[goto_I_X_frozenset]

    def closure(self, items):
        """Computes the closure of a set of LR(0) items.

        The closure of a set of items includes all items that can be derived from the grammar
        based on the current position of the dot.

        Args:
            items (Set[Item]): A set of LR(0) items.

        Returns:
            Set[Item]: The closure of the input set of items.
        """
        closure_set = set(items)
        added = True
        while added:
            added = False
            new_items = set()
            for item in closure_set:
                if item.dot_position < len(item.rhs):
                    symbol = item.rhs[item.dot_position]
                    if symbol in self.grammar.non_terminals:
                        for prod in self.grammar.productions:
                            if prod[0] == symbol:
                                new_item = LR0Item(prod[0], prod[1], 0)
                                if new_item not in closure_set:
                                    new_items.add(new_item)
                                    added = True
            closure_set.update(new_items)
        return closure_set

    def goto(self, items, symbol):
        """Computes the GOTO set for a set of LR(0) items and a grammar symbol.

        Args:
            items (Set[Item]): A set of LR(0) items.
            symbol (str): The grammar symbol for which to compute the GOTO set.

        Returns:
            Set[Item]: The GOTO set for the given items and symbol.
        """
        goto_set = set()
        for item in items:
            if item.dot_position < len(item.rhs) and item.rhs[item.dot_position] == symbol:
                new_item = LR0Item(item.lhs, item.rhs, item.dot_position + 1)
                goto_set.add(new_item)
        return self.closure(goto_set)

    def construct_parsing_table(self):
        """Constructs the ACTION and GOTO tables for the LR(0) parser.

        The ACTION table maps (state, terminal) pairs to parser actions (shift, reduce, or accept).
        The GOTO table maps (state, non-terminal) pairs to new states.

        Raises:
            ValueError: If there is a conflict during the construction of the parsing tables.
        """
        for I in self.C:
            state_no = self.states[frozenset(I)]
            # Construct ACTION table
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
                        for term_symbol in self.grammar.terminals:
                            action_key = (state_no, term_symbol)
                            action_value = ('reduce', item.lhs, item.rhs)
                            if action_key in self.action and self.action[action_key] != action_value:
                                print(f"Conflict at state {state_no}, symbol {term_symbol}")
                            self.action[action_key] = action_value
            # Construct GOTO table
            for A in self.grammar.non_terminals:
                next_state = self.transitions.get((state_no, A))
                if next_state is not None:
                    self.goto_table[(state_no, A)] = next_state
