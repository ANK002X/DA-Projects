import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pytz
from datetime import datetime

# Load the dataset
data = pd.read_csv('https://raw.githubusercontent.com/ANK002X/Datasets/main/superstore.csv')

# Convert Order Date to datetime
data['Order.Date'] = pd.to_datetime(data['Order.Date'])

# Extract year and month from the Order Date column
data['Month'] = data['Order.Date'].dt.month
data['Year'] = data['Order.Date'].dt.year

# Calculate key metrics
total_sales = data[data['Year'] == data['Year'].max()]['Sales'].sum()
total_orders = data[data['Year'] == data['Year'].max()]['Order.ID'].nunique()
total_products_sold = data[data['Year'] == data['Year'].max()]['Quantity'].sum()

# Calculate Sales Growth of current year
previous_year_sales = data[data['Year'] == data['Year'].max() - 1]['Sales'].sum()
current_year_sales = data[data['Year'] == data['Year'].max()]['Sales'].sum()
sales_growth = ((current_year_sales - previous_year_sales) / previous_year_sales) * 100

# Calculate the shipping time
data['Ship.Date'] = pd.to_datetime(data['Ship.Date'])
data['Order.Date'] = pd.to_datetime(data['Order.Date'])

# Extract year and month from the Order Date column
data['Order.Date'] = pd.to_datetime(data['Order.Date'])
data['Month'] = data['Order.Date'].dt.month
data['Year'] = data['Order.Date'].dt.year
data['shippingTime'] = (data['Ship.Date'] - data['Order.Date']).dt.days
data['shippingTime']

# Get time
# Set the timezone to Eastern Daylight Time (EDT)
edt_tz = pytz.timezone('US/Eastern')

# Get the current time in EDT
current_time_edt = datetime.now(edt_tz)
timeVar = current_time_edt.strftime("%Y-%m-%d %H:%M")

