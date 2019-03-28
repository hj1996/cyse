import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 

def internettrafficreport():
	date=time.time()
	try:

		content = requests.get("http://internettrafficreport.com/namerica.htm")
		tables = pd.read_html(content.text,header=0)
		tables=tables[4]
		current_time=time.strftime("%H:%M:%S",time.localtime(date))
		current_date=time.strftime("%a %d %b %Y",time.localtime(date))
		tables["Time collected"]=current_time
		tables["date collected"]=current_date
		tables["Source"]="Internet traffic report"
		print tables
		tables.to_csv("data/"+"internettrafficreport-_"+str(date)+".csv",index=False)
	except ValueError:
		pass

		