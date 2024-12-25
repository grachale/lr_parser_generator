import pytest
from src.grammars.context_free_grammar import ContextFreeGrammar
from src.parsers.slr1_parser import SLR1Parser
from src.items.lr0_item import LR0Item


@pytest.fixture
def grammar1():
    terminals = ["*", "+", "a", "(", ")"]
    non_terminals = ["S", "E", "P", "T"]
    productions = [
        ("S", ["E"]),
        ("E", ["E", "*", "P"]),
        ("E", ["P"]),
        ("P", ["P", "+", "T"]),
        ("P", ["T"]),
        ("T", ["a"]),
        ("T", ["(", "E", ")"]),
    ]
    start_symbol = "S"
    return ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)


@pytest.fixture
def grammar2():
    terminals = ["+", "a", "(", ")"]
    non_terminals = ["S", "E", "T"]
    productions = [
        ("S", ["E"]),
        ("E", ["E", "+", "T"]),
        ("E", ["T"]),
        ("T", ["a"]),
        ("T", ["(", "E", ")"]),
    ]
    start_symbol = "S"
    return ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)


@pytest.fixture
def parser1(grammar1):
    parser = SLR1Parser(grammar1)
    parser.items()
    parser.construct_parsing_table()
    return parser


@pytest.fixture
def parser2(grammar2):
    parser = SLR1Parser(grammar2)
    parser.items()
    parser.construct_parsing_table()
    return parser


def test_canonical_collection(parser1):
    assert len(parser1.C) > 0, "Canonical collection should not be empty."
    for i, item_set in enumerate(parser1.C):
        assert isinstance(item_set, set), f"Item set {i} should be a set."
        assert all(
            isinstance(item, LR0Item) for item in item_set), f"All items in item set {i} should be of type LR0Item."


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
    input_string = ["a"]
    configurations = parser1.parse(input_string)
    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_valid_input_complex(parser1):
    input_string = ["a", "+", "a", "*", "a"]
    configurations = parser1.parse(input_string)
    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_invalid_input(parser1):
    input_string = ["a", "+", "*"]  # Invalid input
    configurations = parser1.parse(input_string)
    assert configurations is None or configurations[-1][2] != ("accept",), "Invalid input should not be accepted."


def test_parse_valid_input_second_grammar(parser2):
    input_string = ["a", "+", "(", "a", ")"]
    configurations = parser2.parse(input_string)
    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_invalid_input_second_grammar(parser2):
    input_string = ["a", "+", "(", ")"]  # Invalid input
    configurations = parser2.parse(input_string)
    assert configurations is None or configurations[-1][2] != ("accept",), "Invalid input should not be accepted."