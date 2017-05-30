import time
import os
import re
from selenium import webdriver

#Uncomment the url for the site you wish to grab peer info from.
#You can run each one and merge the results using merge.py
#When 'Done?' appears, wait a few moments, and then hit 'enter'.
#A number higher than 0 should appear three times. If the numbers don't appear,
#or are different, a problem has occured!


#Point to your phantomjs installation
PHANTOMJS_PATH = "phantomjs"

#Select source
#url = "https://proxy1.zn.kindlyfire.me/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
url = "https://www.0proxy.ml/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
#url = "http://proxy.zeroexpose.com/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
#url = "http://zeronet.crypt.cat:8080/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D/"
#url = "https://zeroproxy.atomike.ninja/1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D/"

browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_log_path=os.path.devnull)
browser.set_window_size(1400, 1000)

browser.get(url)
browser.switch_to.frame(browser.find_element_by_id("inner-iframe"))
time.sleep(10)
text = browser.page_source

peerlist = re.findall('(?<=<span class="value">)[0-9]+(?=</span>)', text)
titlelist = re.findall('(?<=<span class="title">).+?(?=</span>)', text)
addrlist = re.findall('(?<=data-key=")[13][a-km-zA-HJ-NP-Z0-9]{26,33}', text)

print len(addrlist), len(peerlist), len(titlelist)

sitelist = zip(addrlist, peerlist, titlelist)

f = open("peerlist.txt","w")
for site in sitelist:
	f.write(site[0].encode('utf-8').strip()+" "+site[1].encode('utf-8').strip()+" "+site[2].encode('utf-8').strip()+"\n")
f.close()
browser.quit()