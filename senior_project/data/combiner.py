import time
import pandas as pd
import os
import glob
import re

def file_opener():
	master_index={}
	for filename in glob.glob('*.csv'):
		#print filename
		date=filename.split("_")
		date=date[1]
		date=date.split(".")
		date=float(date[0])
		source=filename.split("-")
		provider=source[1]
		provider=provider.replace("problems","")
		provider=provider.replace("reportus","")
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
			#print df
		elif "withhead" in filename:
			df = pd.read_csv(filename)
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
	
def combiner():
	master_index=file_opener()
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
			combine_notable.to_csv("combined_data/"+str(header)+"no_table"+".csv",index=False)
			combine_index.update({header+" no table":combine_notable})
			table_index=[]
			for items in header_table:
				location=table_headers.index(items)
				location=table_data[location]
				table_index.append(location)
			print table_index
			combine_table=pd.concat(table_index)
			combine_index.update({header+" table":combine_table})
			print header
			combine_table.to_csv("combined_data/"+str(header)+".csv",index=False)
		except  ValueError:
			pass
	
	return combine_index

combiner()