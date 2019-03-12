import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 

def istheservicedown():
	f=open("providers.txt","r")
	data=f.readlines()
	date=time.time()

	for provider in data:
		try:
			provider=provider.replace("\n","")
			print provider
			content = requests.get("https://istheservicedown.com/problems/"+provider)
			content = content.text    #opens the website to grab that data in it
			soup = BeautifulSoup(content,"html5lib")
			data=soup.findAll("ul", {"class": "inline-list-bullet"})
			data=str(data[0])
			data=data.replace(" <span>",";")
			data=data.replace("</span></li>\n","")
			data=data.replace("</ul>","")
			data=data.replace(")","")
			data=data.replace("(","")
			data=data.replace("\n","")
			data=data.split("<li>")
			data.pop(0)
			percent_data=data
			percent_dic={}
			for data in percent_data:
				print data
				data=data.split(";")
				data[1]=data[1].replace(" ","")
				percent_dic[data[0]]=data[1]
			print percent_dic
			status_data=soup.findAll("div", {"class": "service-status-alert"})
			status_data=str(status_data)
			status_data=status_data.split("</i>")
			status_data=status_data[1]
			status_data=status_data.split("at")
			status_data=status_data[0]
			status_data=status_data.replace(u'\\xa0', u'')
			print status_data
			percent_dic["Status"]=status_data
			percent_dic["Provider"]=provider
			percent_dic["Source"]="Is the service down"
			current_time=time.strftime("%H:%M:%S",time.localtime(date))
			current_date=time.strftime("%a %d %b %Y",time.localtime(date))
			percent_dic["Date collected"]=current_date
			percent_dic["Time collected"]=current_time
			content = requests.get("https://istheservicedown.com/problems/"+provider+"/map")
			tables = pd.read_html(content.text,header=0)
			tables=tables[0]
			for headers in percent_dic:
				tables[headers]=percent_dic[headers]
			tables.to_csv("data/"+"istheservicedown-"+provider+"_"+str(date)+".csv",index=False)
			print tables
		except IndexError:
			print provider
			pass