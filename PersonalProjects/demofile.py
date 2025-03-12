import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

# Data loading
# dataLink = "https://data.cityofchicago.org/resource/t7ek-mgzi.json?$order=id&$limit=100000&$offset=0"
dataLink = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$order=date%20DESC&$limit=99999&$offset=0"

imagepath = "G:\\Workspace\\Projects\\Github\\DA-Projects\\PersonalProjects\\moroccan-flower.png"
try:
    data = pd.read_json(dataLink)
    print("Data loaded successfully.")
    # adding month column
    data['month'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m')
except Exception as e:
    print("Error loading data:", str(e))

# Create Dash app
app = dash.Dash(__name__)

# Define colors and styles
colors = {
    'background': '#f0f4f8',
    'text': '#212121',
    'primary': '#3f51b5',
    'secondary': '#ff4081',
    'accent': '#00bcd4',
}

# Load Background Pattern
def get_base64_encoded_image(image_path):
    """Encodes an image in base64."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"

try:
    background_pattern = get_base64_encoded_image(imagepath)
    print("Background pattern loaded successfully.")
except FileNotFoundError:
    background_pattern = None
    print("Background pattern not found.")

styles = {
    'title': {
        'textAlign': 'center',
        'color': colors['text'],
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '36px',
        'fontWeight': '600',
        'marginBottom': '30px',
    },
    'dropdown_label': {
        'color': colors['text'],
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '16px',
        'marginBottom': '10px',
        'display': 'block',
        'fontWeight': '600',
    },
    'dropdown_style': {
        'width': '100%',
        'border': '1px solid #ccc',
        'borderRadius': '8px',
        'color': colors['text'],
        'padding': '10px',
    },
    'app_container': {
        'backgroundImage': f'url("{background_pattern}")',
        'backgroundSize': 'cover',
        'padding': '20px',
        'fontFamily': 'Roboto, sans-serif',
        'minHeight': '100vh',
        'backgroundColor': colors['background']
    },
}

# App layout
app.layout = html.Div(
    style=styles['app_container'],
    children=[
        html.H1("Chicago Crime Data Dashboard", style=styles['title']),
        html.Div(style={'marginBottom': '20px'}, children=[
            html.Label("Select Crime Type:", style=styles['dropdown_label']),
            dcc.Dropdown(
                id='crime-type-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(data['primary_type'].unique())],
                value=data['primary_type'].iloc[0],
                style=styles['dropdown_style']
            ),
        ]),
        html.Div(style={'marginBottom': '20px'}, children=[
            html.Label("Select Month:", style=styles['dropdown_label']),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(data['month'].unique())],
                value=data['month'].iloc[0],
                style=styles['dropdown_style']
            ),
        ]),
        html.Div(style={'marginBottom': '20px'}, children=[
            dcc.Checklist(
                id='all-months-checkbox',
                options=[{'label': 'All Months', 'value': 'all'}],
                value=[]
            ),
        ]),
        html.Div(style={'marginBottom': '20px'}, children=[
            dcc.Graph(id='crime-heatmap', style={'height': '600px'})
        ]),
    ]
)

# Callback to update heatmap
@app.callback(
    Output('crime-heatmap', 'figure'),
    [Input('crime-type-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('all-months-checkbox', 'value')]
)
def update_heatmap(selected_crime_type, selected_month, all_months):
    filtered_data = data[data['primary_type'] == selected_crime_type]
    
    if 'all' not in all_months:
        filtered_data = filtered_data[filtered_data['month'] == selected_month]
    
    if filtered_data.empty:
        return go.Figure()  # Return an empty figure if no data is found

    fig = px.density_mapbox(
        filtered_data,
        lat='latitude',
        lon='longitude',
        z='id',  # Using 'id' as a placeholder for density
        radius=10,
        center=dict(lat=41.8781, lon=-87.6298),  # Centered on Chicago
        zoom=10,
        mapbox_style="carto-positron",
        title=f'Heatmap of {selected_crime_type} in {"All Months" if "all" in all_months else selected_month}'
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=colors['text'],
    )
    return fig

# Callback to enable/disable month dropdown
@app.callback(
    Output('month-dropdown', 'disabled'),
    [Input('all-months-checkbox', 'value')]
)
def toggle_month_dropdown(all_months):
    return 'all' in all_months

if __name__ == '__main__':
    app.run_server()  # Run in production mode