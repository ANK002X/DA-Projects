import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Data loading
dataLink = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$order=date%20DESC&$limit=99999&$offset=0"
try:
    data = pd.read_json(dataLink)
    data['month'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m')
except Exception as e:
    print("Error loading data:", str(e))

# Create Dash app
app = dash.Dash(__name__)

# Define colors and styles
colors = {
    'background': '#f0f4f8',
    'text': '#E0E0E0',
}

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
        'color': '#21212',
        'padding': '10px',
        'fontFamily': 'Roboto, sans-serif',
    },
    'app_container': {
        "minHeight": "100vh",
        "justifyContent": "center",
        "alignItems": "center",
        "backgroundColor": "#1A1A2E",  # Dark blue background
        "backgroundImage": "radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px)",
        "backgroundSize": "20px 20px",
        "backgroundRepeat": "repeat",
        'padding': '20px',
        'fontFamily': 'Roboto, sans-serif',
    },
}

# Get the range of data
data_range = f"{data['month'].min()} to {data['month'].max()}"

# App layout
app.layout = html.Div(
    style=styles['app_container'],
    children=[
        html.H1("Chicago Crime Data Dashboard", style=styles['title']),
        html.Div(style={'marginBottom': '20px', 'marginRight': '20px'}, children=[
            html.Label("Select Crime Type:", style=styles['dropdown_label']),
            dcc.Dropdown(
                id='crime-type-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(data['primary_type'].unique())],
                value=data['primary_type'].iloc[0],
                style=styles['dropdown_style']
            ),
        ]),
        html.Div(style={'marginBottom': '20px','marginRight': '20px'}, children=[
            html.Label("Select Month:", style=styles['dropdown_label']),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(data['month'].unique())],
                value=data['month'].iloc[0],
                style=styles['dropdown_style']
            ),
        ]),
        html.Div(style={'marginBottom': '20px', 'color': colors['text']}, children=[
            dcc.Checklist(
                id='all-months-checkbox',
                options=[{'label': f'All Months ({data_range})', 'value': 'all'}],
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
    # If either dropdown is cleared (empty), show all data
    if not selected_crime_type:
        # Show heatmap with all data if crime type is cleared
        filtered_data = data
    else:
        # Filter data based on the selected crime type
        filtered_data = data[data['primary_type'] == selected_crime_type]

    # If month is cleared, show data for all months
    if not selected_month or 'all' in all_months:
        # If "all" months are selected, or month is cleared, show all data
        filtered_data = filtered_data
    else:
        # Filter data based on the selected month
        filtered_data = filtered_data[filtered_data['month'] == selected_month]

    # If no data is available after filtering, return an empty figure
    if filtered_data.empty:
        return go.Figure()  # Return an empty figure if no data is found

    # Determine title based on selections
    crime_title = selected_crime_type if selected_crime_type else "All Crimes"
    month_title = "All Months" if 'all' in all_months or not selected_month else selected_month

    # Generate the heatmap with the filtered data
    fig = px.density_mapbox(
        filtered_data,
        lat='latitude',
        lon='longitude',
        z='id',  # Using 'id' as a placeholder for density
        radius=10,
        center=dict(lat=41.8781, lon=-87.6298),  # Centered on Chicago
        zoom=10,
        mapbox_style="carto-positron",
        title=f'Heatmap of {crime_title} in {month_title}'
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
