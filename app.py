import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from predict import predict
from train import train_solar_prediction_model

# new line to test CICD ...
# train solar prediciton model
train_solar_prediction_model()
# trigure prediction pipeline
predict()

app = dash.Dash(__name__)
# Sample df
df = pd.read_pickle('artifacts/04_model/xgboost_solar_prediction.pickle')


app.layout = html.Div([
    html.H3('Enter the number of days for the forecast'),
    dcc.Input(id='num-days-input', type='number',
              placeholder='Enter number of days', value=1, max=7),
    dcc.Graph(id='time-series-plot')
])


@callback(
    Output('time-series-plot', 'figure'),
    Input('num-days-input', 'value')
)
def update_graph(num_days):
    if num_days is None:
        num_days = 1

    # Convert num_days to an integer if it's not already
    num_days = int(num_days)

    # Get today's date
    current_time = df.index[0]

    # Calculate end date based on selected days in the future
    end_date = current_time + pd.Timedelta(days=num_days)  # timedelta(days=num_days)

    # Filter df based on end date (assuming 'date' is a datetime)
    filtered_df = df.loc[:end_date]
    filtered_df = filtered_df.reset_index()

    # Create the plot
    fig = go.Figure(data=[go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['prediction'])],
        layout=go.Layout(yaxis=dict(title='W')))

    current_hourly_time = current_time.strftime("%Y-%m-%d %H")
    title = f'+ {num_days}DAY Solar pannel energy forecast \
        \n [UTC: {current_hourly_time}]'

    fig.update_layout(title=title)
    return fig


if __name__ == '__main__':
    # train solar prediciton model
    # train_solar_prediction_model()
    # trigure prediction pipeline
    # predict()

    # if debug=True then script is run twice, which is annoying
    app.run_server(host="0.0.0.0", port=5002)
