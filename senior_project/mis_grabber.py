import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 

content = requests.get("https://outage.report/us/xfinity")
content = content.text    #opens the website to grab that data in it
soup = BeautifulSoup(content,"html5lib")
data=soup.findAll("text", {"class": "Gauge__Count-s1qahqgd-5 kqYYAx"})
data=str(data)
data=data.split(">")
data=data[1]
data=data.split("<")
report_time=data[0]
date=time.time()
date=time.strftime("%a %d %b %Y %H:%M:%S",time.gmtime(date))
d = {'Reports in last 20 minutes':[report_time],'Time/date':[date]}
df=pd.DataFrame(data=d)
map_data=soup.findAll("ul",{"class":"RecentReports__Row-q9gvkj-3 dBUIMR"})
list_data=[]
for string in soup.stripped_strings:
    list_data.append(repr(string))
string_data='---'.join(list_data)
reg_ex=r"'United States'.+u'Outage Map'"
results=re.search(reg_ex,string_data,re.IGNORECASE)
provider=results.group()
provider=provider.split("'---u'")
provider=provider[1]
print results
string_no_comm=re.sub(r"Discussion.+",'',string_data)
string_no_comm=re.sub(r".+Live'---u",'',string_no_comm)
string_no_comm=string_no_comm.replace("'","")
parsed_data=string_no_comm.split("---u")
parsed_data = list(filter(None, parsed_data)) #remove empty items
d={"Location":[parsed_data[0]],"Issue":[parsed_data[1]],"How long ago":[parsed_data[2]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Current time/data":[date],'Source':"outage"}
location_DataFrame=pd.DataFrame(data=d)
parsed_data.pop(0)
parsed_data.pop(0)
parsed_data.pop(0)
while len(parsed_data)>0:
	d={"Location":[parsed_data[0]],"Issue":[parsed_data[1]],"How long ago":[parsed_data[2]],'Reports in last 20 minutes':[report_time],'Provider':provider,"Current time/data":[date],'Source':"outage"}
	temp_DataFrame=pd.DataFrame(data=d)
	location_DataFrame=pd.concat([temp_DataFrame,location_DataFrame])
	parsed_data.pop(0)
	parsed_data.pop(0)
	parsed_data.pop(0)
print location_DataFrame
location_DataFrame.to_csv("data/"+"outage-withheadwithhead"+provider+"_"+str(time.time())+".csv",index=False)