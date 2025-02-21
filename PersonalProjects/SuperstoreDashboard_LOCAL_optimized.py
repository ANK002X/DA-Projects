import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
from datetime import datetime

# Constants
DATA_URL = 'https://raw.githubusercontent.com/ANK002X/Datasets/main/superstore.csv'
#TIMEZONE = 'US/Eastern'

# Load and preprocess the dataset
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Order.Date'] = pd.to_datetime(data['Order.Date'])
    data['Ship.Date'] = pd.to_datetime(data['Ship.Date'])
    data['Month'] = data['Order.Date'].dt.month
    data['Year'] = data['Order.Date'].dt.year
    data['shippingTime'] = (data['Ship.Date'] - data['Order.Date']).dt.days
    return data

data = load_data()

# Calculate key metrics
def calculate_metrics(data):
    current_year = data['Year'].max()
    previous_year = current_year - 1
    total_sales = data[data['Year'] == current_year]['Sales'].sum()
    total_orders = data[data['Year'] == current_year]['Order.ID'].nunique()
    total_products_sold = data[data['Year'] == current_year]['Quantity'].sum()
    previous_year_sales = data[data['Year'] == previous_year]['Sales'].sum()
    sales_growth = ((total_sales - previous_year_sales) / previous_year_sales) * 100
    return total_sales, total_orders, total_products_sold, sales_growth

total_sales, total_orders, total_products_sold, sales_growth = calculate_metrics(data)

# Get current time in EDT
def get_current_time():
    edt_tz = pytz.timezone(TIMEZONE)
    current_time_edt = datetime.now(edt_tz)
    return current_time_edt.strftime("%Y-%m-%d %H:%M")

timeVar = get_current_time()

# Country to continent mapping
country_to_continent = {
    # Africa
    'South Africa': 'Africa', 'Democratic Republic of the Congo': 'Africa', 'Niger': 'Africa',
    # ... (rest of the mapping)
}

# Mapping the countries to the respective continents
data['Continent'] = data['Country'].map(country_to_continent)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Global Superstore Dashboard"

# Define the create_tile function
def create_tile(title, value, *colors):
    return html.Div(
        style={'flex': '1', 'margin': '5px'},
        children=[
            html.Div([
                html.H3(title, style={'color': '#FFFFFF'}),
                html.H2(value, style={'color': '#FFFFFF'})
            ], style={
                'background': f'linear-gradient(135deg, {", ".join(colors)})',
                'padding': '20px', 
                'border-radius': '5px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
            })
        ]
    )

# Define the layout
app.layout = html.Div(
    style={'background-color': '#F0F0F0', 'padding': '20px', 'font-family': 'Calibri'},
    children=[
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'color': '#34495E', 'font-family':'Calibri'},
            children=[
                html.Div(style={'flex': '1', 'textAlign': 'center'},
                    children=[
                        html.H1("Global Superstore Dashboard", style={'margin': '0'}),
                    ]
                ),
                html.Span(f'{timeVar}', style={'font-weight':'bold'}),
            ]
        ),
        
        # Overview Tiles
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-between', 'textAlign': 'center', 'width': '100%', 'color': 'Black', 'font-size': 24},
            children=[
                create_tile("Sales YTD", f"${total_sales/1_000_000:.1f}M", '#84F6D5', '#1CA8FF', '#5533FF', '#5E46BF'),
                create_tile("Orders YTD", f"{total_orders}", '#0575E6', '#021B79'),
                create_tile("Products Sold YTD", f"{total_products_sold/1000:.1f}K", '#428bca', '#000000'),
                create_tile("Sales Growth YTD", f"{sales_growth:.2f}%", '#00b388', '#425563'),
            ]
        ),
        
        html.Br(),

        # Accordion for Dropdowns
        html.Button("Dashboard Options", id="toggle-button", n_clicks=0, style={
         'width': '99.8%', 'background-color': '#34495E', 'color': '#FFFFFF', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer', 'font-size': '16px', 'border-radius': '5px', 'margin-bottom': '10px'
        }),
        html.Div(id="accordion-content", children=[
            html.Div([
                dcc.Dropdown(
                    id='dashboard-type',
                    options=[
                        {'label': 'Management Dashboard', 'value': 'Management Dashboard'},
                        {'label': 'Year Based', 'value': 'Year Based'},
                        {'label': '2012 Reports', 'value': '2012 Reports'}
                    ],
                    placeholder='Select Report Type',
                    value='Select Dashboard'
                )
            ], style={'margin-bottom': '20px'}),
            
            html.Div(dcc.Dropdown(
                id='select-year',
                options=[{'label': i, 'value': i} for i in range(2011, 2015)],
                placeholder='Select Year',
                value='Select-year'
            ))
        ], style={
           'width': '97.8%', 'background-color': '#ECF0F1', 'padding': '20px', 'border-radius': '5px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)', 'color': '#404F6E'
        }),

        html.Br(),

        # Chart Display Area
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'justify-content': 'center', 'textAlign': 'center', 'width': '100%', 'color': 'Black', 'font-size': 24})
    ]
)

