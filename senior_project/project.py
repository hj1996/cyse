import pandas as pd
import ssl
from bs4 import BeautifulSoup
import urllib2



def spliter(target_item,text,remove_text,keep):
	filename=text.split(target_item)
	#print filename
	for element in filename:
		if keep == 0:
			if remove_text in element:
				filename.pop(filename.index(element))
		if keep == 1: 
			if remove_text not in element:
				filename.pop(filename.index(element))
	filename="-".join(filename)
	return filename

def providers_Adder(providers,url,found_provider):
	url_list=[]
	for provider in providers:
		found_provider=found_provider.replace("\n","")
		provider=provider.replace("\n","")
		url_new=url.replace(found_provider,provider)
		url_list.append(url_new)
	return url_list
		

ssl._create_default_https_context = ssl._create_unverified_context
website_file=open("website.txt","r")
providers_file=open("providers.txt","r")
providers=providers_file.readlines()
website=website_file.readlines()
data_output=open("data.csv","w")

for data in website:
	for provider in providers: 
		if provider[-1] in data:
			url_list=providers_Adder(providers,data,provider)
			website=website+url_list
			website=list(set(website))
			#break
		else:
			print "false"
	
for data in website:
	data=data.split(",")
	print data[0]
	url=data[0]
	if int(data[1])==0:
		relevent_Data=[]
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content,"lxml")
		text_data=soup.get_text()
		text_data=text_data.splitlines()
		ctr=0
		for lines in text_data:
			lines_location=text_data.index(lines)
			lines=lines.replace(" ","")
			text_data[lines_location]=lines
			if ":" in lines:
				relevent_Data.append(lines)		
		#print relevent_Data
	if int(data[1])==1:
		try:
			tables = pd.read_html(url)
			#print(tables)
			#try:
			filename=spliter("/",url,"com",1)
			filename=spliter(".",filename,"com",0)
			tables[int(data[2][:-1])].to_csv(filename+".csv",index=False)
		except ValueError or urllib2.HTTPError:
			pass 
		except:#add error handling for bad websites 
			pass