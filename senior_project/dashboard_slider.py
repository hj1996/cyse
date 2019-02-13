import os
import glob
import re
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import dash_table

app = dash.Dash(__name__)

def file_opener():
	df = pd.read_csv("internettrafficreport-namerica--.csv")
	return df
	

	

PAGE_SIZE = 5
df=file_opener()
app.layout = html.Div([
	dash_table.DataTable(
		id='table-sorting-filtering',
		columns=[
			{'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
		],
		pagination_settings={
			'current_page': 0,
			'page_size': PAGE_SIZE
		},
		pagination_mode='be',

		filtering='be',
		filtering_settings='',

		sorting='be',
		sorting_type='multi',
		sorting_settings=[]),
	dcc.Slider(
        id='my-slider',
        min=0,
        max=20,
        step=1,
        value=10,		
    ),
	 html.Div(id='slider-output-container')
])

@app.callback(
	Output('table-sorting-filtering', 'data'),
	[Input('table-sorting-filtering', 'pagination_settings'),
	Input('table-sorting-filtering', 'sorting_settings'),
	Input('table-sorting-filtering', 'filtering_settings')])

	 
def update_graph(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = df
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0]
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0]
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    if len(sorting_settings):
        dff = dff.sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')
	
@app.callback(
	dash.dependencies.Output('my-slider', 'value'),
	[dash.dependencies.Input('my-slider', 'value')])

def update_graph_value(value):
	PAGE_SIZE = value
	
	
if __name__ == '__main__':
    app.run_server(debug=True)
