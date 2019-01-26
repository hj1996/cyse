import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
website_file=open("website.txt","r")
website=website_file.readlines()
data_output=open("data.csv","w")
print website
for data in website:
	print data
	try:
		tables = pd.read_html(data[:-1])
		print(tables)
		try:
			tables[3].to_csv("data.csv",index=False)
		except:
			pass
	except ValueError or urllib2.HTTPError:
		pass 
	