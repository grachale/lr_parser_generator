import pytest
from src.grammars.context_free_grammar import ContextFreeGrammar
from src.parsers.lalr1_parser import LALR1Parser
from src.parsers.lr1_parser import LR1Parser


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
def lr1_parser1(grammar1):
    parser = LR1Parser(grammar1)
    parser.items()
    parser.construct_parsing_table()
    return parser


@pytest.fixture
def lalr1_parser1(grammar1):
    parser = LALR1Parser(grammar1)
    parser.items()
    parser.construct_parsing_table()
    return parser


@pytest.fixture
def lr1_parser2(grammar2):
    parser = LR1Parser(grammar2)
    parser.items()
    parser.construct_parsing_table()
    return parser


@pytest.fixture
def lalr1_parser2(grammar2):
    parser = LALR1Parser(grammar2)
    parser.items()
    parser.construct_parsing_table()
    return parser


def test_state_reduction(grammar1, lr1_parser1, lalr1_parser1):
    assert len(lalr1_parser1.C) < len(lr1_parser1.C), "LALR(1) parser should have fewer states than LR(1) parser."


def test_parsing_behavior_simple(grammar1, lalr1_parser1):
    input_string = ["a", "b", "c"]
    configurations = lalr1_parser1.parse(input_string)

    assert configurations[-1][2] == ("accept",), "LALR(1) parser should accept the input."


def test_state_reduction_complex(grammar2, lr1_parser2, lalr1_parser2):
    assert len(lalr1_parser2.C) < len(lr1_parser2.C), "LALR(1) parser should have fewer states than LR(1) parser."


def test_parsing_behavior_complex(grammar2, lalr1_parser2):
    input_string = ["if", "i", "then", "i", ":=", "i", "+", "i", "else", "i", ":=", "i"]
    configurations = lalr1_parser2.parse(input_string)

    assert configurations[-1][2] == ("accept",), "LALR(1) parser should accept the input."


def test_invalid_parsing_behavior(grammar1, lalr1_parser1):
    input_string = ["a", "b", "b"]  # Invalid input
    configurations = lalr1_parser1.parse(input_string)

    assert configurations is None or configurations[-1][2] != (
        "accept",), "LALR(1) parser should reject invalid input."
