from abc import ABC, abstractmethod


class LRParser(ABC):
    """Abstract base class for all types of LR parsers (e.g., LR(0), SLR(1), LALR(1), LR(1)).

    This class provides a common interface and shared methods for different LR parsers. It handles
    grammar augmentation, the construction of parsing tables, and the parsing of input strings.
    Specific types of LR parsers (e.g., LR(0), LR(1)) should inherit from this class and implement
    the abstract methods.

    Attributes:
        grammar (ContextFreeGrammar): The context-free grammar used by the parser.
        action (dict): The ACTION table used in LR parsing, mapping (state, symbol) pairs to actions.
        goto_table (dict): The GOTO table used in LR parsing, mapping (state, non-terminal) pairs to states.
        states (dict): A dictionary mapping item sets to state numbers.
        transitions (dict): A dictionary storing state transitions for the parser.
        C (list): The canonical collection of item sets used in constructing the parsing tables.

    Methods:
        items():
            Abstract method to generate the canonical collection of item sets for the parser.
        construct_parsing_table():
            Abstract method to construct the ACTION and GOTO tables.
        parse(input_string):
            Parses an input string using the constructed ACTION and GOTO tables.
    """

    def __init__(self, context_free_grammar):
        """Initializes the LRParser with a context-free grammar.

        This method augments the given grammar, computes the FIRST sets, and initializes the
        data structures for the ACTION and GOTO tables.

        Args:
            context_free_grammar (ContextFreeGrammar): The context-free grammar to be used by the parser.
        """
        self.grammar = context_free_grammar
        self.grammar.augment_grammar()
        self.grammar.compute_first()
        self.action = {}
        self.goto_table = {}
        self.states = {}
        self.transitions = {}
        self.C = []

    @abstractmethod
    def items(self):
        """Generates the canonical collection of item sets.

        This method should be implemented by subclasses to generate the collection of item sets
        specific to the type of LR parser (e.g., LR(0), SLR(1), LALR(1), LR(1)).
        """
        pass

    @abstractmethod
    def construct_parsing_table(self):
        """Constructs the ACTION and GOTO tables for the parser.

        This method should be implemented by subclasses to construct the ACTION and GOTO tables
        specific to the type of LR parser.
        """
        pass

    def parse(self, input_string):
        """
        Parses an input string using the constructed ACTION and GOTO tables.

        This method simulates the LR parsing process, tracking each step's configuration
        as the parser processes the input string. The configurations include the current
        parser stack, the remaining input, and the action taken (shift, reduce, accept, or error).

        Args:
            input_string (List[str]): The input string to be parsed, represented as a list of tokens.

        Returns:
            List[Tuple[List[int], List[str], Union[Tuple[str, Any], None]]]:
                A list of configurations during the parsing process. Each configuration is a tuple
                containing the current stack, the remaining input, and the action taken.
        """
        input_string = input_string + ['$']
        stack = [0]
        index = 0
        configurations = []

        while True:
            state = stack[-1]
            token = input_string[index]
            action = self.action.get((state, token))
            configurations.append((stack[:], input_string[index:], action))

            if action is None:
                print(f"Error: no action defined for state {state} and token '{token}'")
                return
            elif action[0] == 'shift':
                stack.append(action[1])
                index += 1
            elif action[0] == 'reduce':
                lhs = action[1]
                rhs = action[2]
                # Pop the stack based on the length of the RHS
                for _ in rhs:
                    stack.pop()
                state = stack[-1]
                goto_state = self.goto_table.get((state, lhs))
                if goto_state is None:
                    print(f"Error: no goto state for state {state} and non-terminal '{lhs}'")
                    return
                stack.append(goto_state)
            elif action[0] == 'accept':
                print("Input string accepted.")
                break
            else:
                print(f"Error: unknown action {action}")
                return

        return configurations