# Dictionary with correct country-to-continent mapping
country_to_continent = {
    # Africa
    'South Africa': 'Africa', 'Democratic Republic of the Congo': 'Africa', 'Niger': 'Africa',
    'Madagascar': 'Africa', 'Egypt': 'Africa', 'Morocco': 'Africa', 'Cameroon': 'Africa',
    'Ghana': 'Africa', 'Chad': 'Africa', 'Kenya': 'Africa', 'Djibouti': 'Africa',
    'Zambia': 'Africa', 'Angola': 'Africa', 'Tanzania': 'Africa', 'Sierra Leone': 'Africa',
    'Liberia': 'Africa', 'Guinea-Bissau': 'Africa', 'Somalia': 'Africa', 'Senegal': 'Africa',
    'Tunisia': 'Africa', 'Mali': 'Africa', 'Algeria': 'Africa', 'Benin': 'Africa',
    'Ethiopia': 'Africa', 'Libya': 'Africa', 'Mozambique': 'Africa', 'Togo': 'Africa',
    "Cote d'Ivoire": 'Africa', 'Lesotho': 'Africa', 'Rwanda': 'Africa', 'Sudan': 'Africa',
    'Guinea': 'Africa', 'Republic of the Congo': 'Africa', 'Namibia': 'Africa',
    'Central African Republic': 'Africa', 'Eritrea': 'Africa', 'Mauritania': 'Africa',
    'Swaziland': 'Africa', 'Gabon': 'Africa', 'Equatorial Guinea': 'Africa',
    'South Sudan': 'Africa', 'Burundi': 'Africa', 'Nigeria': 'Africa', 'Uganda': 'Africa',
    'Zimbabwe': 'Africa',

    # North America
    'Canada': 'North America', 'United States': 'North America', 'Mexico': 'North America',

    # Caribbean
    'Cuba': 'North America', 'Trinidad and Tobago': 'North America', 'Guadeloupe': 'North America',
    'Jamaica': 'North America', 'Martinique': 'North America', 'Barbados': 'North America',
    'Dominican Republic': 'North America', 'Haiti': 'North America',

    # Central and South America
    'El Salvador': 'South America', 'Guatemala': 'South America', 'Nicaragua': 'South America',
    'Panama': 'South America', 'Honduras': 'South America', 'Brazil': 'South America',
    'Colombia': 'South America', 'Chile': 'South America', 'Uruguay': 'South America',
    'Bolivia': 'South America', 'Ecuador': 'South America', 'Paraguay': 'South America',
    'Argentina': 'South America', 'Peru': 'South America', 'Venezuela': 'South America',

    # Europe
    'France': 'Europe','Italy': 'Europe','Spain': 'Europe','Portugal': 'Europe','Germany': 'Europe',
    'Austria': 'Europe', 'Belgium': 'Europe','Switzerland': 'Europe', 'Netherlands':
    'Europe', 'United Kingdom': 'Europe', 'Norway': 'Europe', 'Finland': 'Europe',
    'Sweden': 'Europe', 'Denmark': 'Europe','Ireland': 'Europe', 'Russia': 'Europe',
    'Poland': 'Europe', 'Ukraine': 'Europe', 'Bulgaria': 'Europe', 'Czech Republic': 'Europe',
    'Hungary': 'Europe', 'Romania': 'Europe', 'Belarus': 'Europe', 'Georgia': 'Europe',
    'Croatia': 'Europe', 'Israel': 'Europe', 'Montenegro': 'Europe', 'Moldova': 'Europe',
    'Estonia': 'Europe', 'Albania': 'Europe', 'Slovakia': 'Europe',
    'Bosnia and Herzegovina': 'Europe', 'Armenia': 'Europe', 'Slovenia': 'Europe',
    'Macedonia': 'Europe', 'Turkey': 'Europe', 'Lithuania': 'Europe',

    # Asia
    'India': 'Asia', 'Bangladesh': 'Asia', 'Afghanistan': 'Asia', 'Nepal': 'Asia',
    'Sri Lanka': 'Asia', 'Pakistan': 'Asia', 'Hong Kong': 'Asia', 'China': 'Asia',
    'Japan': 'Asia', 'Taiwan': 'Asia', 'South Korea': 'Asia', 'Mongolia': 'Asia',
    'Malaysia': 'Asia', 'Singapore': 'Asia', 'Cambodia': 'Asia', 'Thailand': 'Asia',
    'Myanmar (Burma)': 'Asia', 'Vietnam': 'Asia', 'Philippines': 'Asia', 'Indonesia': 'Asia',
    'Kazakhstan': 'Asia', 'Uzbekistan': 'Asia', 'Kyrgyzstan': 'Asia', 'Bahrain': 'Asia',
    'United Arab Emirates': 'Asia', 'Qatar': 'Asia', 'Saudi Arabia': 'Asia', 'Iran': 'Asia',
    'Iraq': 'Asia', 'Jordan': 'Asia', 'Lebanon': 'Asia', 'Syria': 'Asia', 'Yemen': 'Asia',
    'Azerbaijan': 'Asia', 'Armenia': 'Asia', 'Turkey': 'Asia', 'Turkmenistan': 'Asia',
    'Tajikistan': 'Asia', 'Mongolia': 'Asia',

    # Oceania
    'New Zealand': 'Oceania', 'Australia': 'Oceania', 'Papua New Guinea': 'Oceania',

    # Other
    'South Sudan': 'Africa', 'Sudan': 'Africa', 'Mauritania': 'Africa', 'Central African Republic': 'Africa'
}

