"""
Course: dpat'4
Lab: 05
"""

import dash
import numpy as np

import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dash import html, dcc, Input, Output, State

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no",
        }
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css]
)

app.title = "Harmonic Visualisation"

initial_values = {
    'amplitude': {'value': 1.0, 'min': 0.1, 'max': 10.0},
    'frequency': {'value': 1, 'min': 0.1, 'max': 10.0},
    'phase': {'value': 0, 'min': 0.0, 'max': 2 * np.pi},
    'noise_mean': {'value': 0.0, 'min': -1.0, 'max': 1.0},
    'noise_covariance': {'value': 0.1, 'min': 0.0, 'max': 1.0},
}

ids = {'buttons': [], 'sliders': [], 'checklists': []}


def build_header():
    return html.Div(
        children=[
            html.H4('Harmonic Visualisation'),
        ],
        className="pt-5 pb-3"
    )


def build_sliders():
    sliders = []

    for key, value in initial_values.items():
        slider_id = key + '-input'
        ids['sliders'].append(slider_id)
        step_size = (value['max'] - value['min']) // 100

        slider = html.Div(
            children=[
                dbc.Label(key.replace('_', ' ').title()),
                dcc.Slider(
                    id=slider_id,
                    min=value['min'],
                    max=value['max'],
                    step=step_size,
                    value=value['value'],
                    className="dbc mb-4",
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                )
            ]
        )

        sliders.append(slider)

    return sliders


def build_switch():
    html_id = 'switch-input'
    ids['checklists'].append(html_id)

    return html.Div(
        children=[
            dbc.Label('Additional settings'),
            dbc.Checklist(
                id=html_id,
                value=[1],
                switch=True,
                options=[
                    {"label": "Show noise", "value": 1}
                ],
                className="mb-4"
            )
        ]
    )


def build_buttons():
    btn_random_id, btn_reset_id = 'random-button', 'reset-button'
    ids['buttons'].append(btn_random_id), ids['buttons'].append(btn_reset_id)

    return html.Div(
        children=[
            dbc.Button(
                "Randomise",
                id=btn_random_id,
                color="primary",
                className="ml-4",
                n_clicks=0
            ),
            dbc.Button(
                "Reset",
                id=btn_reset_id,
                color="danger",
                n_clicks=0
            )
        ],
        className="d-flex flex-row gap-2"
    )


def build_settings():
    return dbc.Card(
        dbc.CardBody(
            children=[
                html.H5('Function settings', className="card-title"),
                html.Br(),
                *build_sliders(),
                html.Hr(),
                build_switch(),
                build_buttons()
            ]
        ),
        id='settings'
    )


app.layout = dbc.Container(
    children=[
        build_header(),
        html.Div(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(build_settings(), md=4),
                        dbc.Col(
                            dbc.Spinner(
                                children=[
                                    dcc.Graph(id='graph'),
                                    html.Div(id='slider-output-container')
                                ],
                                delay_show=200
                            )
                        )
                    ]
                )
            ],
            className="border border-secondary-subtle p-4 rounded-4 shadow-sm"
        )
    ],
    fluid=True,
    className="container-md"
)


@app.callback(
    [Output(slider_id, 'value') for slider_id in ids['sliders']],
    [Input(button_id, 'n_clicks') for button_id in ids['buttons']],
    [State(slider_id, 'value') for slider_id in ids['sliders']]
)
def update_inputs(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return args[-len(ids['sliders']):]
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'reset-button' in button_id:
        return [initial_values[slider_id.split('-')[0]]['value'] for slider_id in ids['sliders']]

    if 'random-button' in button_id:
        return [
            np.random.uniform(initial_values[slider_id.split('-')[0]]['min'],
                              initial_values[slider_id.split('-')[0]]['max'])
            for slider_id in ids['sliders']
        ]


noise_cache = {}


@app.callback(
    Output('graph', 'figure'),
    [Input(slider_id, 'value') for slider_id in ids['sliders']],
    [Input('switch-input', 'value')]
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    noise_key = (noise_mean, noise_covariance)
    t = np.linspace(0, 2 * np.pi, 500)

    if noise_key not in noise_cache:
        noise_cache[noise_key] = np.random.normal(noise_mean, noise_covariance, t.shape)

    noise = noise_cache[noise_key]

    harmonic = amplitude * np.sin(frequency * t + phase)
    signal = harmonic + noise if 1 in show_noise else harmonic

    # Create the figure
    figure = {
        'data': [
            go.Scatter(x=t, y=harmonic, mode='lines', name='Harmonic', line=dict(dash='dash')),
            go.Scatter(x=t, y=signal, mode='lines', name='Signal')
        ],
        'layout': {
            'title': 'Harmonic Function with Noise',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'}
        }
    }
    return figure


@app.callback(
    Output('slider-output-container', 'children'),
    [Input(slider_id, 'value') for slider_id in ids['sliders']],
    [Input('switch-input', 'value')]
)
def update_output(*args):
    values = args[:-1]
    switch = args[-1]

    tmp = []

    for slider_id, value in zip(ids['sliders'], values):
        label = slider_id.replace('_', ' ').replace('-input', '').title()
        tmp.append(html.P(f'{label}: {value}'))

    tmp.append(html.P(f'Show Noise: {switch}'))

    return html.Div(
        children=[
            dbc.Button(
                "Debug info",
                id="hover-target",
                color="secondary",
                className="me-1",
                n_clicks=0,
            ),
            dbc.Popover(
                tmp,
                target="hover-target",
                body=True,
                trigger="hover",
            )
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
