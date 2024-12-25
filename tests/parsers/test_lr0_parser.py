import pytest
from src.grammars.context_free_grammar import ContextFreeGrammar
from src.items.lr0_item import LR0Item
from src.parsers.lr0_parser import LR0Parser


@pytest.fixture
def grammar():
    terminals = ["a", "b", "c"]
    non_terminals = ["S", "A", "B"]
    productions = [
        ("S", ["A", "B", "S"]),
        ("S", ["c"]),
        ("A", ["a"]),
        ("B", ["b"]),
    ]
    start_symbol = "S"
    return ContextFreeGrammar(terminals, non_terminals, productions, start_symbol)


@pytest.fixture
def parser(grammar):
    parser = LR0Parser(grammar)
    parser.items()
    parser.construct_parsing_table()
    return parser


def test_canonical_collection(parser):
    # Test that the canonical collection of items is constructed correctly
    assert len(parser.C) > 0, "Canonical collection should not be empty."

    for i, item_set in enumerate(parser.C):
        assert isinstance(item_set, set), f"Item set {i} should be a set."
        assert all(
            isinstance(item, LR0Item) for item in item_set), f"All items in item set {i} should be of type LR0Item."


def test_action_table(parser):
    # Test that the ACTION table is constructed and contains expected keys
    assert len(parser.action) > 0, "ACTION table should not be empty."
    for (state, symbol), action in parser.action.items():
        assert isinstance(state, int), f"State {state} should be an integer."
        assert isinstance(symbol, str), f"Symbol {symbol} should be a string."
        assert action[0] in ["shift", "reduce", "accept"], f"Invalid action {action[0]} in ACTION table."


def test_goto_table(parser):
    # Test that the GOTO table is constructed and contains expected keys
    assert len(parser.goto_table) > 0, "GOTO table should not be empty."
    for (state, non_terminal), goto_state in parser.goto_table.items():
        assert isinstance(state, int), f"State {state} should be an integer."
        assert isinstance(non_terminal, str), f"Non-terminal {non_terminal} should be a string."
        assert isinstance(goto_state, int), f"GOTO state {goto_state} should be an integer."


def test_parse_valid_input(parser):
    # Test parsing a valid input string
    input_string = ["a", "b", "c"]
    configurations = parser.parse(input_string)

    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_valid_complex_input(parser):
    # Test parsing a more complex valid input string
    input_string = ["a", "b", "a", "b", "c"]
    configurations = parser.parse(input_string)

    assert configurations is not None, "Parsing should produce configurations."
    assert configurations[-1][2] == ("accept",), "Input should be accepted."


def test_parse_invalid_input(parser):
    # Test parsing an invalid input string
    input_string = ["a", "a", "c"]  # Invalid input
    configurations = parser.parse(input_string)

    assert configurations is None or configurations[-1][2] != ("accept",), "Invalid input should not be accepted."
