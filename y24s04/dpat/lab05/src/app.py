"""
Course: dpat'4
Lab: 05
"""

import dash
import dash_bootstrap_components as dbc

from dash import html, dcc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

EXPLAINER = """ Some dope dog shit """

controls = html.Div(
    [
        dbc.Row(
            dbc.Label('Controls'),
        ),
        dbc.Row(
            dbc.ButtonGroup([
                dbc.Button(
                    "Randomize",
                    color="primary",
                    id="randomize",
                ),
                dbc.Button(
                    "Reset settings",
                    color="secondary",
                    id="reset",
                )
            ]),
        )
    ]
)

app.layout = dbc.Container(
    [
        html.H1("Harmonic Visualisation"),
        dcc.Markdown(EXPLAINER),

        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dash.dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
