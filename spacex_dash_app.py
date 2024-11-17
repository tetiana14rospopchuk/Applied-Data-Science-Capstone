# # Import required libraries
# import pandas as pd
# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
# import plotly.express as px

# # Read the airline data into pandas dataframe
# spacex_df = pd.read_csv("spacex_launch_dash.csv")
# max_payload = spacex_df['Payload Mass (kg)'].max()
# min_payload = spacex_df['Payload Mass (kg)'].min()

# # Create a dash application
# app = dash.Dash(__name__)

# # Create an app layout
# app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
#                                         style={'textAlign': 'center', 'color': '#503D36',
#                                                'font-size': 40}),
#                                 # TASK 1: Add a dropdown list to enable Launch Site selection
#                                 # The default select value is for ALL sites
#                                 # dcc.Dropdown(id='site-dropdown',...)
#                                 html.Br(),

#                                 # TASK 2: Add a pie chart to show the total successful launches count for all sites
#                                 # If a specific launch site was selected, show the Success vs. Failed counts for the site
#                                 html.Div(dcc.Graph(id='success-pie-chart')),
#                                 html.Br(),

#                                 html.P("Payload range (Kg):"),
#                                 # TASK 3: Add a slider to select payload range
#                                 #dcc.RangeSlider(id='payload-slider',...)

#                                 # TASK 4: Add a scatter chart to show the correlation between payload and launch success
#                                 html.Div(dcc.Graph(id='success-payload-scatter-chart')),
#                                 ])

# # TASK 2:
# # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# # TASK 4:
# # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# # Run the app
# if __name__ == '__main__':
#     app.run_server()


import pandas as pd
import dash
from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # Dropdown for site selection
    html.Br(),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),

    # Pie chart for successful/failed launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # Slider for payload range selection
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=max_payload,
        step=1000,
        marks={0: '0', max_payload: str(max_payload)},
        value=[min_payload, max_payload]
    ),
    # Scatter chart for success vs payload
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2 Callback: Update pie chart based on selected site
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
# def get_pie_chart(entered_site):
#     filtered_df = spacex_df
#     if entered_site == 'ALL':
#         fig = px.pie(data, values='class', 
#         names='pie chart names', 
#         title='title')
#         return fig
#     else:

def update_pie_chart(selected_site):
    filtered_df = spacex_df if selected_site == 'ALL' else spacex_df[spacex_df['Launch Site'] == selected_site]
    success_counts = filtered_df.groupby('class').size().reset_index(name='count')
    success_counts['Launch Outcome'] = success_counts['class'].map({1: 'Success', 0: 'Failure'})
    
    fig = px.pie(success_counts, names='Launch Outcome', values='count', title=f"Launch Success vs Failure for {selected_site}")
    return fig

# Task 4 Callback: Update scatter plot based on selected site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Launch Site',
                     title=f"Payload vs Launch Success for {selected_site}",
                     labels={'class': 'Launch Success (1=Success, 0=Failure)'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

