from bs4 import BeautifulSoup
from selenium import webdriver
import project_request

key_words_file=open("key_words.txt","r") #file with all of the words to look for 
key_words=key_words_file.readlines()

url = "https://www.akamai.com/us/en/solutions/intelligent-platform/visualizing-akamai/real-time-web-monitor.jsp"
browser = webdriver.PhantomJS()
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
text_data=soup.get_text()
result=project_request.text_finder(text_data,key_words)
print result