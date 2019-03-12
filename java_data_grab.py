from bs4 import BeautifulSoup
from selenium import webdriver
import searcher

key_words_file=open("key_words.txt","r") #file with all of the words to look for 
key_words=key_words_file.readlines()

url = "https://www.isitdownrightnow.com/simfileshare.net.html"
browser = webdriver.PhantomJS()
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
text_data=soup.get_text()
for tag in soup(text_data):
    for attribute in ["class", "id", "name", "style"]:
        del tag[attribute]
text_data=text_data.splitlines() #create a list with data split by new line
for lines in text_data: #removes extra spaces in the data
	lines_location=text_data.index(lines)
	lines=lines.replace(" ","")
	text_data[lines_location]=lines
text_data_string=" ".join(text_data)
print text_data_string.encode("utf-8")
result=searcher.number_text(text_data_string,key_words)
print result