import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Load data
def load_data():
    try:
        return pd.read_csv('flies_info.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=['Fly Name', 'Type', 'Best Use', 'Image URL'])
    
df = load_data()

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate dropdown options
def generate_dropdown_options(df):
    return [{'label': row['Fly Name'], 'value': row['Fly Name']} for _,
row in df.iterrows()]

dropdown_options = generate_dropdown_options(df)

# Layout of the app
app.layout = html.Div(className='container', children=[
    html.H1('Fly Reference Guide'),
    html.Div(className='dropdown-container', children=[
        dcc.Dropdown(
        id='fly-dropdown',
        options=dropdown_options,
        placeholder='Select a fly',
        )
    ]),
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
    
    fly_data = df[df['Fly Name'] == selected_fly].iloc[0]
    return html.Div([
        html.H2(fly_data['Fly Name']),
        html.Img(src=fly_data['Image URL'], style={'width': '300px'}),
        html.P(f"Type: {fly_data['Type']}"),
        html.P(f"Best Use: {fly_data['Best Use']}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
