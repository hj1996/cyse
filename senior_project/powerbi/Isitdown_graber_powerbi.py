import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 
import os.path


def isitdown(provider):
	try:
		provider=provider.replace("\n","")
		#print provider
		content = requests.get("https://www.isitdownrightnow.com/"+provider+".com.html")
		#content=requests.get("https://www.isitdownrightnow.com/comcast.com.html")
		#content = content.text    #opens the website to grab that data in it
		tables = pd.read_html(content.text,header=0)
		df1 = tables[0].iloc[:, :3]
		df2 = tables[0].iloc[:, 4:7]
		df2.columns = ["Date","Time reported(PT)","Ping Time(ms.)"]
		df1.columns = ["Date","Time reported(PT)","Ping Time(ms.)"]
		combine_tables=pd.concat([df1,df2],ignore_index=True)
		current_timedate=time.strftime("%a %d %b %Y %H:%M:%S",time.localtime(date))
		#current_date=time.strftime("%a %d %b %Y",time.localtime(date))
		combine_tables["Time collected"]=current_timedate
		#combine_tables["date collected"]=current_date
		combine_tables["Source"]="Is it down right now?"
		combine_tables["Provider"]=provider
		combine_tables['Ping Time(ms.)'] = combine_tables['Ping Time(ms.)'].str.extract('(\d*\.?\d*)', expand=False).astype(float)
		print combine_tables
		combine_tables.to_csv(os.path.expanduser("~/Documents/senior_project/data/"+"isitdownrightnow-"+provider+"_"+str(date)+".csv"),index=False)
		data=combine_tables
		return combine_tables
	except ValueError:
		#print provider
		pass
			
f=open(os.path.expanduser("~/Documents/senior_project/providers.txt"),"r")
data=f.readlines()
date=time.time()
table_list=[]
for provider in data:
	table_list.append(isitdown(provider))
final_table=pd.concat(table_list)