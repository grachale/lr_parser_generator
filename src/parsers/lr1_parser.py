# GLOBAL IMPORTS
from collections import deque

# LOCAL IMPORTS
from src.items.lr1_item import LR1Item
from src.parsers.lr_parser import LRParser


class LR1Parser(LRParser):
    """Implements the LR(1) parser for constructing parsing tables and parsing input strings.

    The LR(1) parser uses LR(1) items, which include lookaheads to resolve reduce actions more precisely.
    This parser constructs the canonical collection of LR(1) items, the ACTION and GOTO tables,
    and parses input strings based on these tables.

    Attributes:
        grammar (ContextFreeGrammar): The context-free grammar used by the parser.
        action (dict): The ACTION table used in LR(1) parsing, mapping (state, terminal) pairs to actions.
        goto_table (dict): The GOTO table used in LR(1) parsing, mapping (state, non-terminal) pairs to states.
        states (dict): A dictionary mapping item sets to state numbers.
        transitions (dict): A dictionary storing state transitions for the parser.
        C (list): The canonical collection of LR(1) item sets used in constructing the parsing tables.

    Methods:
        items():
            Constructs the canonical collection of LR(1) items.
        closure(items):
            Computes the closure of a set of LR(1) items, including propagating lookaheads.
        compute_lookaheads(item):
            Computes the lookahead set for a given LR(1) item.
        compute_first_sequence(symbols):
            Computes the FIRST set for a sequence of grammar symbols.
        goto(items, symbol):
            Computes the GOTO set for a set of LR(1) items and a grammar symbol.
        construct_parsing_table():
            Constructs the ACTION and GOTO tables for the LR(1) parser.
    """

    def items(self):
        """Constructs the canonical collection of LR(1) items.

        The canonical collection is built using the closure and goto operations.
        Each set of items corresponds to a state in the parsing table. LR(1) items
        include lookahead sets to determine valid reductions.

        Raises:
            ValueError: If there is a conflict during the construction of the canonical collection.
        """
        initial_item = LR1Item(self.grammar.augmented_start_symbol, [self.grammar.start_symbol], 0, ['$'])
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
        """Computes the closure of a set of LR(1) items.

        The closure includes all items derivable from the grammar for the current dot position,
        while propagating lookahead sets to relevant items.

        Args:
            items (Set[LR1Item]): A set of LR(1) items.

        Returns:
            Set[LR1Item]: The closure of the input set of items.
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
                        lookaheads = self.compute_lookaheads(item)
                        for prod in self.grammar.productions:
                            if prod[0] == symbol:
                                new_item = LR1Item(prod[0], prod[1], 0, lookaheads)
                                if new_item not in closure_set:
                                    new_items.add(new_item)
                                    added = True
                                else:
                                    # Merge lookaheads
                                    for existing_item in closure_set:
                                        if existing_item == new_item:
                                            if not lookaheads.issubset(existing_item.lookaheads):
                                                existing_item.lookaheads.update(lookaheads)
                                                added = True
            closure_set.update(new_items)
        return closure_set

    def compute_lookaheads(self, item):
        """Computes the lookahead set for a given LR(1) item.

        The lookahead set is derived from the symbols following the current dot position
        and the item's existing lookaheads.

        Args:
            item (LR1Item): The LR(1) item for which to compute lookaheads.

        Returns:
            Set[str]: The lookahead set for the item.
        """
        beta = item.rhs[item.dot_position + 1:]
        lookaheads = item.lookaheads
        first_beta = self.compute_first_sequence(beta)
        if 'ε' in first_beta:
            first_beta.remove('ε')
            first_beta.update(lookaheads)
        return first_beta

    def compute_first_sequence(self, symbols):
        """Computes the FIRST set for a sequence of grammar symbols.

        Args:
            symbols (List[str]): A list of grammar symbols.

        Returns:
            Set[str]: The FIRST set for the sequence.
        """
        first = set()
        if not symbols:
            first.add('ε')
        else:
            for symbol in symbols:
                first.update(self.grammar.first[symbol] - {'ε'})
                if 'ε' not in self.grammar.first[symbol]:
                    break
            else:
                first.add('ε')
        return first

    def goto(self, items, symbol):
        """Computes the GOTO set for a set of LR(1) items and a grammar symbol.

        Args:
            items (Set[LR1Item]): A set of LR(1) items.
            symbol (str): The grammar symbol for which to compute the GOTO set.

        Returns:
            Set[LR1Item]: The GOTO set for the given items and symbol.
        """
        goto_set = set()
        for item in items:
            if item.dot_position < len(item.rhs) and item.rhs[item.dot_position] == symbol:
                new_item = LR1Item(item.lhs, item.rhs, item.dot_position + 1, item.lookaheads)
                goto_set.add(new_item)
        return self.closure(goto_set)

    def construct_parsing_table(self):
        """Constructs the ACTION and GOTO tables for the LR(1) parser.

        The ACTION table maps (state, terminal) pairs to parser actions (shift, reduce, or accept).
        The GOTO table maps (state, non-terminal) pairs to new states.

        Raises:
            ValueError: If there is a conflict during the construction of the parsing tables.
        """
        for I in self.C:
            state_no = self.states[frozenset(I)]
            # Construct ACTION table
            for item in I:
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
                else:
                    if item.lhs == self.grammar.augmented_start_symbol:
                        self.action[(state_no, '$')] = ('accept',)
                    else:
                        for a in item.lookaheads:
                            action_key = (state_no, a)
                            action_value = ('reduce', item.lhs, item.rhs)
                            if action_key in self.action and self.action[action_key] != action_value:
                                print(f"Conflict at state {state_no}, symbol {a}")
                            self.action[action_key] = action_value
            # Construct GOTO table
            for A in self.grammar.non_terminals:
                next_state = self.transitions.get((state_no, A))
                if next_state is not None:
                    self.goto_table[(state_no, A)] = next_state
