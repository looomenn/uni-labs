"""
Course: dpat
Lab: 06
"""

import dash
import numpy as np

import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dash import html, dcc, Input, Output, State, ctx

DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(
    __name__,
    title="Numpy",
    external_stylesheets=[dbc.themes.BOOTSTRAP, DBC_CSS]
)


def build_sliders():

    def get_slider(name, slider_id, min_value, max_value, step=1.0):
        return html.Div([
            dbc.Label(name, html_for=slider_id),
            dcc.Slider(
                id=slider_id,
                className='dbc',
                min=min_value,
                max=max_value,
                value=min_value,
                step=step,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ])

    k_slider = get_slider("K Value", "k_slider", 1, 5)
    b_slider = get_slider("B Value", "b_slider", 1, 5)
    n_points = get_slider("N Points", "n_points", 100, 200, step=20)
    noise_level = get_slider("Noise Level", "noise_lvl", 2, 5),
    grad_learning_rate = get_slider("Learning Rate", "learning_rate",0, 0.5, 0.01),
    grad_n_iter = get_slider("Number of iterations", "n_iter", 500, 6000, 100),

    return [k_slider, b_slider, n_points, noise_level, grad_learning_rate, grad_n_iter]


def build_header():
    return html.Div(
        children=[
            html.H4(app.title),
        ],
        className="pt-3 pb-3"
    )


def build_settings():
    return dbc.Card([
        dbc.CardHeader('Settings'),
        dbc.CardBody([
            dbc.Form(
                id='settings',
                children=[
                    *build_sliders()
                ]
            )
        ])
    ])


def build_output():
    return dbc.Card([
        dbc.CardHeader('Output'),
        dbc.CardBody(
            id='output-cont',
            children=[
                html.P('No data to display')
            ]
        )
    ])


@app.callback(
    [
        Output('scatter-plot', 'figure'),
        Output('error-plot', 'figure'),
        Output('output-cont', 'children')
    ],
    [
        Input('k_slider', 'value'),
        Input('b_slider', 'value'),
        Input('n_points', 'value'),
        Input('noise_lvl', 'value'),
        Input('learning_rate', 'value'),
        Input('n_iter', 'value'),
    ]
)
def update_figure(k_value, b_value, n_points, noise_lvl, learning_rate, num_iters):

    x, y = generate_data(k_value, b_value, n_points, noise_lvl)

    k_squares, b_squares = squares(x, y)
    k_gradient, b_gradient, errors = gradient(x, y, learning_rate, num_iters)

    polyfit_params = np.polyfit(x, y, 1)

    scatter_fig = {
        'data': [
            go.Scatter(x=x, y=y, mode='markers', name='Generated Data'),
            go.Scatter(x=x, y=k_value * x + b_value, mode='lines', name='True Line'),
            go.Scatter(x=x, y=k_squares * x + b_squares, mode='lines', name='Least Squares Line'),
            go.Scatter(x=x, y=polyfit_params[0] * x + polyfit_params[1], mode='lines', name='Polyfit Line'),
            go.Scatter(x=x, y=k_gradient * x + b_gradient, mode='lines', name='Gradient Descent Line')
        ],
        'layout': {
            'autosize': True,
            'title': 'Regression Lines',
            'xaxis': {'title': 'x'},
            'yaxis': {'title': 'y'},
        }
    }

    error_fig = {
        'data': [
            go.Scatter(x=list(range(len(errors))), y=errors, mode='lines', name='Error')
        ],
        'layout': {
            'title': 'Error vs Iterations',
            'xaxis': {'title': 'Number of Iterations'},
            'yaxis': {'title': 'Error'}
        }
    }

    output = html.Div([
        html.P(f'Squares: {k_squares}, {b_squares}'),
        html.P(f'Gradient: {k_gradient}, {b_gradient}'),
        html.P(f'Polyfit: {polyfit_params}'),
        html.P(f'Errors: {errors[:5]}'),
    ])

    return [scatter_fig, error_fig, output]


def gradient(x, y, learning_rate=0.01, n_iter=1000):
    k_est = 0.0
    b_est = 0.0
    n = len(x)
    errors = []

    for _ in range(n_iter):
        y_pred = k_est * x + b_est
        error = y - y_pred
        cost = (1 / n) * np.sum(error ** 2)
        errors.append(cost)

        k_grad = -(2 / n) * np.sum(x * error)
        b_grad = -(2 / n) * np.sum(error)

        k_est -= learning_rate * k_grad
        b_est -= learning_rate * b_grad

    return k_est, b_est, errors


def squares(x, y):
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    num = np.sum((x - x_mean) * (y - y_mean))
    den = np.sum((x - x_mean) ** 2)

    k_est = num / den
    b_est = y_mean - k_est * x_mean

    return k_est, b_est


def generate_data(k, b, n_points=100, noise_level=2):
    np.random.seed(0)
    x = np.random.uniform(-10, 10, n_points)
    noise = np.random.normal(0, noise_level, n_points)
    y = k * x + b + noise
    return x, y


app.layout = dbc.Container(
    fluid=True,
    className="container-lg",
    children=[
        build_header(),
        html.Div(
            className="border border-secondary-subtle p-4 rounded-4 shadow-sm",
            children=[
                dbc.Row([
                    dbc.Col(
                        md=3,
                        className='d-flex flex-column gap-4',
                        children=[
                            build_settings(),
                            build_output()
                        ]
                    ),
                    dbc.Col(
                        children=[
                            dcc.Graph(id='scatter-plot', config={'displayModeBar': False}),
                            dcc.Graph(id='error-plot', config={'displayModeBar': False})
                        ]
                    )
                ])
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
