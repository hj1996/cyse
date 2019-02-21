import pandas as pd #import the module that 
import ssl #import the module for SSl connections 
import re #import the module for regulor expression  
from bs4 import BeautifulSoup #import the module to parse html
import urllib2 #import the module to connect websites and get data 
import time #import the module for time base fuction 
import requests 

def twitter_remover(data):#removes comments and twitter text from data
	data_cleaned=re.sub(r"comments.+",'-',data)
	print data_cleaned.encode("utf-8")
	return data_cleaned
	

def spliter(text):#clean name to write file 
	#regulor expression +mean one or more of the item before and . mean any character 
	#/plan text version so it is looking for any character follow by a / and replaces it with nonething  
	filename=re.sub(r".+\//",'',text) 
	filename=re.sub(r"www\.",'',filename) #looks for www.
	filename=re.sub(r"\.[com]*[^A-z]*|html*",'-',filename) #remove text that follows .com
	filename=re.sub(r"-+",'-',filename)
	filename=filename.replace("/","") #removes any remainning / since they cannot be in a filename
	return filename

def providers_Adder(providers,url,found_provider): #adds more url with providers from provider file
	url_list=[] #empty list to store the all of the created url
	for provider in providers: #for loop for all of the providers in the providers file
		found_provider=found_provider.replace("\n","") #removes the newline at the end of some providers
		provider=provider.replace("\n","") #removes the newline
		url_new=url.replace(found_provider,provider) #replaces the old provder with the new one
		url_list.append(url_new) #adds the new url to the list 
	return url_list
def text_finder(text,words_list): #looks for text that are in the word list file
	#print text.encode("utf-8") ##prints out the text using teh utf-8 format
	results_list=[] #empty list to store all of the text found 
	for words in words_list: #goes throught the word in the key word file
		words=words.replace("\n","") #removes the newline
		#creates a regulor expression to look for the word follow by and char not A-z with is then follow by any number of numbers 
		reg_ex=r""+words+" \ "
		reg_ex=reg_ex.replace(" ","")
		reg_ex=reg_ex+"b[^A-Z]+[0-9]+" 
		results=re.search(reg_ex,text,re.IGNORECASE)
		if results != None: #if the word is not found the re returns none 
			results=results.group()# .group() creates text version of the data 
			results_list.append(results) #add the data to the list
	return results_list
def csv_writer(data,website): #save the data as a csv file 
	clean_Web=spliter(website) #runs the spliter fuction
	#print clean_Web
	output_csv=open(clean_Web+"-notable_"+str(time.time())+".csv","w") #adds no table to state that the data was not made with pandas
	for infor in data:
		infor=str(infor)
		infor=re.sub(r"[^A-z 1-9.]+|[ ]",",",infor) #splits a text follow by number with a newline 
		output_csv.write(infor+"\n") #writes the data and adds a new line
	
ssl._create_default_https_context = ssl._create_unverified_context #stop ssl errors 
website_file=open("website.txt","r") #file with all of the website
providers_file=open("providers.txt","r") #file with all of the provider ex att and comcast 
#opens and reads needed files
providers=providers_file.readlines()
website=website_file.readlines()
data_output=open("data.csv","w")
key_words_file=open("key_words.txt","r") #file with all of the words to look for 
key_words=key_words_file.readlines()

for data in website:
#looks for website with a provider in the url to create additional url for other providers 
	for provider in providers: 
		if provider[-1] in data:
			url_list=providers_Adder(providers,data,provider)
			website=website+url_list
			website=list(set(website))
			#break
		else:
			pass
	
for data in website:
	data=data.split(",") #splits the websites by , to create a list 
	#print data
	url=data[0]
	if "0" in data[1]: #0 in the season entry mean that the website has data that is not in a table  
		relevent_Data=[] #empty list for useful data 
		content = requests.get(url)
		content = content.text    #opens the website to grab that data in it
		soup = BeautifulSoup(content,"html5lib")
		#print len(data)
		text_data=soup.get_text() #get all of the text data
		text_data=text_data.splitlines() #create a list with data split by new line
		ctr=0
		for lines in text_data: #removes extra spaces in the data
			lines_location=text_data.index(lines)
			lines=lines.replace(" ","")
			text_data[lines_location]=lines
		text_data_string=" ".join(text_data) #join the data with a space inbetween the text
		if "1" in data[3]:	
			text_data_string=twitter_remover(text_data_string)
		found_text=text_finder(text_data_string,key_words) #runs the fext_finder fuction 
		csv_writer(found_text,url) #writes the data into a file
		#except urllib2.HTTPError, e:
		#	#print "error connecting to "+url
		#	pass
		#except:#better error handling
		#	#print data[0]
	if "1" in data[1]: #1 means that there is data that is in a table so pandas can grab it 
		try:
			content=requests.get(url)
			tables = pd.read_html(content.text) #get the data using pandas
			#tables = pd.fillna(0)
			#print tables
			filename=spliter(url) #runs that function to clean up the url 
			tables[int(data[2].replace("\n",""))].to_csv(filename+"_"+str(time.time())+".csv",index=False) #save the data as a csv file

		except ValueError:#add error handling for bad websites 
		#	#print "error connecting to"+url
			pass
		#except:
		#	#print "error connecting to "+url
		#	pass