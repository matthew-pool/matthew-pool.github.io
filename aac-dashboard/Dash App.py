#!/usr/bin/env python
# coding: utf-8

# In[ ]:


""" This dashboard uses a my mongo_crud.py module to show an interactive data table with an
    unfiltered view of the Austin Animal Center Outcomes dataset and a corresponding geolocation chart
    to display location, name, and breed of the selected row in the data table.
"""

## NOTE
# Water Rescue (Intact Female @26-156 weeks): Labrador Retriever Mix, Chesapeake Bay Retriever, Newfoundland
# Mountain or Wilderness Rescue (Intact Male @26-156 weeks): German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, Rottweiler
# Disaster Rescue or Individual Tracking (Intact Male @20-300 weeks): Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler


# Setup the Jupyter version of Dash
import base64
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table, no_update
from dash.dependencies import Input, Output, State
from dash import callback_context
from dash.exceptions import PreventUpdate

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime

from mongo_crud import MongoCrud


###########################
# Model
###########################

# Database connection instance
username = "aacuser"
password = "M22"
host = 'nv-desktop-services.apporto.com'
port = 32474
database = 'AAC'
collection = 'animals'

db = MongoCrud(username, password, host, port, database, collection)

df = pd.DataFrame.from_records(db.read({}))  # JSON input & returned list object (empty object returns all documents)

# returns a new dataframe that does not contain the dropped column(s) to avoid invalid _id (ObjectID) type error
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)

#########################
# View
#########################

app = JupyterDash(__name__)

# Company logo
image_filename = 'aac_logo.png'
try:
    with open(image_filename, 'rb') as file:  # with statement to ensure file closes properly
        decoded_image = base64.b64encode(file.read()).decode()
except Exception as e:
    decoded_image = None

# Layout
app.layout = html.Div([
    #html.Div(id='hidden-div', style={'display':'none'}),

    html.A(
        href='https://www.snhu.edu',  # image-click URL
        children=[
            html.Img(
                src='data:image/png;base64,{}'.format(decoded_image),
                style={'width': '20%', 'max-width': '150px', 'min-width': '50px', 'height': 'auto'}  # logo
            )
        ],
        target="_blank"  # opens link in new tab
    ),

    html.Center(html.B(html.H1('Austin Animal Center: Dashboard'))),
    html.Hr(),

    dcc.RadioItems(
        id='type-selector',
        options=[
            {'label': 'Water Rescues', 'value': 'water_dogs'},
            {'label': 'Mountain or Wilderness Rescues', 'value': 'wilderness_dogs'},
            {'label': 'Disaster Rescues or Individual Tracking', 'value': 'disaster_dogs'}
        ],
        value=None,  # no default selection
        labelStyle={'display': 'block'}  # display options in block style
    ),

    html.Button('Reset', id='reset-button'),
    html.Br(),  # line break    
    html.Hr(),  # horizontal line


    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable="single",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",  # enables built-in pagination for table UX
        page_current=0,  # current page number
        page_size=10,    # number of rows to display on a single page
    ), 

    # input box to limit rows
    dcc.Input(
        id='limit-input',
        type='number',
    ),

    html.Br(),  # line break
    html.Hr(),  # horizontal line

    # Sets up side-by-side widgets
    html.Div(
        className='row',
        style={'display' : 'flex'},
        children=[
            html.Div(
                id='graph-id',
                className='col s12 m6',
            ),
            dl.Map(  # changed from html.Div
                id='map-id',
                children=[
                    dl.TileLayer(),
                    dl.LayerGroup(id='marker-layer')  # Container to dynamically add markers
                ],
                className='col s12 m6',
            )
        ]
    ),
    # unique tag displayed after other layout elements
    html.H4("Matthew Pool: MongoDB-Dash-Pandas (MVC)", id="m-pool")
])

#############################################
# Controller
#############################################