@app.callback(
    Output("accordion-content", "style"),
    [Input("toggle-button", "n_clicks")],
    [State("accordion-content", "style")]
)
def toggle_accordion(n_clicks, style):
    if n_clicks % 2 == 1:
        style["display"] = "block"
    else:
        style["display"] = "none"
    return style

@app.callback(
    Output('select-year', 'disabled'),
    [Input('dashboard-type', 'value')]
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Year Based' and selected_statistics != 'Management Dashboard'

@app.callback(
    Output('output-container', 'children'),
    [Input('select-year', 'value'),
     Input('dashboard-type', 'value')]
)
def update_output_container(input_year, selected_statistics):
    if input_year and selected_statistics == 'Management Dashboard':
        return create_management_dashboard(data, int(input_year))
    elif selected_statistics == '2012 Reports':
        return create_2012_reports(data)
    elif input_year and selected_statistics == 'Year Based':
        return create_year_based_dashboard(data, int(input_year))

def create_management_dashboard(data, year):
    static_data = data[data['Year'] == year]
    # Create charts
    area_chart = create_area_chart(static_data)
    sunburst_chart = create_sunburst_chart(static_data)
    bubble_chart = create_bubble_chart(static_data)
    funnel_chart = create_funnel_chart(static_data)
    treemap_chart = create_treemap_chart(static_data)
    waterfall_chart = create_waterfall_chart(static_data)
    # Combine all charts into one layout
    return [
        html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'textAlign': 'center', 'width': '100%', 'color': 'Black', 'font-size': 24},
                 children=[
                             html.Div(style={'flex': '1', 'margin': '5px'},children=[dcc.Graph(figure=area_chart),dcc.Graph(figure=waterfall_chart)]),
                             html.Div(style={'flex': '1', 'margin': '5px'},children=[dcc.Graph(figure=treemap_chart),dcc.Graph(figure=sunburst_chart)]),
                             html.Div(style={'flex': '1', 'margin': '5px'},children=[dcc.Graph(figure=bubble_chart),dcc.Graph(figure=funnel_chart)])]
        )
    ]

def create_2012_reports(data):
    static_data = data[data['Year'] == 2012]
    avg_shipping_time = static_data.groupby('Month')['shippingTime'].mean().reset_index()
    R_chart1 = dcc.Graph(
        figure=px.line(avg_shipping_time, x='Month', y='shippingTime', title='Average Shipping Time Trends')
    )
    average_sales = static_data.groupby(['Category'])['Profit'].sum().reset_index()
    R_chart2 = dcc.Graph(
        figure=px.bar(average_sales, x='Category', y='Profit', title="Category-wise Profit in 2012")
    )
    exp_rec = static_data.groupby(['Ship.Mode'])['Profit'].sum().reset_index()
    R_chart3 = dcc.Graph(
        figure=px.pie(exp_rec, values='Profit', names='Ship.Mode', title="Profit by Ship Modes in 2012")
    )
    category_data = static_data.groupby('Category').agg({'Shipping.Cost': 'sum', 'Profit': 'sum', 'Sales': 'sum'}).reset_index()
    R_chart4 = dcc.Graph(
        figure=px.scatter(category_data, x='Shipping.Cost', y='Sales', size='Profit', color='Category',
                          title='Shipping Cost, Sales, Profit by Cateogry in 2012', color_continuous_scale='Plasma')
    )
    return [
        html.Div(className='chart-item', children=[R_chart1, R_chart2]),
        html.Div(className='chart-item', children=[R_chart3, R_chart4])
    ]

def create_year_based_dashboard(data, year):
    yearly_data = data[data['Year'] == year]
    yas = yearly_data.groupby('Month')['Sales'].mean().reset_index()
    Y_chart1 = dcc.Graph(
        figure=px.line(yas, x='Month', y='Sales', title="Monthly Average Product Sales for the year {}".format(year))
    )
    Y_chart2 = dcc.Graph(
        figure=px.scatter(yearly_data, x='Sales', y='Profit', title='Sales and Profit for the year {}'.format(year))
    )
    avr_vdata = yearly_data.groupby(['Category'])['Sales'].sum().reset_index()
    Y_chart3 = dcc.Graph(
        figure=px.bar(avr_vdata, x='Category', y='Sales', title="Sum of Product Sales by Category for the year {}".format(year))
    )
    avr_vdata1 = yearly_data.groupby(['Ship.Mode'])['Sales'].sum().reset_index()
    Y_chart4 = dcc.Graph(
        figure=px.pie(avr_vdata1, values='Sales', names='Ship.Mode', title="Sum of Product Sales by Ship Mode for the year {}".format(year))
    )
    return [
        html.Div(className='chart-item', children=[Y_chart1, Y_chart2]),
        html.Div(className='chart-item', children=[Y_chart3, Y_chart4])
    ]

# Define chart creation functions
def create_area_chart(data):
    sales_profit_time = data.groupby(data['Order.Date'].dt.to_period('M')).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    sales_profit_time['Order.Date'] = sales_profit_time['Order.Date'].dt.to_timestamp()
    return px.area(sales_profit_time, x='Order.Date', y=['Sales', 'Profit'],
                   title='Sales & Profit Over Time', labels={'value': 'Amount', 'x':'Order Date'}, color_discrete_sequence=px.colors.sequential.Plasma)

def create_sunburst_chart(data):
    category_sales = data.groupby(['Category', 'Sub.Category']).agg({'Sales': 'sum'}).reset_index()
    return px.sunburst(category_sales, path=['Category', 'Sub.Category'], values='Sales',
                       title='Top Categories by Sales', color='Sales', color_continuous_scale='RdBu')

def create_bubble_chart(data):
    continent_sales_profit = data.groupby('Continent').agg({'Sales': 'sum', 'Profit': 'sum', 'Order.ID': 'count'}).reset_index()
    return px.scatter(continent_sales_profit, x='Sales', y='Profit', size='Order.ID', color='Continent',
                      title='Sales, Profit, Orders by Continent', size_max=60, color_continuous_scale=px.colors.diverging.Temps)

def create_funnel_chart(data):
    funnel_data = data.groupby('Continent').agg({'Sales': 'sum'}).reset_index()
    return px.funnel(funnel_data, x='Sales', y='Continent', title='Sales Funnel by Continent', color='Sales')

def create_treemap_chart(data):
    segment_sales = data.groupby(['Segment', 'Category']).agg({'Sales': 'sum'}).reset_index()
    return px.treemap(segment_sales, path=['Segment', 'Category'], values='Sales', title='Segment, Category by Sales',
                      color='Sales', color_continuous_scale=px.colors.sequential.Redor)

def create_waterfall_chart(data):
    category_profit = data.groupby('Category').agg({'Profit': 'sum'}).reset_index()
    new_row = pd.DataFrame([['Fashion & Beauty', -70125], ['Pharmacy', 195070]], columns=['Category', 'Profit'])
    category_profit = pd.concat([category_profit, new_row], ignore_index=True)
    return go.Figure(go.Waterfall(
        name="Profit",
        orientation="v",
        x=category_profit['Category'],
        y=category_profit['Profit'],
        connector={"line":{"color":"rgb(63, 63, 63)"}},
    )).update_layout(
        title="Profit Contribution by Category",
        waterfallgap=0.3
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)