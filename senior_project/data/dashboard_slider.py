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
import time



def file_opener():
	master_index={}
	for filename in glob.glob('*.csv'):
		print filename
		date=filename.split("_")
		date=date[1]
		date=date.split(".")
		date=float(date[0])
		source=filename.split("-")
		provider=source[1]
		provider=provider.replace("problems","")
		source=source[0]
		if "notable" in filename:
			df = pd.read_csv(filename,header=None)
			df = df.fillna(0)
			df= df.T
			new_header=df.iloc[0]
			df=df[1:]
			df.columns=new_header
			df["Time/date"]=time.strftime("%a %d %b %Y %H:%M:%S",time.gmtime(date))
			df["Source"]=source
			df["Provider"]=provider
			print df
		else:
			df = pd.read_csv(filename)
			new_header=df.iloc[0]
			df=df[1:]
			df.columns=new_header
			df["Time"]=time.strftime("%a %d %b %Y %H:%M:%S",time.gmtime(date))
			df["Source"]=source
			df["Provider"]=provider
		master_index.update({filename:df})
	return master_index
	
def combiner(master_index):
	table_data=master_index.values()
	unque_header_list=[]
	combine_index={}
	table_headers=master_index.keys()
	for headers in table_headers:
		unque_header=headers.split("-")
		unque_header=unque_header[0]
		unque_header_list.append(unque_header)
	unque_header_list=list(set(unque_header_list))
	for header in unque_header_list:
		r = re.compile(header+".+notable")
		r2= re.compile(header+".+")
		header_notable=list(filter(r.match, table_headers))
		header_table=list(filter(r2.match, table_headers))
		header_table=list(set(header_table)-set(header_notable))
		notable_index=[]
		for items in header_notable:
			location=table_headers.index(items)
			location=table_data[location]
			notable_index.append(location)
		try:
			combine_notable=pd.concat(notable_index)
			combine_index.update({header+" no table":combine_notable})
			table_index=[]
			for items in header_table:
				location=table_headers.index(items)
				location=table_data[location]
				table_index.append(location)
			print table_index
			combine_table=pd.concat(table_index)
			combine_index.update({header+" table":combine_table})
		except:
			pass
	return combine_index

app = dash.Dash(__name__)

	

	

PAGE_SIZE = 5
master_index=file_opener()
combine_index=combiner(master_index)
table_data=combine_index.values()
table_headers=combine_index.keys()
df=table_data[2]
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
	

	
	
if __name__ == '__main__':
    app.run_server(debug=True)
