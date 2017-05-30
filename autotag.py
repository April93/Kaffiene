import time
import os
import re
from selenium import webdriver

import urllib, json
from bs4 import BeautifulSoup


tags = set()

filename = 'data.txt'
textfile = open(filename, 'r')
data = textfile.read().split('\n')
textfile.close()
for line in data:
	lsplit = line.split(":")
	tsplit = lsplit[0].split("[")
	if len(tsplit) == 2:
		tags |= set(tsplit[1].split(", "))
print tags


filename = 'newsitesa.txt'
textfile = open(filename, 'r')
data = textfile.read().split('\n')
textfile.close()
sites = []
titles = []
for line in data:
	title = line.split("[")[0]
	lsplit = line.split(":")
	tsplit = lsplit[1].split(" ")
	# if len(tsplit) == 2:
		# tags |= set(tsplit[1].split(", "))
	titles.append(title)
	sites.append(tsplit[0])

listofsites = zip(titles, sites)
#Point to your phantomjs installation
PHANTOMJS_PATH = "phantomjs"


# response = urllib.urlopen(url)
# data = json.loads(response.read())

browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_log_path=os.path.devnull)
browser.set_window_size(1400, 1000)

#siteaddr = "1B1qzx67wJ2gxVTvurvzHwYAi988g7b3VN"

f = open("newsites2.txt","a")
f.write("---\n")

for siteaddr in listofsites:
	print siteaddr[1]
	url = "https://www.0proxy.ml/"+siteaddr[1]
	browser.get(url+"/content.json")
	#time.sleep(10)
	text = browser.page_source
	print text
	if "Not Found" in text or "504 Gateway Time-out" in text:
		print "Bad"
		wr = siteaddr[0]+"["+":"+siteaddr[1]+" -"+"\n"
		print wr
		f.write(wr)
	else:
		soup = BeautifulSoup(text, "lxml")
		data = json.loads(soup.find("body").text)
		domain = data.get('domain')
		orig = data.get('cloned_from')
		description = data.get('description')
		merged_type = data.get('merged_type')
		title = data.get('title')
		peer = '-'
		print domain, orig, description, title, merged_type

		browser.get(url)
		browser.switch_to.frame(browser.find_element_by_id("inner-iframe"))
		time.sleep(5)
		text = browser.page_source
		soup = BeautifulSoup(text, 'html.parser')

		result = set(soup.get_text().split()) & tags#set(keywords)
		wr = title+"["+', '.join(list(result))+":"+siteaddr[1]+" "+peer+"\n"
		print wr
		f.write(wr.encode('utf-8'))

f.close()
browser.quit()

#url = "https://proxy1.zn.kindlyfire.me/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
#url = "https://bit.no.com:43110/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
#url = "http://proxy.zeroexpose.com/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
#url = "http://zeronet.crypt.cat:8080/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D/"
#url = "https://zeroproxy.atomike.ninja/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D/"



#Grab.py stuff to fetch from znet pages
# browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_log_path=os.path.devnull)
# browser.set_window_size(1400, 1000)

# browser.get(url)
# browser.switch_to.frame(browser.find_element_by_id("inner-iframe"))
# raw_input("Done?")
# text = browser.page_source

# peerlist = re.findall('(?<=<span class="value">)[0-9]+(?=</span>)', text)
# titlelist = re.findall('(?<=<span class="title">).+?(?=</span>)', text)
# addrlist = re.findall('(?<=data-key=")[13][a-km-zA-HJ-NP-Z0-9]{26,33}', text)

# print len(addrlist), len(peerlist), len(titlelist)

# sitelist = zip(addrlist, peerlist, titlelist)

# f = open("peerlist.txt","w")
# for site in sitelist:
# 	f.write(site[0].encode('utf-8').strip()+" "+site[1].encode('utf-8').strip()+" "+site[2].encode('utf-8').strip()+"\n")
# f.close()
#browser.quit()