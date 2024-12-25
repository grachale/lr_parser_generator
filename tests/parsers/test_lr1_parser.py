import pytest
from src.grammars.context_free_grammar import ContextFreeGrammar
from src.parsers.lr1_parser import LR1Parser
from src.items.lr1_item import LR1Item


@pytest.fixture
def grammar1():
    terminals = ["c", "b", "a"]
    non_terminals = ["S", "A"]
    productions = [
        ("S", ["S", "c"]),
        ("S", ["A", "S", "c"]),
        ("S", ["b"]),
        ("A", ["a", "A"]),
        ("A", ["a"]),
    ]
    start_symbol = "S"
    return ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)


@pytest.fixture
def grammar2():
    terminals = ["if", "then", "+", "*", "(", ")", "or", "else", "i", ":="]
    non_terminals = ["S", "A", "I", "E", "T", "P", "B", "L"]
    productions = [
        ("S", ["A"]),
        ("S", ["I"]),
        ("A", ["i", ":=", "E"]),
        ("I", ["if", "B", "then", "A", "L"]),
        ("E", ["T"]),
        ("E", ["E", "+", "T"]),
        ("T", ["P"]),
        ("T", ["T", "*", "P"]),
        ("P", ["(", "E", ")"]),
        ("P", ["i"]),
        ("B", ["B", "or", "i"]),
        ("B", ["i"]),
        ("L", ["else", "S"]),
        ("L", ["ε"]),
    ]
    start_symbol = "S"
    return ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)


@pytest.fixture
def parser1(grammar1):
    parser = LR1Parser(grammar1)
    parser.items()
    parser.construct_parsing_table()
    return parser


@pytest.fixture
def parser2(grammar2):
    parser = LR1Parser(grammar2)
    parser.items()
    parser.construct_parsing_table()
    return parser


def test_canonical_collection(parser1):
    assert len(parser1.C) > 0, "Canonical collection should not be empty."
    for i, item_set in enumerate(parser1.C):
        assert isinstance(item_set, set), f"Item set {i} should be a set."
        assert all(
            isinstance(item, LR1Item) for item in item_set), f"All items in item set {i} should be of type LR1Item."


def test_action_table(parser1):
    assert len(parser1.action) > 0, "ACTION table should not be empty."
    for (state, symbol), action in parser1.action.items():
        assert isinstance(state, int), f"State {state} should be an integer."
        assert isinstance(symbol, str), f"Symbol {symbol} should be a string."
        assert action[0] in ["shift", "reduce", "accept"], f"Invalid action {action[0]} in ACTION table."


def test_goto_table(parser1):
    assert len(parser1.goto_table) > 0, "GOTO table should not be empty."
    for (state, non_terminal), goto_state in parser1.goto_table.items():
        assert isinstance(state, int), f"State {state} should be an integer."
        assert isinstance(non_terminal, str), f"Non-terminal {non_terminal} should be a string."
        assert isinstance(goto_state, int), f"GOTO state {goto_state} should be an integer."


def test_parse_valid_input_simple(parser1):
    input_string = ["a", "b", "c"]
    configurations = parser1.parse(input_string)
    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_valid_input_complex(parser1):
    input_string = ["a", "a", "b", "c", "c"]
    configurations = parser1.parse(input_string)
    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_invalid_input(parser1):
    input_string = ["a", "b", "b"]  # Invalid input
    configurations = parser1.parse(input_string)
    assert configurations is None or configurations[-1][2] != ("accept",), "Invalid input should not be accepted."


def test_parse_valid_input_second_grammar(parser2):
    input_string = ["if", "i", "then", "i", ":=", "i", "+", "i", "else", "i", ":=", "i"]
    configurations = parser2.parse(input_string)
    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_invalid_input_second_grammar(parser2):
    input_string = ["if", "i", "then", "i", "+", "else"]  # Invalid input
    configurations = parser2.parse(input_string)
    assert configurations is None or configurations[-1][2] != ("accept",), "Invalid input should not be accepted."
