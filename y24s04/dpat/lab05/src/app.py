"""
Course: dpat'4
Lab: 05
"""

import dash
import numpy as np

import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from scipy.signal import iirfilter, lfilter, welch
from dash import html, dcc, Input, Output, State, ctx

DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(
    __name__,
    title="Harmonic Visualisation",
    external_stylesheets=[dbc.themes.BOOTSTRAP, DBC_CSS]
)

# Dict for default values of each input
DEFAULTS: dict = {
    'amplitude': {'value': 1.0, 'min': 0.1, 'max': 10.0, 'step': '?', 'category': 'function'},
    'frequency': {'value': 1, 'min': 0.1, 'max': 10.0, 'step': '?', 'category': 'function'},
    'phase': {'value': 0, 'min': 0.0, 'max': round(2 * np.pi), 'step': '?', 'category': 'function'},
    'noise_mean': {'value': 0.0, 'min': -1.0, 'max': 1.0, 'step': '?', 'category': 'noise'},
    'noise_covariance': {'value': 0.1, 'min': 0.0, 'max': 1.0, 'step': '?', 'category': 'noise'},
    'filter_order': {'value': 4, 'min': 1, 'max': 10, 'step': '?', 'category': 'filter'},
    'cutoff_frequency': {'value': 0.02, 'min': 0.01, 'max': 0.08, 'step': '?', 'category': 'filter'}
}


def calc_steps(
        min_: float,
        max_: float,
        steps: float = 10
) -> float:
    """ Calculates step value (for dcc.Slider) based on the given min and max values """

    raw = (max_ - min_) / steps
    correlation = 10 ** np.floor(np.log10(raw))
    res = raw / correlation

    if res >= 5:
        return 5 * correlation
    elif res >= 2:
        return 2 * correlation
    else:
        return correlation


def build_header():
    return html.Div(
        children=[
            html.H4('Harmonic Visualisation'),
        ],
        className="pt-3 pb-3"
    )