@app.callback(
    [
        Output('datatable-id', 'data'),
        Output('datatable-id', 'filter_query'),
        Output('datatable-id', 'sort_mode'),
        Output('datatable-id', 'selected_rows'),
        Output('type-selector', 'value'),
        Output('limit-input', 'value'),
        Output('graph-id', 'children')
    ],
    [Input('type-selector', 'value'),
     Input('reset-button', 'n_clicks')
    ],
    prevent_initial_call=False
)
def update_dashboard(filter_type, n_clicks):  # listens for changes in type-selector options & reset button clicks

    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    query = {}  # inialize empty dict to retrieve all documents

    if trigger_id == 'reset-button':  # Reset button clicked
        filter_type = None

    if filter_type:  # Adjust query ony if filter is set
        rescue_dogs = {
            'water_dogs': {
                'breeds': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland'],
                'sex': 'Intact Female',
                'min_age': 26,
                'max_age': 156
            },
            'wilderness_dogs': {
                'breeds': ['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler'],
                'sex': 'Intact Male',
                'min_age': 26,
                'max_age': 156
            },
            'disaster_dogs': {
                'breeds': ['Doberman Pinscher', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler'],
                'sex': 'Intact Male',
                'min_age': 20,
                'max_age': 300
            }
        }

        dog_info = rescue_dogs.get(filter_type, {})  # access the rescue_breeds dict
        breeds = dog_info.get('breeds', [])            # access the breeds list in the rescue_breeds dict
        sex = dog_info.get('sex', None)
        min_age = dog_info.get('min_age', 0)
        max_age = dog_info.get('max_age', 1000)

        query = {
            'breed': {'$in': breeds},
            'sex_upon_outcome': sex,
            'age_upon_outcome_in_weeks': {'$gte': min_age, '$lte': max_age}
        }

    try:
        df = pd.DataFrame.from_records(db.read(query))
        if df.empty:
            return [{}], "No data to load.", "multi", [], filter_type, "", no_update
    except Exception as e:
        return [{}], "Error loading data.", "multi", [], filter_type, "", no_update

    df.drop(columns=['_id'], inplace=True)

    # Calculate breed counts and sort
    breed_counts = df['breed'].value_counts().reset_index()
    breed_counts.columns = ['breed', 'count']

    # Select top 9 breeds and all other breeds as "Other Breeds"
    top_breeds = breed_counts.head(9)
    final_breeds = top_breeds

    if not filter_type and len(breed_counts) > 9:  # Add "Other Breeds" only if no filter set and more than 9 breeds
        other_breeds_sum = breed_counts.iloc[9:].sum()['count']

        if other_breeds_sum > 0:  # Add "Other Breeds" only if there are any
            other_breeds_row = pd.DataFrame([['Other Breeds', other_breeds_sum]], columns=['breed', 'count'])
            final_breeds = pd.concat([top_breeds, other_breeds_row])  # Combine top 9 breeds and "Other Breeds"

    # Populate pie chart with Dog breeds data
    pie_chart = dcc.Graph(
            figure=px.pie(
                data_frame=final_breeds,
                names='breed',
                color_discrete_sequence=px.colors.sequential.RdBu,
                values='count',
                title='AAC Dog Breeds'
            )
    )

    # datatable data, filter_query, sort_mode, selected_rows, type-selector: value, limit-input: value, graph-id: children
    return df.to_dict('records'), "", "multi", [], filter_type, "", pie_chart


# Callback to update geo-location chart for the selected data entry
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),  # derived_virtual_data is the dict of data available from the datatable
     Input('datatable-id', "derived_virtual_selected_rows")])  # derived_virtual_selected_rows is the list of selected row(s) in the table
def update_map(viewData, index):
    if not viewData or index is None:
        return []  # don't update markers if no data or rows are selected

    # Geolocation chart  
    dff = pd.DataFrame.from_dict(viewData)

    # Prevents IndexError if row_index is out of range of ViewData
    if not index or index[0] >= len(dff):  # no valid selection
        return[]


    # List can be converted to a row index here since using single-row selection 
    row = index[0]  # Austin TX is at [30.75,-97.48]

    return [
        dl.Map(style={'width': '1000px', 'height': '500px'},
               center=[30.75,-97.48],
               zoom=9,
               children=[
                   dl.TileLayer(id="base-layer-id"),
                   # Marker with tool tip and popup
                   # location_lat=col14, location_long=col15, breed=col5, name=col10
                   dl.Marker(position=[dff.iloc[row, 13],dff.iloc[row,14]],
                             children=[
                                 dl.Tooltip(dff.iloc[row,4]),
                                 dl.Popup([
                                     html.H3("Animal Name"),
                                     html.P(dff.iloc[row,9])
                                 ])
                             ]
                            )
               ]
              )
    ]


@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_rows')]
)
def update_styles(selected_rows):
    if not selected_rows:
        return []

    return [{
        'if': { 'row_index': i },
        'background_color': '#D2F3FF'
    } for i in selected_rows]


# Updates datatable to only display a user-defined number of documents
@app.callback(
    Output('datatable-id', 'page_size'),
    [Input('limit-input', 'value')],
    [State('datatable-id', 'page_size')]
)
def update_page_size(input_value, current_page_size):
    if input_value is not None and input_value != '' and int(input_value) > 0:  # Check for valid input before returning value
        return int(input_value)
    else:
        return current_page_size  # if invalid input value



# Dash app running on http://127.0.0.1:15185/
app.run_server(debug=True)


# In[ ]:




