import pandas as pd
import ssl
import re 
from bs4 import BeautifulSoup
import urllib2



def spliter(text):#clean name to write file 
	filename=re.sub(r".+\//",'',text)
	filename=re.sub(r"www\.",'',filename)
	filename=re.sub(r"\.[com]*[^A-z]*|html*",'-',filename)
	filename=filename.replace("/","")
	return filename

def providers_Adder(providers,url,found_provider): #adds more url with providers from provider file
	url_list=[]
	for provider in providers:
		found_provider=found_provider.replace("\n","")
		provider=provider.replace("\n","")
		url_new=url.replace(found_provider,provider)
		url_list.append(url_new)
	return url_list
def text_finder(text,words_list):
	print text.encode("utf-8")
	results_list=[]
	for words in words_list:
		words=words.replace("\n","")
		reg_ex=r""+words+" \ "
		reg_ex=reg_ex.replace(" ","")
		reg_ex=reg_ex+"b[^A-Z]+[0-9]+"
		results=re.search(reg_ex,text,re.IGNORECASE)
		if results != None: 
			results=results.group()
			results_list.append(results)
	return results_list
def csv_writer(data,website):
	clean_Web=spliter(website)
	print clean_Web
	output_csv=open(clean_Web+"-notable.csv","w")
	for infor in data:
		infor=str(infor)
		infor=re.sub(r"[^A-z 1-9.-]+|[ ]",",",infor)
		output_csv.write(infor+"\n")
	
ssl._create_default_https_context = ssl._create_unverified_context #
website_file=open("website.txt","r")
providers_file=open("providers.txt","r")
providers=providers_file.readlines()
website=website_file.readlines()
data_output=open("data.csv","w")
key_words_file=open("key_words.txt","r")
key_words=key_words_file.readlines()

for data in website:
	for provider in providers: 
		if provider[-1] in data:
			url_list=providers_Adder(providers,data,provider)
			website=website+url_list
			website=list(set(website))
			#break
		else:
			pass
	
for data in website:
	data=data.split(",")
	print data
	url=data[0]
	if "0" in data[1]:
		relevent_Data=[]
		#try:
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content,"html5lib")
		print len(data)
		text_data=soup.get_text()			
		text_data=text_data.splitlines()
		ctr=0
		for lines in text_data:
			lines_location=text_data.index(lines)
			lines=lines.replace(" ","")
			text_data[lines_location]=lines
		text_data_string=" ".join(text_data)
		found_text=text_finder(text_data_string,key_words)
		csv_writer(found_text,url)
		#except urllib2.HTTPError, e:
		#	print "error connecting to "+url
		#	pass
		#except:#better error handling
		#	print data[0]
	if "1" in data[1]:
		try:
			tables = pd.read_html(url)
			filename=spliter(url)
			print tables[4]
			tables[int(data[2].replace("\n",""))].to_csv(filename+".csv",index=False)
		except urllib2.HTTPError, e:
			print "error connecting to "+url
			pass
		except:#add error handling for bad websites 
			print "error connecting to"+url