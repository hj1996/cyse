import time
import pandas as pd
import os
import glob
import re

def file_opener():
	master_index={}
	for filename in glob.glob('*.csv'):
		print filename
		df = pd.read_csv(filename)
		master_index[filename]=df
	return master_index
		
def combiner():
	master_index=file_opener()
	table_headers=master_index.keys()
	unique_header=[]
	for header in table_headers:
		header=header.split("-")
		header=header[0]
		unique_header.append(header)
	unique_header=list(set(unique_header))
	header_dic={}
	for header in unique_header:
		r = re.compile(header+".+")
		header_match=list(filter(r.match, table_headers))
		header_dic[header]=header_match
	data_frame_dic={}
	for header in header_dic:
		data_frame_list=[]
		for file in header_dic[header]:
			data_frame_list.append(master_index[file])
		data_frame_dic[header]=data_frame_list
	for header in data_frame_dic:
		combine_frame=pd.concat(data_frame_dic[header])
		print combine_frame
		#combine_frame= combine_frame.fillna(0)
		combine_frame.to_csv("combined_data/"+str(header)+".csv",index=False)
combiner()