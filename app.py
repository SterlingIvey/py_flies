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
    return [{'label': row['Fly Name'], 'value': row['Fly Name']} for _, row in df.iterrows()]

dropdown_options = generate_dropdown_options(df)

# Custom CSS
app.css.append_css({
    'external_url': 'https://cdnjs.cloudfare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
})

custom_css = """
body {
    background-color: #f4f1e3;
    font-family: 'Courier New', monospace;
}
.container {
    background-color: #d9bf77;
    border: 2px solid # 4d3319;
    border-radius: 10px;
    padding: 20px;
    margin: 20px;
}
h1, h2, p {
    color: #4d3319;
}
img {
    border: 2px solid #4d3319;
    border-radius: 5px;
}
"""

# Layout of the app
app.layout = html.Div(className='container', children=[
    html.H1('Fly Reference Guide'),
    dcc.Dropdown(
        id='fly-dropdown',
        options=dropdown_options,
        placeholder='Select a fly',
        style={'background-color': '#d9bf77', 'color': '#4d3319'}
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
    
    fly_data = df[df['Fly Name'] == selected_fly].iloc[0]
    return html.Div([
        html.H2(fly_data['Fly Name']),
        html.Img(src=fly_data['Image URL'], style={'width': '300px'}),
        html.P(f"Type: {fly_data['Type']}"),
        html.P(f"Best Use: {fly_data['Best Use']}")
    ])
    
@app.server.route('/assets/custom.css')
def serve_css():
    return custom_css, 200, {'Content-Type': 'text/css'}

if __name__ == '__main__':
    app.run_server(debug=True)
