import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 
import string
import os.path

def downdetector(provider):
		try:
			provider=provider.replace("\n","")
			#print provider
			content = requests.get("https://downdetector.com/status/"+provider)
			content = content.text    #opens the website to grab that data in it
			soup = BeautifulSoup(content,"html5lib")
			list_data=[]
			status_data=soup.findAll("div",{"class":"alert"})
			#print status_data
			location_data=soup.findAll("h3",{"class":"cities"})
			##print location_data
			Reg_2=r'\/status\/[A-z -]+\/[A-z-]+'
			location_data=re.findall(Reg_2,str(location_data),re.IGNORECASE)
			location_list=[]
			if str(location_data) != "None":
				for location in location_data:
					location=location.split('/')
					location=location[3]
					if location !="map":
						location_list.append(location)
					##print location_list
			location_dic={"Location":location_list}
			Reg=r"[A-z]+ problems"
			results=re.search(Reg,str(status_data),re.IGNORECASE)
			if str(results) != "None":
				status_data=results.group()
			else:
					Reg=r"problems"
					results=re.search(Reg,str(status_data),re.IGNORECASE)
					if str(results) != "None":
						status_data=results.group()
			for li_tag in soup.find_all('li'):
				data=li_tag.text, li_tag.next_sibling
				data=" ".join(data)
				data=data.replace("\n","")
				data=data.replace("  ","")
				list_data.append(data)
			string_Data="---".join(list_data)
			reg_ex=r"---[A-z ]+ \([0-9]+%\)"
			results=re.findall(reg_ex,string_Data,re.IGNORECASE)
			percent_dic={}
			if str(results) != "None":
				for percent_data in results:
					#print percent_data
					percent_data=percent_data.split("(")
					percent_data[0]=percent_data[0].replace("---","")
					percent_data[1]=percent_data[1].replace(")","")
					percent_dic[percent_data[0].lower()]=percent_data[1]
			full_DataFrame=pd.DataFrame(data=location_dic)
			percent_header=["bad signal","internet","landline internet","limited channels","mobile internet","mobile phone","no network or reception","no signal","no tv","online viewing","phone","total blackout","tv"] 
			for header in percent_header:
				full_DataFrame[header]=""
			for x in percent_dic:
				full_DataFrame[x]=percent_dic[x]
			print status_data
			full_DataFrame["Status"]=status_data
			full_DataFrame["Provider"]=provider
			full_DataFrame["Source"]="Down detector"
			current_time=time.strftime("%H:%M:%S",time.localtime(date))
			current_date=time.strftime("%a %d %b %Y",time.localtime(date))
			full_DataFrame["Date collected"]=current_date
			full_DataFrame["Time collected"]=current_time
			if full_DataFrame.empty:
				pass
			else: 
				full_DataFrame.to_csv(os.path.expanduser("~/Documents/senior_project/data/"+"downdetector-"+provider+"_"+str(date)+".csv"),index=False)
				#print full_DataFrame
			return full_DataFrame
		except IndexError:
			##print provider
			pass
	
f=open(os.path.expanduser("~/Documents/senior_project/providers.txt"),"r")
data=f.readlines()
date=time.time()
table_list=[]
for provider in data:
	table_list.append(downdetector(provider))
downdetector_currentdata=pd.concat(table_list)