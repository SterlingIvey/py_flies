import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Load data
try:
    df = pd.read_csv('flies_info.csv')
except Exception as e:
    print(f"Error loading CSV: {e}")
    df = pd.DataFrame(columns=['Fly Name', 'Type', 'Best Use', 'Image URL'])

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1('Fly Reference Guide'),
    dcc.Dropdown(
        id='fly-dropdown',
        options=[{'label': row['Fly Name'], 'value': row['Fly Name']}
for _, row in df.iterrows()],
        placeholder='Select a fly'
    ),
    html.Div(id='fly-info')
])

# Callback to update the fly information
@app.callback(
    Output('fly-info', 'children'),
    Input('fly-dropdown', 'value')
)
def display_fly_info(selected_fly):
    if selected_fly is None:
        return html.Div()
    
    try:
        fly_data = df[df['Fly Name'] == selected_fly].iloc[0]
        print(f"Selected Fly Data: {fly_data}")

        return html.Div([
            html.H2(fly_data['Fly Name']),
            html.Img(src=fly_data['Image URL'], style={'width': '300px'}),
            html.P(f"Type: {fly_data['Type']}"),
            html.P(f"Best Use: {fly_data['Best Use']}")
    ])
    except Exception as e:
        print(f"Error is callback: {e}")
        return html.Div({
            html.H2("Error loading fly data"),
            html.P(str(e))
        })
    
if __name__ == '__main__':
    app.run_server(debug=True)
