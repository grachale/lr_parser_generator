# Learning Tool for LR Parsers

This project is a learning tool designed to help users understand and generate LR parsers, including LR(0), SLR(1), LALR(1), and LR(1). It provides interactive features such as grammar definition, parser construction, and input string testing, enabling users to explore the internal structures and functionality of LR parsers.

---

## Features

- **Grammar Definition**: Define grammars using terminals, non-terminals, productions, and a start symbol.
- **Parser Construction**:
  - Generate ACTION and GOTO tables.
  - Build canonical collections.
  - Support for LR(0), SLR(1), LALR(1), and LR(1) parsers.
- **Interactive Testing**: Test input strings and visualize parsing steps.
- **Visualization**: View essential parsing components, such as FIRST/FOLLOW sets and canonical item sets.
- **Modular Design**: Built for easy extension and maintenance.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/grachale/lr_parser_generator
   ```

2. Navigate to the project directory:
   ```bash
   cd lr_parser_generator
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Application

The user interface is built using Streamlit. To launch the application:
```bash
streamlit run run.py
```

This will open a web-based interface where you can:
- Define grammars.
- Select parser types (LR(0), SLR(1), LALR(1), LR(1)).
- Test input strings.
- Visualize parser components.

### Example Grammar Input
Define a grammar in the sidebar of the application:
- **Non-terminals**: `E T F`
- **Terminals**: `id + * ( )`
- **Productions**:
  ```
  E -> T E2
  E2 -> + T E2 | ε
  T -> F T2
  T2 -> * F T2 | ε
  F -> ( E ) | id
  ```
- **Start Symbol**: `E`

---

## Project Structure

```plaintext
src/
├── grammars/               # Grammar classes
│   ├── grammar.py          # Base Grammar class
│   └── context_free_grammar.py # ContextFreeGrammar class
├── items/                  # Item classes
│   ├── lr0_item.py         # LR(0) Item class
│   └── lr1_item.py         # LR(1) Item class
├── parsers/                # Parser classes
│   ├── lr_parser.py        # Abstract LRParser class
│   ├── lr0_parser.py       # LR(0) parser implementation
│   ├── slr1_parser.py      # SLR(1) parser implementation
│   ├── lalr1_parser.py     # LALR(1) parser implementation
│   └── lr1_parser.py       # LR(1) parser implementation
└── ui/                     # User interface components
    └── app.py              # Main entry point for the Streamlit app
```

---

## Testing

Unit tests are implemented using the [pytest](https://docs.pytest.org/) framework. Mocking is used where necessary, for example, to simulate grammar behavior in parser tests.

### Running Tests

To run all tests:
```bash
pytest
```

### Test Coverage
- **Grammars**: Tests for grammar operations like FIRST and FOLLOW computation.
- **Items**: Tests for LR(0) and LR(1) item functionality.
- **Parsers**: Comprehensive tests for parser construction and parsing operations.

---

## Future Improvements

Potential future extensions for the tool include:
- Error recovery mechanisms.
- Support for ambiguous grammars.
- Enhanced graphical visualizations of parser states.
- Improved grammar input flexibility.