def build_slider(name: str, config: dict):
    step = config['step'] if '?' not in config['step'] \
        else calc_steps(config['min'], config['max'], 5)

    slider_div_id = name + '-div'
    category = config['category']

    slider = html.Div(
        id=slider_div_id,
        className=f"mb-4",
        children=[
            dbc.Label(name.replace('_', ' ').title(), html_for=name),
            dcc.Slider(
                id=name,
                className="dbc",
                min=config['min'],
                max=config['max'],
                marks=None,
                value=config['value'],
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ]
    )

    return slider


def build_categorial_sliders(defaults, category):
    return [
        build_slider(name, config)
        for name, config
        in defaults.items()
        if config['category'] == category
    ]


def build_switches():
    return html.Div(
        children=[
            dbc.Checklist(
                id='switch-input',
                value=['show_noise'],
                switch=True,
                options=[
                    {"label": "Show noise", "value": 'show_noise'},
                    {"label": "Show filter", "value": 'show_filter'},
                    {"label": "Split graphs", "value": 'split_graph'},
                ],
                inline=True,
                className="mb-4"
            )
        ]
    )


def build_buttons():
    return html.Div(
        children=[
            dbc.Button(
                "Randomise",
                id='random-button',
                color="primary",
                className="ml-4",
                n_clicks=0
            ),
            dbc.Button(
                "Reset",
                id='reset-button',
                color="danger",
                n_clicks=0
            )
        ],
        className="d-flex flex-row gap-2"
    )


def build_settings():
    sliders: list = [build_slider(name, config) for name, config in DEFAULTS.items()]

    function_settings = dbc.Col([dbc.Card([
        dbc.CardHeader('Function Settings'),
        dbc.CardBody([
            dbc.Form([
                *build_categorial_sliders(DEFAULTS, 'function'),
            ])
        ])
    ])
    ])

    noise_settings = dbc.Col([dbc.Card([
        dbc.CardHeader('Noise Settings'),
        dbc.CardBody([
            dbc.Form([
                *build_categorial_sliders(DEFAULTS, 'noise'),
            ])
        ])
    ])
    ])

    filter_settings = dbc.Col([
        dbc.Card([
            dbc.CardHeader('Filter Settings'),
            dbc.CardBody([
                dbc.Form([
                    *build_categorial_sliders(DEFAULTS, 'filter'),
                ])
            ])
        ])
    ])

    general_settings = dbc.Col([
        dbc.Card([
            dbc.CardHeader('General Settings'),
            dbc.CardBody([
                build_switches(),
                build_buttons()
            ])
        ])
    ])

    return [function_settings, noise_settings, filter_settings, general_settings]


@app.callback(
    [
        Output('noise_mean', 'disabled'),
        Output('noise_covariance', 'disabled'),
        Output('filter_order', 'disabled'),
        Output('cutoff_frequency', 'disabled'),
        Output('noise_mean-div', 'style'),
        Output('noise_covariance-div', 'style'),
        Output('filter_order-div', 'style'),
        Output('cutoff_frequency-div', 'style'),
    ],
    [
        Input('switch-input', 'value')
    ]
)
def update_sliders(switches):
    show_noise = 'show_noise' in switches
    show_filter = 'show_filter' in switches

    noise_div_style = {'opacity': '0.2'} if not show_noise else {'opacity': '1'}
    filter_div_style = {'opacity': '0.2'} if not show_filter else {'opacity': '1'}

    return [not show_noise, not show_noise, not show_filter,
            not show_filter, noise_div_style, noise_div_style, filter_div_style, filter_div_style]


@app.callback(
    [
        Output('amplitude', 'value'),
        Output('frequency', 'value'),
        Output('phase', 'value'),
        Output('noise_mean', 'value'),
        Output('noise_covariance', 'value'),
        Output('filter_order', 'value'),
        Output('cutoff_frequency', 'value')
    ],
    [
        Input('random-button', 'n_clicks'),
        Input('reset-button', 'n_clicks')
    ],
    [
        State('amplitude', 'value'),
        State('frequency', 'value'),
        State('phase', 'value'),
        State('noise_mean', 'value'),
        State('noise_covariance', 'value'),
        State('filter_order', 'value'),
        State('cutoff_frequency', 'value')
    ]
)
def update_inputs(random_btn, reset_btn, *args):
    if 'reset-button' == ctx.triggered_id:
        return [DEFAULTS[slider]['value'] for slider in DEFAULTS.keys()]

    if 'random-button' == ctx.triggered_id:
        return [
            np.random.uniform(
                DEFAULTS[slider]['min'],
                DEFAULTS[slider]['max']
            ) for slider in DEFAULTS.keys()
        ]

    return args


noise_cache = {}


@app.callback(
    [
        Output('graph', 'figure'),
        Output('harmonic-graph', 'figure'),
        Output('signal-graph', 'figure'),
        Output('filter-graph', 'figure'),
        Output('graph', 'style'),
        Output('harmonic-graph', 'style'),
        Output('signal-graph', 'style'),
        Output('filter-graph', 'style')
    ],
    [
        Input('amplitude', 'value'),
        Input('frequency', 'value'),
        Input('phase', 'value'),
        Input('noise_mean', 'value'),
        Input('noise_covariance', 'value'),
        Input('filter_order', 'value'),
        Input('cutoff_frequency', 'value'),
        Input('switch-input', 'value')
    ]
)
def update_graph(
        amplitude,
        frequency,
        phase,
        noise_mean,
        noise_cov,
        filter_order,
        cutoff_freq,
        switches
):
    show_noise = 'show_noise' in switches
    show_filter = 'show_filter' in switches
    split_graph = 'split_graph' in switches

    noise_key = (noise_mean, noise_cov)
    t = np.linspace(0, 2 * np.pi, 500)

    if noise_key not in noise_cache:
        noise_cache[noise_key] = np.random.normal(noise_mean, noise_cov, t.shape)

    noise = noise_cache[noise_key]

    harmonic = amplitude * np.sin(frequency * t + phase)
    signal = harmonic + noise if show_noise else harmonic

    nyquist_rate = 0.5
    normalised_cutoff = cutoff_freq / nyquist_rate

    filter_order = int(filter_order)

    if show_filter:
        b, a = iirfilter(
            filter_order, normalised_cutoff, btype='low', ftype='butter', analog=False
        )
        filtered_signal = lfilter(b, a, signal)
    else:
        filtered_signal = signal

    harmonic_graph = {
        'data': [
            go.Scatter(x=t, y=harmonic, mode='lines', name='Harmonic', line=dict(dash='dash'))
        ],
        'layout': {
            'title': 'Harmonic Function',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'}
        }
    }

    signal_fig = {
        'data': [
            go.Scatter(x=t, y=signal, mode='lines', name='Noisy Signal')
        ],
        'layout': {
            'autosize': True,
            'title': 'Noisy Signal',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'}
        }
    }

    filtered_fig = {
        'data': [
            go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal')
        ],
        'layout': {
            'autosize': True,
            'title': 'Filtered Signal',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'}
        }
    }

    combined_fig = {
        'data': [
            go.Scatter(x=t, y=harmonic, mode='lines', name='Harmonic', line=dict(dash='dash')),
            go.Scatter(x=t, y=signal, mode='lines', name='Signal'),
            go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal')
        ],
        'layout': {
            'autosize': True,
            'title': 'Harmonic Function with Noise',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'}
        }
    }

    if split_graph:
        combined_graph_style = {"display": "none"}
        harmonic_graph_style = {"display": "block"}
        signal_graph_style = {"display": "block"} if show_noise else {"display": "none"}
        filtered_graph_style = {"display": "block"} if show_filter else {"display": "none"}
    else:
        combined_graph_style = {"display": "block"}
        harmonic_graph_style = {"display": "none"}
        signal_graph_style = {"display": "none"}
        filtered_graph_style = {"display": "none"}

    return [
        combined_fig, harmonic_graph, signal_fig, filtered_fig,
        combined_graph_style, harmonic_graph_style, signal_graph_style, filtered_graph_style
    ]


app.layout = dbc.Container(
    children=[
        build_header(),
        html.Div(
            children=[
                dbc.Row(
                    children=[
                        *build_settings()
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Spinner(
                            children=[
                                dcc.Graph(id='graph'),
                                html.Div(
                                    className="d-flex flex-column mh-30",
                                    children=[
                                        dcc.Graph(id='harmonic-graph', style={'display': 'none'}),
                                        dcc.Graph(id='signal-graph', style={'display': 'none'}),
                                        dcc.Graph(id='filter-graph', style={'display': 'none'})
                                    ]
                                )
                            ],
                            delay_show=200
                        )
                    ]
                )
            ],
            className="border border-secondary-subtle p-4 rounded-4 shadow-sm"
        )
    ],
    fluid=True,
    className="container-lg"
)

if __name__ == "__main__":
    app.run_server(debug=True)
