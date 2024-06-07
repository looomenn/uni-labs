"""
Course: dpat'4
Lab: 05
"""

import dash
import numpy as np

import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from scipy.signal import iirfilter, filtfilt, welch
from dash import html, dcc, Input, Output, State, ctx

DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(
    __name__,
    title="Harmonic Visualisation",
    external_stylesheets=[dbc.themes.BOOTSTRAP, DBC_CSS]
)

# Dict for default values of each input
DEFAULTS: dict = {
    'amplitude': {'value': 1.0, 'min': 1, 'max': 10.0, 'step': '?', 'category': 'function'},
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

    slider = html.Div(
        id=slider_div_id,
        children=[
            dbc.Label(name.replace('_', ' ').title(), html_for=name),
            dcc.Slider(
                id=name,
                className="dbc p-1",
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
                    {"label": "Noise?", "value": 'show_noise'},
                    {"label": "Filter?", "value": 'show_filter'},
                    {"label": "Custom Filter?", "value": 'show_custom_filter'},
                    {"label": "Split graphs?", "value": 'split_graph'},
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

    def generate_setting_card(name):
        return dbc.Col([
            dbc.Card([
                dbc.CardHeader(f'{name.title()} Settings'),
                dbc.CardBody([
                    dbc.Form(
                        className='d-flex flex-column gap-4',
                        children=[
                            *build_categorial_sliders(DEFAULTS, name)
                        ]
                    )
                ])
            ])
        ])

    function_settings = generate_setting_card("function")
    noise_settings = generate_setting_card("noise")
    filter_settings = generate_setting_card("filter")

    general_settings = dbc.Col(
        md=4,
        children=
        [
            dbc.Card([
                dbc.CardHeader('General Settings'),
                dbc.CardBody([
                    build_switches(),
                    build_buttons()
                ])
            ])
        ]
    )

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
    show_custom_filter = 'show_custom_filter' in switches

    noise_div_style = {'opacity': '0.2'} if not show_noise else {'opacity': '1'}

    filter_order_div_style = {'opacity': '1'} if show_filter or show_custom_filter else {'opacity': '0.2'}
    filter_cutoff_div_style = {'opacity': '1'} if show_filter else {'opacity': '0.2'}

    show_filter_order = show_filter or show_custom_filter

    return [
        not show_noise,
        not show_noise,
        not show_filter_order,
        not show_filter,
        noise_div_style,
        noise_div_style,
        filter_order_div_style,
        filter_cutoff_div_style
    ]


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
        Output('combined-graph', 'figure'),
        Output('harmonic-graph', 'figure'),
        Output('signal-graph', 'figure'),
        Output('filter-graph', 'figure'),
        Output('custom_filter-graph', 'figure'),
        Output('combined-graph-col', 'style'),
        Output('harmonic-graph-col', 'style'),
        Output('signal-graph-col', 'style'),
        Output('filter-graph-col', 'style'),
        Output('custom_filter-graph-col', 'style'),
        Output('combined-graph-col', 'width'),
        Output('harmonic-graph-col', 'width'),
        Output('signal-graph-col', 'width'),
        Output('filter-graph-col', 'width'),
        Output('custom_filter-graph-col', 'width'),
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
    show_custom_filter = 'show_custom_filter' in switches
    split_graph = 'split_graph' in switches

    fs = 100
    t = np.arange(0, 2 * np.pi, 1/fs)

    # noise caching
    noise_key = (noise_mean, noise_cov)
    if noise_key not in noise_cache:
        noise_cache[noise_key] = np.random.normal(noise_mean, noise_cov, t.shape)

    noise = noise_cache[noise_key]
    harmonic = amplitude * np.sin(frequency * t + phase)
    signal = harmonic + noise if show_noise else harmonic

    nyquist_rate = 0.5

    normal_cutoff = cutoff_freq / nyquist_rate
    filter_order = int(filter_order)

    if show_filter:
        b, a = iirfilter(filter_order, normal_cutoff, btype='low', ftype='butter', analog=False)
        filtered_signal = filtfilt(b, a, signal)
    else:
        filtered_signal = signal

    # check for the custom filter
    custom_filtered_signal = custom_filter(signal, filter_order) if show_custom_filter else signal

    # figure creating
    harmonic_fig = create_figure('harmonic', t, harmonic, '#1d77b4')
    signal_fig = create_figure('noise', t, signal, '#ff7f0f')
    filtered_fig = create_figure('filtered signal', t, filtered_signal, '#2ba02b')
    custom_filtered_fig = create_figure('custom filtered signal', t, custom_filtered_signal, '#d62728')

    combined_fig = {
        'data': [
            go.Scatter(x=t, y=harmonic, mode='lines', name='Harmonic', line=dict(dash='dash', color='#1f77b4'))
        ],
        'layout': {
            'autosize': True,
            'title': 'Harmonic Function with Noise',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'},
            'margin': {'l': 30, 'r': 25, 't': 25, 'b': 40}
        }
    }

    if show_noise:
        combined_fig['data'].append(
            go.Scatter(x=t, y=signal, mode='lines', name='Signal', line={'color': '#ff7f0e'})
        )

    if show_filter:
        combined_fig['data'].append(
            go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal', line={'color': '#2ca02c'}),
        )

    if show_custom_filter:
        combined_fig['data'].append(
            go.Scatter(x=t, y=custom_filtered_signal, mode='lines', name='Custom Filtered Signal',
                       line={'color': '#d62728'}),
        )

    graphs = [False, True, show_noise, show_filter, show_custom_filter]
    styles, widths = divide_graphs(graphs, split_graph)

    return [
        combined_fig,
        harmonic_fig,
        signal_fig,
        filtered_fig,
        custom_filtered_fig,
        *styles,
        *widths
    ]


def create_figure(name, x_data, y_data, line_color) -> go.Scatter:
    return {
        'data': [
            go.Scatter(x=x_data, y=y_data, mode='lines', name=name.title(), line={'color': line_color})
        ],
        'layout': {
            'title': name.title(),
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'},
            'margin': {'l': 30, 'r': 25, 't': 25, 'b': 40}
        }
    }


def divide_graphs(show_graphs, split_graph):
    if split_graph:
        col_styles = [{"display": "block"} if show else {"display": "none"} for show in show_graphs]
        enabled_graphs = sum(show_graphs)

        col_width = int(12 / enabled_graphs) if enabled_graphs else 0
        col_widths = [col_width if show else 0 for show in show_graphs]

    else:
        col_styles = [{'display': 'block' if i == 0 else 'none'} for i in range(len(show_graphs))]
        col_widths = [12] * len(show_graphs)

    return col_styles, col_widths


def custom_filter(signal, window_size):
    if window_size % 2 == 0:
        window_size += 1

    half_window = window_size // 2
    filtered_signal = np.zeros_like(signal)

    padded_signal = np.pad(signal, (half_window, half_window), mode='edge')

    for i in range(len(signal)):
        filtered_signal[i] = np.mean(padded_signal[i:i + window_size])

    return filtered_signal


GRAPHS: dict = {
    'combined-graph': {'style': {'display': 'block'}},
    'harmonic-graph': {'style': {'display': 'none'}},
    'signal-graph': {'style': {'display': 'none'}},
    'filter-graph': {'style': {'display': 'none'}},
    'custom_filter-graph': {'style': {'display': 'none'}}
}

app.layout = dbc.Container(
    children=[
        build_header(),
        html.Div(
            className="border border-secondary-subtle p-4 rounded-4 shadow-sm",
            children=[
                dbc.Row(
                    children=[
                        *build_settings()
                    ]
                ),
                dbc.Row(
                    className="pt-3",
                    children=[
                        dbc.Col(
                            id=name + '-col',
                            width=12,
                            style=config['style'],
                            children=[
                                dbc.Spinner(
                                    color='primary',
                                    delay_show=100,
                                    children=[dcc.Graph(id=name)]
                                )
                            ]
                        )
                        for name, config
                        in GRAPHS.items()
                    ]
                )
            ],
        )
    ],
    fluid=True,
    className="container-lg"
)

if __name__ == "__main__":
    app.run_server(debug=True)
