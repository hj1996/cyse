import re #import the module for regulor expression
import pandas as pd

def number_text(text,word_list):
	results_list=[]
	for words in word_list:
		words=words.replace("\n","")
		expres=r"[0-9 .]+"+words
		print expres
		results=re.search(expres,text,re.IGNORECASE)
		print results
		if results != None: #if the word is not found the re returns none 
			results=results.group()# .group() creates text version of the data 
			results_list.append(results) #add the data to the list
	return results_list

def text_word(text,word_list):
	results_list=[]
	for words in word_list:
		words=words.replace("\n","")
		expres= r"[A-z ]+."+words
		results=re.search(expres,text,re.IGNORECASE)
		if results != None: #if the word is not found the re returns none 
			results=results.group()# .group() creates text version of the data 
			results_list.append(results) #add the data to the list
	return results_list
	
def word_text(text,word_list):
	results_list=[]
	for words in word_list:
		words=words.replace("\n","")
		expres=words+r"[A-z ]+."
		results=re.search(expres,text,re.IGNORECASE)
		if results != None: #if the word is not found the re returns none 
			results=results.group()# .group() creates text version of the data 
			results_list.append(results) #add the data to the list
	return results_list