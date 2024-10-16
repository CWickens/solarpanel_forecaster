import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from predict import predict
from train import train_solar_prediction_model


def load_solar_forecast_data():
    df = pd.read_pickle('artifacts/04_model/xgboost_solar_prediction.pickle')
    return df


# Constants
FIGURE_TEMPLATE = 'CYBORG'
APP_THEME = dbc.themes.CYBORG
MAX_FORECAST_DAYS = 7
DEFAULT_FORECAST_DAYS = 1
PORT = 5002

# Load figure template
load_figure_template(FIGURE_TEMPLATE)

# Initialize data
train_solar_prediction_model()
predict()
df = load_solar_forecast_data()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[APP_THEME])

# App layout
app.layout = html.Div([
    html.H1('Home solar panel energy forecaster'),
    html.Hr(),
    html.H6('Number of days to forecast'),
    dcc.Input(
        id='num-days-input',
        type='number',
        placeholder='Enter number of days',
        value=DEFAULT_FORECAST_DAYS,
        max=MAX_FORECAST_DAYS
    ),
    html.Button('Update Prediction', id='update-button', n_clicks=0),
    dcc.Graph(id='time-series-plot')
])


@callback(
    Output('time-series-plot', 'figure'),
    Input('num-days-input', 'value'),
    Input('update-button', 'n_clicks')
)
def update_graph(num_days, n_clicks):
    global df
    if n_clicks > 0:
        predict()
        df = load_solar_forecast_data()

    num_days = int(num_days or DEFAULT_FORECAST_DAYS)
    current_time = df.index[0]
    end_date = current_time + pd.Timedelta(days=num_days)

    filtered_df = df.loc[:end_date].reset_index()

    fig = go.Figure(data=[go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['prediction'],
        fill='tozeroy'
    )])

    fig.update_layout(
        template='plotly_dark',
        yaxis_title='W',
        yaxis=dict(range=[0, max(filtered_df['prediction'].max(), 3500)]),
        title=f'Solar energy forecast (+ {num_days} DAY)',
        title_font=dict(size=25, family='Arial, sans-serif', color='white'),
        title_x=0.5
    )

    return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=PORT)
