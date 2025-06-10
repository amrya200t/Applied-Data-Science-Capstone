# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

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
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
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
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0 kg', 1000: '1000 kg', 2000: '2000 kg',
                                            3000: '3000 kg', 4000: '4000 kg', 5000: '5000 kg',
                                            6000: '6000 kg', 7000: '7000 kg', 8000: '8000 kg',
                                            9000: '9000 kg', 10000: '10000 kg'},
                                    value=[min_payload, max_payload] # Default to full range
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Calculate total success and failure for all sites
        fig = px.pie(spacex_df,
                     values='class',
                     names='Launch Site',
                     title='Total Success Launches By Site (All Sites)')
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Calculate success (class=1) and failure (class=0) counts for the selected site
        fig = px.pie(filtered_df,
                     names='class', # Names will be '0' for failure, '1' for success
                     title=f'Success vs. Failed Launches for site {entered_site}',
                     color='class', # Color the slices based on success (1) or failure (0)
                     color_discrete_map={0: 'red', 1: 'green'} # Assign specific colors
                    )
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range # Unpack the payload range values
    # Filter the DataFrame based on payload range
    filtered_payload_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_payload_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version', # Color points by Booster Version
                         title='Correlation between Payload and Success for All Sites (Filtered by Payload Range)')
    else:
        # Filter the DataFrame further for the selected site
        filtered_site_payload_df = filtered_payload_df[
            filtered_payload_df['Launch Site'] == entered_site
        ]
        fig = px.scatter(filtered_site_payload_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version', # Color points by Booster Version
                         title=f'Correlation between Payload and Success for site {entered_site} (Filtered by Payload Range)')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
