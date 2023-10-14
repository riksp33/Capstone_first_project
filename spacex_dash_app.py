# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                               dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value='ALL',
                                            placeholder="Dropdown menu for selecting launch site",
                                            searchable=True
                                            ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),



                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0 , max= 10000, step = 1000,
                                                marks={0:'0' ,
                                                         2500 : '2500',
                                                         5000:'5000',
                                                         7500:'7500'
                                                         },
                                                value = [min_payload , max_payload]),



                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])











@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success lauches per site')
        return fig
    else:
        sitio_filtro = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(sitio_filtro['class'] ,names = 'class',
        title = 'Total succes launches for site ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def get_scatter(entered_site , slider):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1]) ]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df , x = 'Payload Mass (kg)' , y = 'class' , color = 'Booster Version Category')
        return fig
    else:
        sitio_filtro = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(sitio_filtro , x = 'Payload Mass (kg)' , y = 'class' , color = 'Booster Version Category')
        return fig




# Run the app
if __name__ == '__main__':
    app.run_server()
