from dash import dcc, html

def create_layout():
    """
    Create and return the Dash layout for the application.

    Returns:
        A Dash HTML Div component representing the application's layout.
    """
    layout = html.Div(
        style={"backgroundColor": "#1E1E1E", "color": "white", "padding": "20px"},
        children=[
            html.H1("LR Parser Generator", style={"textAlign": "center"}),

            html.Div(
                style={"display": "flex", "gap": "20px"},
                children=[
                    html.Div(
                        style={"flex": "1"},
                        children=[
                            html.H3("Define a New Grammar"),
                            html.Label("Non-terminals (space-separated)"),
                            dcc.Input(
                                id="non-terminals",
                                type="text",
                                placeholder="E T F",
                                style={"width": "100%"}
                            ),
                            html.Br(),
                            html.Label("Terminals (space-separated)"),
                            dcc.Input(
                                id="terminals",
                                type="text",
                                placeholder="id + * ( )",
                                style={"width": "100%"}
                            ),
                            html.Br(),
                            html.Label("Start symbol"),
                            dcc.Input(
                                id="start-symbol",
                                type="text",
                                placeholder="E",
                                style={"width": "100%"}
                            ),
                            html.Br(),
                            html.Label("Productions (one per line, use '->' and '|' for alternatives)"),
                            dcc.Textarea(
                                id="productions",
                                placeholder="E -> E + T | T\nT -> T * F | F\nF -> ( E ) | id",
                                style={"width": "100%", "height": "150px"}
                            ),
                            html.Br(),
                            html.Button("Build Grammar & Parser", id="build-button", style={"backgroundColor": "#4CAF50", "color": "white", "border": "none", "padding": "10px 20px", "cursor": "pointer"}),
                        ]
                    ),
                    html.Div(
                        style={"flex": "1"},
                        children=[
                            html.Label("Choose Parser Type"),
                            dcc.Dropdown(
                                id="parser-type",
                                options=[
                                    {"label": "LR(0)", "value": "LR(0)"},
                                    {"label": "SLR(1)", "value": "SLR(1)"},
                                    {"label": "LR(1)", "value": "LR(1)"},
                                    {"label": "LALR(1)", "value": "LALR(1)"}
                                ],
                                value="LR(0)",
                                style={"color": "black"}
                            )
                        ]
                    )
                ]
            ),

            html.Hr(),

            html.H3("Results"),

            dcc.Tabs(
                id="tabs",
                value="tab-grammar",
                children=[
                    dcc.Tab(label="Augmented Grammar", value="tab-grammar"),
                    dcc.Tab(label="FIRST Sets", value="tab-first"),
                    dcc.Tab(label="FOLLOW Sets", value="tab-follow"),
                    dcc.Tab(label="Canonical Collection", value="tab-canonical"),
                    dcc.Tab(label="ACTION Table", value="tab-action"),
                    dcc.Tab(label="GOTO Table", value="tab-goto"),
                    dcc.Tab(label="Parse Input String", value="tab-parse"),
                ]
            ),

            html.Div(id="tab-content", style={"marginTop": "20px"}),

            html.Hr(),

            html.Div(id="status-message", style={"color": "lightgreen", "fontWeight": "bold"})
        ]
    )
    return layout
