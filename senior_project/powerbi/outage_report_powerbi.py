import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 

def outage():
	f=open("providers.txt","r")
	data=f.readlines()
	for provider in data:
		try:
			provider=provider.replace("\n","")
			content = requests.get("https://outage.report/us/"+provider)
			content = content.text    #opens the website to grab that data in it
			soup = BeautifulSoup(content,"html5lib")
			data=soup.findAll("text", {"class": "Gauge__Count-s1qahqgd-5 kqYYAx"}) #gets the websie section for the number of report
			data=str(data)
			data=data.split(">")#cleans up the data
			data=data[1]
			data=data.split("<")
			report_time=data[0]
			date=time.time()
			current_time=time.strftime("%H:%M:%S",time.gmtime(date)) #creates the filed for time and date
			date=time.strftime("%a %d %b %Y %H:%M:%S",time.gmtime(date))
			current_time=time.strftime("%H:%M:%S")
			d = {'Reports in last 20 minutes':[report_time],'Time/date':[date]}
			df=pd.DataFrame(data=d)
			percent_data=soup.findAll("ul",{"class":"OutageSubjectsBox__Ul-cl1exo-0 gknwmv"}) #gets issues list
			percent_data=str(percent_data)
			percent_data=percent_data.replace("</li>","")
			percent_data=percent_data.replace("</ul>","")#more cleaning
			percent_data=percent_data.replace("[","")
			percent_data=percent_data.replace("]","")
			percent_data=percent_data.split("<li>")
			percent_data.pop(0)
			percent_dic={}
			for data in percent_data:#splits the issue type from the percents
				print data
				data=data.split("-")
				data[1]=data[1].replace(" ","")
				percent_dic[data[0]]=data[1]
			print percent_dic
			map_data=soup.findAll("ul",{"class":"RecentReports__Row-q9gvkj-3 dBUIMR"})#gets the location data from the site
			list_data=[]
			for string in soup.stripped_strings:
				list_data.append(repr(string))
			string_data='---'.join(list_data)
			reg_ex=r"'United States'.+u'Outage Map'" #reg expression to find the location data 
			results=re.search(reg_ex,string_data,re.IGNORECASE)
			provider=results.group()
			provider=provider.split("'---u'")
			provider=provider[1]
			print results
			string_no_comm=re.sub(r"Discussion.+",'',string_data) #removes the comment section 
			string_no_comm=re.sub(r".+Live'---u",'',string_no_comm)
			string_no_comm=string_no_comm.replace("'","")
			parsed_data=string_no_comm.split("---u")
			parsed_data = list(filter(None, parsed_data)) #remove empty items
			d={"Location":[parsed_data[0]],"Issue":[parsed_data[1]],"How long ago":[parsed_data[2]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Date/Time":[date],'Source':"Outage Report"}
			location_DataFrame=pd.DataFrame(data=d) #creates a data frame using panda
			parsed_data.pop(0)
			parsed_data.pop(0) #removes usesless data 
			parsed_data.pop(0)
			while len(parsed_data)>0:
				d={"Location":[parsed_data[0]],"Issue":[parsed_data[1]],"How long ago":[parsed_data[2]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Date/Time":[date],'Source':"Outage Report"}
				temp_DataFrame=pd.DataFrame(data=d) #creates a second data frame 
				location_DataFrame=pd.concat([temp_DataFrame,location_DataFrame])#combines the two data frame
				parsed_data.pop(0)
				parsed_data.pop(0)
				parsed_data.pop(0)
			for headers in percent_dic:
				location_DataFrame[headers]=percent_dic[headers]
			print location_DataFrame
			location_DataFrame.to_csv("data/"+"outage-report-"+provider+"_"+str(time.time())+".csv",index=False) #save the data to a csv
		except IndexError: #error handling
			print provider