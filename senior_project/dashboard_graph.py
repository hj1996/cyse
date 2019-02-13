import os
import glob
import re
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

def file_opener():
	df = pd.read_csv("internettrafficreport-namerica--.csv")
	return df
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
df=file_opener()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H4(children='internet traffic report'),
    generate_table(df)
])

app.layout =html.Div(["hello"]), 
	html.Div([
		html.Div([
			dcc.Graph(
				id='ping-vs-packet_loss',
				figure={
					'data': [
						go.Scatter(
							x=df[df['Router'] == i]['Response Time (ms)'],
							y=df[df['Router'] == i]['Packet Loss (%)'],
							text=df[df['Router'] == i]['Router'],
							mode='markers',
							opacity=0.7,
							marker={
								'size': 15,
								'line': {'width': 0.5, 'color': 'white'}
							},
							name=i
						) for i in df.Router.unique()
					],
					'layout': go.Layout(
						xaxis={'type': 'log', 'title': 'Response Time (ms)'},
						yaxis={'title': 'Packet Loss (%)'},
						margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
						legend={'x': 0, 'y': 1},
						hovermode='closest'
					)
				}
			)], className = "six columns"),
			html.Div([
			dcc.Graph(
				id='ping-vs-packet',
				figure={
					'data': [
						go.Scatter(
							x=df[df['Router'] == i]['Response Time (ms)'],
							y=df[df['Router'] == i]['Packet Loss (%)'],
							text=df[df['Router'] == i]['Router'],
							mode='markers',
							opacity=0.7,
							marker={
								'size': 15,
								'line': {'width': 0.5, 'color': 'white'}
							},
							name=i
						) for i in df.Router.unique()
					],
					'layout': go.Layout(
						xaxis={'type': 'log', 'title': 'Response Time (ms)'},
						yaxis={'title': 'Packet Loss (%)'},
						margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
						legend={'x': 0, 'y': 1},
						hovermode='closest'
					)
				}
		)], className= "six columns")#must add up to 12
			
], className = "row")


if __name__ == '__main__':
    app.run_server(debug=True)