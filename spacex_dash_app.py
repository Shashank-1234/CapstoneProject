# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'Cape Canaveral Space Launch Complex 40 (SLC-40)', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'Kennedy Space Center Launch Complex 39A (LC-39A)', 'value': 'KSC LC-39A'},
                                                    {'label': 'Vandenberg Space Force Base Space Launch Complex 4E (SLC-4E)', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'Cape Canaveral Space Launch Complex 40 (LC-40)', 'value': 'CCAFS LC-40'}
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(min_payload, max_payload, 2000, value=[min_payload, max_payload], id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def generate_pie_chart(launch_site):
    
    if(launch_site == 'ALL'):

       # df =  spacex_df[spacex_df['Launch Site']==launch_site]
        df = spacex_df[spacex_df['class']==1]
        print(spacex_df[spacex_df['class']==1])
        fig = px.pie(df, values='class', names='Launch Site', title='Total Success Launches by Site')
        #fig = px.pie(spacex_df, 'Class', names='Launch Site', title='Total Success Launches by Site')

    else :
        df =  spacex_df[spacex_df['Launch Site']==launch_site]
        grapthTitle =  'Total Success Launches at "{}"'.format(launch_site)
        fig = px.pie(df, names='class', title=grapthTitle)
        
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])

def generate_scatter_chart(launch_site, payload_value):
    
    if(launch_site != 'ALL'):
        df =  spacex_df[spacex_df['Launch Site']==launch_site]
        #df = df[df['class']==1]
        df = df[df['Payload Mass (kg)'].between(payload_value[0],payload_value[1])]
        
        
        # Group the data by Month and compute average over arrival delay time.
        # line_data = df.groupby('Booster Version Category')['class'].mean().reset_index()
        line_data = df

        scatterTitle = 'Correlation between Payload and Success for "{}"'.format(launch_site)
        #fig = go.Figure(data=go.Scatter(x=line_data['Payload Mass (kg)'], y=line_data['class'], mode='lines', color='Booster Version Category'))
        fig = px.scatter(line_data, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        fig.update_layout(title=scatterTitle, xaxis_title='Pay Load in (Kgs)', yaxis_title='Class')
    else:
        df =  spacex_df
        #df = df[df['class']==1]
        df = df[df['Payload Mass (kg)'].between(payload_value[0],payload_value[1])]
        
        
        # Group the data by Month and compute average over arrival delay time.
        #line_data = df.groupby('Booster Version Category')['class'].mean().reset_index()
        line_data = df

        scatterTitle = 'Correlation between Payload and Success for "{}"'.format('All Sites')
        #fig = go.Figure(data=go.Scatter(x=line_data['Payload Mass (kg)'], y=line_data['class'], mode='lines', color='Booster Version Category'))
        fig = px.scatter(line_data, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        fig.update_layout(title=scatterTitle, xaxis_title='Pay Load in (Kgs)', yaxis_title='Class')
    
    return fig 
  


# Run the app
if __name__ == '__main__':
    app.run_server()
