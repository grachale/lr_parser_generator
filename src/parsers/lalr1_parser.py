# GLOBAL IMPORTS
from collections import defaultdict

# LOCAL IMPORTS
from src.items.item import Item
from src.items.lr1_item import LR1Item
from src.parsers.lr1_parser import LR1Parser


class LALR1Parser(LR1Parser):
    """Implements the LALR(1) parser for constructing parsing tables and parsing input strings.

    The LALR(1) parser is a more space-efficient variation of the LR(1) parser. It merges states
    in the canonical collection of LR(1) items that have identical LR(0) cores but different lookaheads.
    This reduces the size of the parsing tables while retaining the power of LR(1) parsing.

    Attributes:
        grammar (ContextFreeGrammar): The context-free grammar used by the parser.
        action (dict): The ACTION table used in LALR(1) parsing, mapping (state, terminal) pairs to actions.
        goto_table (dict): The GOTO table used in LALR(1) parsing, mapping (state, non-terminal) pairs to states.
        states (dict): A dictionary mapping merged item sets to state numbers.
        transitions (dict): A dictionary storing state transitions for the parser.
        C (list): The canonical collection of merged LR(1) item sets used in constructing the parsing tables.

    Methods:
        merge_states():
            Merges states in the canonical collection of LR(1) items that have identical LR(0) cores.
        construct_parsing_table():
            Constructs the ACTION and GOTO tables for the LALR(1) parser.
    """

    def merge_states(self):
        """Merges states with identical LR(0) items but different lookaheads.

        This method reduces the size of the canonical collection by grouping LR(1) item sets
        that share the same LR(0) core (i.e., items without lookaheads). The merged states combine
        the lookaheads from the original states.

        The following updates are made:
        1. States are grouped by their LR(0) cores.
        2. Lookaheads for merged items are computed as the union of the lookaheads from all contributing states.
        3. The state mapping, transitions, and canonical collection (`C`) are updated to reflect the merged states.
        """
        state_groups = defaultdict(list)

        # Group states by their LR(0) core
        for idx, I in enumerate(self.C):
            core = frozenset([Item(item.lhs, item.rhs, item.dot_position) for item in I])
            state_groups[core].append((idx, I))

        new_states = {}
        new_C = []
        state_mapping = {}

        # Merge states in each group
        for core, states in state_groups.items():
            merged_items_dict = {}
            for idx, items in states:
                for item in items:
                    key = (item.lhs, tuple(item.rhs), item.dot_position)
                    if key not in merged_items_dict:
                        merged_items_dict[key] = set()
                    merged_items_dict[key].update(item.lookaheads)

            new_items = set()
            for key, lookaheads in merged_items_dict.items():
                new_items.add(LR1Item(key[0], list(key[1]), key[2], lookaheads))

            state_no = len(new_C)
            for idx, _ in states:
                state_mapping[idx] = state_no

            new_states[frozenset(new_items)] = state_no
            new_C.append(new_items)

        # Update transitions to reflect merged states
        new_transitions = {}
        for (old_state, symbol), new_state in self.transitions.items():
            from_state = state_mapping[old_state]
            to_state = state_mapping[new_state]
            new_transitions[(from_state, symbol)] = to_state

        self.states = {frozenset(I): idx for idx, I in enumerate(new_C)}
        self.transitions = new_transitions
        self.C = new_C

    def construct_parsing_table(self):
        """Constructs the ACTION and GOTO tables for the LALR(1) parser.

        This method first merges states with identical LR(0) cores and then constructs the
        ACTION and GOTO tables using the merged canonical collection.

        Raises:
            ValueError: If there is a conflict during the construction of the parsing tables.
        """
        self.merge_states()
        super().construct_parsing_table()