# Mapping the countries to the respective continents using the dictionary 'country_to_continent'
data['Continent'] = data['Country'].map(country_to_continent)

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Global Superstore Dashboard"

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
                html.Div(
                    style={'flex': '1', 'margin': '5px'},
                    children=[
                        html.Div([
                            html.H3("Sales YTD", style={'color': '#FFFFFF'}),
                            html.H2(f"${total_sales/1_000_000:.1f}M", style={'color': '#FFFFFF'})
                        ], style={
                           'background':'linear-gradient(135deg, #84F6D5, #1CA8FF, #5533FF, #5E46BF)',
                            'padding': '20px', 
                            'border-radius': '5px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        })
                    ]
                ),
                
                html.Div(
                    style={'flex': '1', 'margin': '5px'},
                    children=[
                        html.Div([
                            html.H3("Orders YTD", style={'color': '#ECF0F1'}),
                            html.H2(f"{total_orders}", style={'color': '#FFFFFF'})
                        ], style={
                            'background':'linear-gradient(135deg, #0575E6, #021B79)',
                            'padding': '20px',  
                            'border-radius': '5px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        })
                    ]
                ),
                
                html.Div(
                    style={'flex': '1', 'margin': '5px'},
                    children=[
                        html.Div([
                            html.H3("Products Sold YTD", style={'color': '#ECF0F1'}),
                            html.H2(f"{total_products_sold/1000:.1f}K", style={'color': '#FFFFFF'})
                        ], style={
                            'background':'linear-gradient(135deg, #428bca, #000000)',
                            'padding': '20px', 
                            'border-radius': '5px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        })
                    ]
                ),
                
                html.Div(
                    style={'flex': '1', 'margin': '5px'},
                    children=[
                        html.Div([
                            html.H3("Sales Growth YTD", style={'color': '#ECF0F1'}),
                            html.H2(f"{sales_growth:.2f}%", style={'color': '#FFFFFF'})
                        ], style={
                            'background': 'linear-gradient(135deg, #00b388, #425563)',
                            'padding': '20px', 
                            'border-radius': '5px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                        })
                    ]
                ),
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

# Define the callback functions
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
        static2014_data = data[data['Year'] == int(input_year)]

        # 1. Sales & Profit Over Time (Area Chart)
        sales_profit_time = static2014_data.groupby(static2014_data['Order.Date'].dt.to_period('M')).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
        sales_profit_time['Order.Date'] = sales_profit_time['Order.Date'].dt.to_timestamp()
        area_chart = px.area(sales_profit_time, x='Order.Date', y=['Sales', 'Profit'],
                             title='Sales & Profit Over Time', labels={'value': 'Amount', 'x':'Order Date'}, color_discrete_sequence=px.colors.sequential.Plasma)

        # 2. Top Categories by Sales (Sunburst Chart)
        category_sales = static2014_data.groupby(['Category', 'Sub.Category']).agg({'Sales': 'sum'}).reset_index()
        sunburst_chart = px.sunburst(category_sales, path=['Category', 'Sub.Category'], values='Sales',
                                     title='Top Categories by Sales', color='Sales', color_continuous_scale='RdBu')

        # 3. Sales vs. Profit by Continent (Bubble Chart)
        continent_sales_profit = static2014_data.groupby('Continent').agg({'Sales': 'sum', 'Profit': 'sum', 'Order.ID': 'count'}).reset_index()
        bubble_chart = px.scatter(continent_sales_profit, x='Sales', y='Profit', size='Order.ID', color='Continent',
                                  title='Sales, Profit, Orders by Continent', size_max=60, color_continuous_scale=px.colors.diverging.Temps)

        # 4. Sales Funnel (Funnel Chart)
        funnel_data = static2014_data.groupby('Continent').agg({'Sales': 'sum'}).reset_index()
        funnel_chart = px.funnel(funnel_data, x='Sales', y='Continent', title='Sales Funnel by Continent', color='Sales')

        # 5. Segment, Category by Sales (Treemap)
        segment_sales = static2014_data.groupby(['Segment', 'Category']).agg({'Sales': 'sum'}).reset_index()
        treemap_chart = px.treemap(segment_sales, path=['Segment', 'Category'], values='Sales', title='Segment, Category by Sales',
                                   color='Sales', color_continuous_scale=px.colors.sequential.Redor)

        # 6. Profit Contribution by Category (Waterfall chart)
        category_profit = static2014_data.groupby('Category').agg({'Profit': 'sum'}).reset_index()

        # add a dummy row in profit: Fashion & Beauty, -1012550
        new_row = pd.DataFrame([['Fashion & Beauty', -70125], ['Pharmacy', 195070]], columns=['Category', 'Profit'])

        new_row

        # Concatenate the new row to the original DataFrame
        category_profit = pd.concat([category_profit, new_row], ignore_index=True)
        category_profit

        waterfall_chart = go.Figure(go.Waterfall(
            name="Profit",
            orientation="v",
            x=category_profit['Category'],
            y=category_profit['Profit'],
            connector={"line":{"color":"rgb(63, 63, 63)"}},
        ))

        waterfall_chart.update_layout(
            title="Profit Contribution by Category",
            waterfallgap=0.3
        )


        # Combine all charts into one layout
        return [
            html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'textAlign': 'center', 'width': '100%', 'color': 'Black', 'font-size': 24},
                     children=[
                                 html.Div(style={'flex': '1', 'margin': '5px'},children=[dcc.Graph(figure=area_chart),dcc.Graph(figure=waterfall_chart)]),
                                 html.Div(style={'flex': '1', 'margin': '5px'},children=[dcc.Graph(figure=treemap_chart),dcc.Graph(figure=sunburst_chart)]),
                                 html.Div(style={'flex': '1', 'margin': '5px'},children=[dcc.Graph(figure=bubble_chart),dcc.Graph(figure=funnel_chart)])]
            )
        ]

    elif selected_statistics == '2012 Reports':
        # Example of 2012 Reports
        static2012_data = data[data['Year'] == 2012]
        avg_shipping_time = static2012_data.groupby('Month')['shippingTime'].mean().reset_index()
        
        R_chart1 = dcc.Graph(
            figure=px.line(avg_shipping_time, x='Month', y='shippingTime', title='Average Shipping Time Trends')
        )
        
        average_sales = static2012_data.groupby(['Category'])['Profit'].sum().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Category', y='Profit', title="Category-wise Profit in 2012")
        )
        
        exp_rec = static2012_data.groupby(['Ship.Mode'])['Profit'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Profit', names='Ship.Mode', title="Profit by Ship Modes in 2012")
        )
        
        category_data = static2012_data.groupby('Category').agg({'Shipping.Cost': 'sum', 'Profit': 'sum', 'Sales': 'sum'}).reset_index()
        R_chart4 = dcc.Graph(
            figure=px.scatter(category_data, x='Shipping.Cost', y='Sales', size='Profit', color='Category',
                              title='Shipping Cost, Sales, Profit by Cateogry in 2012', color_continuous_scale='Plasma')
        )
        
        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2]),
            html.Div(className='chart-item', children=[R_chart3, R_chart4])
        ]

    elif (input_year and selected_statistics == 'Year Based'):
        # Example of Year Based charts
        yearly_data = data[data['Year'] == int(input_year)]
        
        yas = yearly_data.groupby('Month')['Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Month', y='Sales', title="Monthly Average Product Sales for the year {}".format(input_year))
        )
        
        Y_chart2 = dcc.Graph(
            figure=px.scatter(yearly_data, x='Sales', y='Profit', title='Sales and Profit for the year {}'.format(input_year))
        )
        
        avr_vdata = yearly_data.groupby(['Category'])['Sales'].sum().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Category', y='Sales', title="Sum of Product Sales by Category for the year {}".format(input_year))
        )
        
        avr_vdata1 = yearly_data.groupby(['Ship.Mode'])['Sales'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(avr_vdata1, values='Sales', names='Ship.Mode', title="Sum of Product Sales by Ship Mode for the year {}".format(input_year))
        )
        
        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2]),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4])
        ]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
