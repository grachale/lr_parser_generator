from dash.dependencies import Input, Output, State
from dash import html, dcc

from src.grammars.context_free_grammar import ContextFreeGrammar
from src.parsers.lalr1_parser import LALR1Parser
from src.parsers.lr0_parser import LR0Parser
from src.parsers.lr1_parser import LR1Parser
from src.parsers.slr1_parser import SLR1Parser


def register_callbacks(app):
    """
    Register all callbacks on the given Dash app.

    Args:
        app: The Dash application instance.
    """

    @app.callback(
        Output("status-message", "children"),
        Input("build-button", "n_clicks"),
        [State("non-terminals", "value"),
         State("terminals", "value"),
         State("start-symbol", "value"),
         State("productions", "value"),
         State("parser-type", "value")]
    )
    def build_parser_feedback(n_clicks, nts, ts, start, prods, ptype):
        """
        Update the status message after attempting to build the parser.

        Returns:
            A status message string indicating success or missing inputs.
        """
        if n_clicks is None:
            return ""
        if not (nts and ts and start and prods and ptype):
            return "Please fill in all fields to build the parser."
        return "Parser built successfully!"

    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value"),
        [State("non-terminals", "value"),
         State("terminals", "value"),
         State("start-symbol", "value"),
         State("productions", "value"),
         State("parser-type", "value"),
         State("build-button", "n_clicks")],
        prevent_initial_call=True
    )
    def render_tab_content(active_tab, nts, ts, start, prods, ptype, n_clicks):
        """
        Render the content of the currently active tab based on the chosen grammar,
        parser type, and constructed parser.

        Returns:
            A Dash component (usually a Div) containing the tab's content.
        """
        if not n_clicks:
            return html.Div("Please define the grammar and build the parser first.")

        if not (nts and ts and start and prods):
            return html.Div("Please provide all grammar details and build the parser.")

        # Build grammar
        non_terminals = nts.split()
        terminals = ts.split()
        start_symbol = start.strip()

        # Parse productions
        productions_list = []
        for line in prods.splitlines():
            line = line.strip()
            if line and '->' in line:
                lhs, rhs = line.split('->')
                lhs = lhs.strip()
                rhs = rhs.strip()
                alternatives = rhs.split('|')
                for alt in alternatives:
                    prod_rhs = alt.strip().split()
                    productions_list.append((lhs, prod_rhs))

        grammar = ContextFreeGrammar(terminals, non_terminals, productions_list, start_symbol)

        # Build parser
        if ptype == 'LR(0)':
            parser = LR0Parser(grammar)
        elif ptype == 'SLR(1)':
            parser = SLR1Parser(grammar)
        elif ptype == 'LR(1)':
            parser = LR1Parser(grammar)
        elif ptype == 'LALR(1)':
            parser = LALR1Parser(grammar)
        else:
            return html.Div("Unknown parser type.")

        parser.items()
        parser.construct_parsing_table()

        # Depending on the tab selected, show appropriate info
        if active_tab == "tab-grammar":
            # Augmented Grammar
            content = [html.H4("Augmented Grammar")]
            for idx, prod in enumerate(parser.grammar.productions):
                content.append(html.Div(f"{idx}: {prod[0]} -> {' '.join(prod[1])}"))
            return html.Div(content)

        elif active_tab == "tab-first":
            # FIRST sets
            if parser.grammar.first is None:
                parser.grammar.compute_first()
            content = [html.H4("FIRST sets")]
            for symbol in parser.grammar.first:
                first_set = ', '.join(parser.grammar.first[symbol])
                content.append(html.Div(f"FIRST({symbol}) = {{ {first_set} }}"))
            return html.Div(content)

        elif active_tab == "tab-follow":
            # FOLLOW sets
            if parser.grammar.follow is None:
                parser.grammar.compute_follow()
            content = [html.H4("FOLLOW sets")]
            for symbol in parser.grammar.follow:
                follow_set = ', '.join(parser.grammar.follow[symbol])
                content.append(html.Div(f"FOLLOW({symbol}) = {{ {follow_set} }}"))
            return html.Div(content)

        elif active_tab == "tab-canonical":
            # Canonical Collection of Items
            content = [html.H4("Canonical Collection of Items")]
            for idx, I in enumerate(parser.C):
                content.append(html.H5(f"I{idx}:"))
                for item in I:
                    content.append(html.Div(str(item)))
            return html.Div(content)

        elif active_tab == "tab-action":
            # ACTION Table
            content = [html.H4("ACTION Table")]
            for key in sorted(parser.action.keys()):
                content.append(html.Div(f"State {key[0]}, Symbol {key[1]}: {parser.action[key]}"))
            return html.Div(content)

        elif active_tab == "tab-goto":
            # GOTO Table
            content = [html.H4("GOTO Table")]
            for key in sorted(parser.goto_table.keys()):
                content.append(html.Div(f"State {key[0]}, Non-terminal {key[1]}: {parser.goto_table[key]}"))
            return html.Div(content)

        elif active_tab == "tab-parse":
            # Provide input box and button to parse a string
            return html.Div([
                html.H4("Parse an input string"),
                dcc.Input(id="input-string", type="text", placeholder="id + id * id", style={"width": "100%"}),
                html.Br(),
                html.Button("Parse", id="parse-button", style={"backgroundColor": "#4CAF50", "color": "white", "border": "none", "padding": "10px 20px", "cursor": "pointer"}),
                html.Div(id="parse-result", style={"marginTop": "20px"})
            ])

    @app.callback(
        Output("parse-result", "children"),
        Input("parse-button", "n_clicks"),
        [State("non-terminals", "value"),
         State("terminals", "value"),
         State("start-symbol", "value"),
         State("productions", "value"),
         State("parser-type", "value"),
         State("input-string", "value")],
        prevent_initial_call=True)
    def parse_input_string(n_clicks, nts, ts, start, prods, ptype, input_str):
        """
        Parse the given input string using the currently selected grammar and parser.

        Returns:
            A Dash component displaying the parsing result or an error message.
        """
        if not all([nts, ts, start, prods, ptype, input_str]):
            return "Please define the grammar, parser type, and provide an input string."

        non_terminals = nts.split()
        terminals = ts.split()
        start_symbol = start.strip()

        productions_list = []
        for line in prods.splitlines():
            line = line.strip()
            if line and '->' in line:
                lhs, rhs = line.split('->')
                lhs = lhs.strip()
                rhs = rhs.strip()
                alternatives = rhs.split('|')
                for alt in alternatives:
                    prod_rhs = alt.strip().split()
                    productions_list.append((lhs, prod_rhs))

        grammar = ContextFreeGrammar(terminals, non_terminals, productions_list, start_symbol)

        if ptype == 'LR(0)':
            parser = LR0Parser(grammar)
        elif ptype == 'SLR(1)':
            parser = SLR1Parser(grammar)
        elif ptype == 'LR(1)':
            parser = LR1Parser(grammar)
        elif ptype == 'LALR(1)':
            parser = LALR1Parser(grammar)
        else:
            return "Unknown parser type."

        parser.items()
        parser.construct_parsing_table()

        input_tokens = input_str.strip().split()
        try:
            parse_result = parser.parse(input_tokens)
            return html.Div([
                html.Div("Parsing successful!"),
                html.Div("Derivation Steps:"),
                html.Pre(str(parse_result))
            ])
        except Exception as e:
            return html.Div(str(e), style={"color": "red"})
