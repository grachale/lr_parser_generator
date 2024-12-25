# GLOBAL IMPORTS
import streamlit as st
import pandas as pd

# LOCAL IMPORTS
from src.grammars.context_free_grammar import ContextFreeGrammar
from src.parsers.lalr1_parser import LALR1Parser
from src.parsers.lr0_parser import LR0Parser
from src.parsers.lr1_parser import LR1Parser
from src.parsers.slr1_parser import SLR1Parser


def run_ui() -> None:
    """
    Main function to render and handle the user interface for the LR Parser Generator application using Streamlit.

    Features:
        - Collects user input for grammar definition, including non-terminals, terminals, productions, and the start symbol.
        - Validates the grammar input and constructs a context-free grammar object.
        - Allows the user to select and build one of the following LR parsers: LR(0), SLR(1), LALR(1), or LR(1).
        - Displays various parser internal structures, including:
            - Augmented Grammar
            - FIRST Sets
            - FOLLOW Sets
            - Canonical Collection of Items
            - ACTION Table
            - GOTO Table
        - Enables parsing of user-provided input strings and displays the parsing steps.
    """
    st.set_page_config(page_title="LR Parser Generator", layout="wide", initial_sidebar_state="expanded")
    st.title("LR Parser Generator")

    st.sidebar.header("Grammar Definition")
    non_terminals = st.sidebar.text_input("Enter non-terminals (space-separated):", "")
    terminals = st.sidebar.text_input("Enter terminals (space-separated):", "")
    start_symbol = st.sidebar.text_input("Enter the start symbol:", "")

    st.sidebar.subheader("Productions")
    st.sidebar.write("Use '->' to separate LHS and RHS, and '|' for alternatives.")
    productions = st.sidebar.text_area("Enter productions (one per line):", "")

    if st.sidebar.button("Define Grammar"):
        if not all([non_terminals, terminals, start_symbol, productions]):
            st.error("Please complete all grammar fields.")
        else:
            non_terminals_list = non_terminals.split()
            terminals_list = terminals.split()
            productions_list = []
            for line in productions.splitlines():
                if '->' in line:
                    lhs, rhs = line.split('->')
                    lhs = lhs.strip()
                    rhs = rhs.strip()
                    alternatives = rhs.split('|')
                    for alt in alternatives:
                        prod_rhs = alt.strip().split()
                        productions_list.append((lhs, prod_rhs))
                else:
                    st.error(f"Invalid production format: {line}")
                    return

            grammar = ContextFreeGrammar(terminals_list, non_terminals_list, productions_list, start_symbol)
            st.session_state['grammar'] = grammar
            st.success("Grammar defined successfully!")

    if 'grammar' in st.session_state:
        grammar = st.session_state['grammar']
        st.subheader("Select Parser Type")
        parser_type = st.selectbox("Choose a parser type:", ["LR(0)", "SLR(1)", "LALR(1)", "LR(1)"])

        if st.button("Build Parser"):
            if parser_type == "LR(0)":
                parser = LR0Parser(grammar)
            elif parser_type == "SLR(1)":
                parser = SLR1Parser(grammar)
            elif parser_type == "LALR(1)":
                parser = LALR1Parser(grammar)
            elif parser_type == "LR(1)":
                parser = LR1Parser(grammar)

            parser.items()
            parser.construct_parsing_table()
            st.session_state['parser'] = parser
            st.success(f"{parser_type} Parser built successfully!")

        if 'parser' in st.session_state:
            parser = st.session_state['parser']
            st.subheader("Parser Features")
            feature = st.selectbox("Select a feature to display:", [
                "Augmented Grammar",
                "FIRST Sets",
                "FOLLOW Sets",
                "Canonical Collection of Items",
                "ACTION Table",
                "GOTO Table",
                "Parse Input String",
            ])

            # Different Parser Internal Structures
            if feature == "Augmented Grammar":
                st.write("**Augmented Grammar:**")
                for idx, prod in enumerate(parser.grammar.productions):
                    st.write(f"{idx}: {prod[0]} -> {' '.join(prod[1])}")

            elif feature == "FIRST Sets":
                if parser.grammar.first is None:
                    parser.grammar.compute_first()
                st.write("**FIRST Sets:**")
                for symbol, first_set in parser.grammar.first.items():
                    st.write(f"FIRST({symbol}) = {{ {', '.join(first_set)} }}")

            elif feature == "FOLLOW Sets":
                if parser.grammar.follow is None:
                    parser.grammar.compute_follow()
                st.write("**FOLLOW Sets:**")
                for symbol, follow_set in parser.grammar.follow.items():
                    st.write(f"FOLLOW({symbol}) = {{ {', '.join(follow_set)} }}")

            elif feature == "Canonical Collection of Items":
                st.write("**Canonical Collection of Items:**")
                for idx, I in enumerate(parser.C):
                    st.write(f"**I{idx}:**")
                    for item in I:
                        st.write(f"  {item}")

            elif feature == "ACTION Table":
                st.write("**ACTION Table:**")
                action_data = {}
                for (state, symbol), action in parser.action.items():
                    if state not in action_data:
                        action_data[state] = {}
                    action_data[state][symbol] = str(action)
                action_table = pd.DataFrame(action_data).T
                action_table.index.name = "State"
                st.dataframe(action_table, use_container_width=True)

            elif feature == "GOTO Table":
                st.write("**GOTO Table:**")
                goto_data = {}
                for (state, non_terminal), goto in parser.goto_table.items():
                    if state not in goto_data:
                        goto_data[state] = {}
                    goto_data[state][non_terminal] = str(goto)
                goto_table = pd.DataFrame(goto_data).T
                goto_table.index.name = "State"
                st.dataframe(goto_table, use_container_width=True)

            elif feature == "Parse Input String":
                input_string = st.text_input("Enter the input string (tokens separated by spaces):")
                if st.button("Parse Input"):
                    tokens = input_string.split()
                    try:
                        configurations = parser.parse(tokens)

                        # Check if input was accepted
                        if configurations is None or configurations[-1][2] != ('accept',):
                            st.error("Parsing failed.")
                            return
                        else:
                            st.success("Input string parsed successfully!")

                        st.write("**Parsing Steps:**")

                        steps_data = []
                        for step in configurations:
                            stack = ' '.join(map(str, step[0]))
                            remaining_input = ' '.join(step[1])
                            action = str(step[2])
                            steps_data.append({"Stack": stack, "Remaining Input": remaining_input, "Action": action})

                        steps_df = pd.DataFrame(steps_data)
                        st.dataframe(steps_df, use_container_width=True)

                    except ValueError as e:
                        st.error(f"Error during parsing: {e}")
