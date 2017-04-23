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
#print tags


filename = 'newsitesa.txt'
textfile = open(filename, 'r')
data = textfile.read().split('\n')
textfile.close()
sites = []
for line in data:
	lsplit = line.split(":")
	tsplit = lsplit[1].split(" ")
	# if len(tsplit) == 2:
		# tags |= set(tsplit[1].split(", "))

	sites.append(tsplit[0])

#Point to your phantomjs installation
PHANTOMJS_PATH = "phantomjs"


# response = urllib.urlopen(url)
# data = json.loads(response.read())

browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_log_path=os.path.devnull)
browser.set_window_size(1400, 1000)

#siteaddr = "1B1qzx67wJ2gxVTvurvzHwYAi988g7b3VN"

f = open("newsites2.txt","a")
f.write("---\n")

for siteaddr in sites:
	print siteaddr
	url = "https://proxy1.zn.kindlyfire.me/"+siteaddr
	browser.get(url+"/content.json")
	text = browser.page_source
	print text
	if "Not Found" in text or "504 Gateway Time-out" in text:
		print "Bad"
	else:
		soup = BeautifulSoup(text, "lxml")
		data = json.loads(soup.find("body").text)
		domain = data.get('domain')
		orig = data['cloned_from']
		description = data['description']
		title = data['title']
		peer = '-'

		browser.get(url)
		browser.switch_to.frame(browser.find_element_by_id("inner-iframe"))
		time.sleep(5)
		text = browser.page_source
		soup = BeautifulSoup(text, 'html.parser')

		# keywords = ["blog","zero","news","ebooks","games","zerohello", "zeroboard", "zerosearch", "zeroblog", "dydx", "zeronet", "site", "pitcairn", "island", "trip", "2012", "bluish", "coder", "old", "blog", "bluish", "coder", "blog", "zerobay", "river", "of", "news", "bootstrap", "jquery", "site", "things", "to", "see!", "zeronet", "index", "smokingcode", "blog", "acerplatanoide", "zeroblog", "javascript", "emulator", "games", "tv", "episodes", "before", "the", "law", "zeronet", "proxy", "decentral", "blog", "elmit", "blog", "zeronet", "rocks", "underd0g", "zeronet", "site", "zero", "network", "homepage", "rush", "wallet", "online", "bitcoins", "old", "zerotalk", "cute", "cutting", "zeronet", "requirements", "transmission", "blog", "adultlit", "public", "share", "zero", "habr", "high", "maintenance", "s04e01", "qasim", "zeroname", "winterblufox", "old", "blog", "winterblufox", "blog", "karsten", "site", "michael", "zigler", "site", "ojrask", "site", "coinbin", "zero", "address", "brain", "wallet", "generator", "salvotnt", "anime", "blog", "tor", "test", "smoking", "code", "labrat.mobi", "studio", "mobile", "web", "games", "the", "corsair", "ebooks", "zeroid", "split", "secret", "censored", "websites", "j", "zeronet", "site", "zero", "cinema", "blog", "videos", "movies", "films", "entertainment", "idealcoder", "blog", "emoji", "day", "xgame", "test", "blog", "zeromart", "retroshare", "rus", "zerotalk", "myzeroblog", "retroshare", "eng", "the", "coding", "love", "blog", "anarchist", "buddhism", "lostfile", "blog", "lyc", "jsnes", "emulator", "game", "of", "life", "porn2peer", "nsfw", "porn", "lostfile", "index", "zerocinema", "blog", "zerotube", "0.1", "ZOMG", "Teh", "Blog!", "blog", "russian", "it", "crypto", "zerobunker", "site", "zerovid", "vulonkaaz", "site", "vulonkaaz", "blog", "anonymouscoward", "site", "anonymouscoward", "pgp", "key", "beatface", "cryptonewsday", "js2coffee", "javascript", "coffeescript", "converter", "kickassfeeds", "books", "kickassfeeds", "movies", "kickassfeeds", "anime", "lyc", "language", "misesinstitutet", "tactiic", "torlock", "tunecedemalis", "javascript", "beautifier", "yamamushi", "site", "wimp", "curlybear", "blog", "curlybear", "zerotalk", "zerochat", "tutorial", "sample", "zeroit", "zeronet", "blog", "legionof7", "site", "chocodum", "page", "zerobunker", "blog", "drwasho", "blog", "next", "blog", "everything", "talk", "Chinese", "Forum", "zerotalk", "with", "images", "it", "begins", "m1nistry", "site", "slothkrew", "zeronet", "slothkrew", "sloth", "hacking", "ctf", "opsec", "netsec", "irc", "community", "bazaarbay", "uwidth", "web", "zero", "zeronet", "css", "html", "template", "example", "mobile", "width", "dark", "simple", "minimal", "0chan", "imageboards", "0chan", "imageboard", "4chan", "images", "social", "anonymous", "class", "coder", "zeroproxy", "home", "page", "homepage", "zeroproxy", "link-directory", "blackshroud", "blog", "social", "australia", "zeronet", "politics", "zerotorrent", "torrent", "download", "films", "torrent", "future", "no", "more", "DNS", "takedown", "ZeroCDN", "cdn", "developers", "code", "javascript", "css", "indevelopment", "5ko", "blog", "petko", "tech", "blog", "python", "incivist", "blog", "pirate", "party", "switzerland", "politics", "forum", "revolution", "bad", "punching", "host", "file", "bphf", "security", "privacy", "anti", "ad", "track", "pub", "malware", "spyware", "exploit", "fraud", "hijack", "phishing", "typosquating", "botnet", "bad", "ssl", "worm", "trojan", "virus", "ddos", "hackshack", "deavmi", "malio", "programming", "felix", "knet", "hackshack", "hack", "shack", "deavmi", "blog", "deavmi", "nim", "python", "julia", "basic", "freebasic", "programming", "computers", "computing", "numbers", "maths", "mathematics", "nimlang", "languages", "nimrod", "C", "open", "source", "gnu", "free", "software", "software", "open", "blog", "photos", "photography", "images", "ihalutrotdn", "phantump", "adventures", "1", "blog", "journal", "diary", "twister", "win", "builds", "twister", "p2p", "blog", "win", "build", "linux", "forum", "doge", "ascii", "art", "dev.net", "forum", "raspberry", "pi", "forum", "forum", "raspberry", "pi", "raspberry", "pi", "tutorial", "help", "user", "community", "raspberrypi.net", "raspberry", "pi", "forum", "community", "g0r'blog", "test", "begining", "blog", "g0r'blog", "2", "g0r", "blog", "exploration", "heathenman", "proxy", "Alternatives", "IT", "french", "IT", "mesh", "make", "hack", "alternative", "alternatives", "opensource", "decentralized", "blockchain", "ouvert", "partage", "libre", "gnu", "Alternatives-fr", "alternative", "french", "IT", "P2P", "opensource", "zerolimit", "torrent", "download", "magnet", "movies", "musics", "games", "applications", "apps", "series", "tv", "shows", "episodes", "Simple", "Wiki", "Clone", "wiki", "info", "simple", "opensource", "sabotage.blogfa.com", "on", "zeronet", "anarchism", "anarchy", "persian", "iran", "blog", "cgm616", "blog", "new", "blog", "cgm616", "zeromaps", "brainofjtclean", "sharing", "books", "on", "zeronet", "books", "pdf", "text", "docs", "library", "download", "klaus", "zimmermann", "on", "zero", "net", "blog", "free", "software", "activism", "privacy", "Hacking", "to", "the", "Gate~", "raito", "", "spanish", "blog", "software", "libre", "gnusocial", "anime", "divided", "by", "zero", "cryptocurrencies", "darknets", "encryption", "steganography", "liberty", "divided", "by", "zero", "2", "cryptography", "cryptocurrencies", "cryptocurrency", "encryption", "steganography", "liberty", "darknet", "the", "freedom", "crate", "freedom", "crate", "linux", "flip", "a", "coin", "coin", "luck", "flip", "zero", "mail", "mail", "p2p", "messaging", "nebel", "kerze", "dampfen", "dampfer", "ezigarette", "nebelkerze", "prohibition", "vape", "vaping", "blog", "info", "quellen", "sources", "aroma", "aromen", "akku", "akkus", "verdampfer", "selbstwickelverdampfer", "import", "nikotin", "koffein", "tabak", "testris", "seite", "game", "webgame", "test", "pac", "man", "pac", "man", "pac", "man", "game", "html5", "games", "pacman", "el", "blog", "de", "roberth", "blog", "music", "videos", "images", "tutorials", "programming", "0ne", "site", "one", "site", "site", "index", "blog", "0ne", "0neSite", "0ne", "Site", "the", "last", "bit", "literature", "blog", "scifi", "fiction", "books", "images", "bit", "cannon", "torrent", "torrents", "archive", "backup", "index", "the", "pirate", "bay", "KAT", "kickass", "yify", "yts", "kickasstorrents", "shinra", "is", "a", "zero", "blog", "belge", "belgique", "francophone", "france", "shinra", "nouveau", "relative", "de", "la", "monnaie", "monnaie", "maths", "protocole", "Internet", "mesure", "zerofr", "forum", "fr", "francais", "learn", "hack", "katee", "owen", "fanpage", "NSFW", "images", "videos", "bugaga", "tiddly", "wiki", "blog", "wiki", "TiddlyWiki", "finance", "russian", "kateeowen.bit", "katee", "owen", "tits", "boobs", "nsfw", "free", "speech", "debate", "freedom", "free", "speech", "porn", "0chan", "porn", "chan", "imageboard", "images", "videos", "nsfw", "social", "blog", "personal", "blog", "thoughts", "soft", "blog", "blog", "soft", "weird", "my", "ip", "finder", "ip", "myip", "my", "ip", "Kaffiene", "Search", "search", "kaffie", "kaffiene", "find", "zeronet", "search", "engine", "engine", "FIRST", "PROGRAMMER", "blogs", "images", "social", "Himalaya", "yeti", "comments", "hints", "tips", "unix", "linux", "microcontroller", "retro", "computing", "3x71nc7", "Blog", "blog", "programming", "tutorial", "zeronet", "how-to", "tutorials", "jkne", "blog", "music", "blog", "censorship", "music", "electronica", "dance", "statik", "0", "statik", "0", "zero", "statikshock", "blog", "movies", "tv", "shows", "torrents", "warez", "p2p", "scene", "lifestyle", "drugs", "sex", "alcohol", "blog", "news", "Kaffie", "Blog", "blog", "kaffie", "games", "hacking", "tech", "zero", "zeronet", "code", "programming", "kaffiene", "beginner", "guide", "intro", "Effekt", "blog", "english", "blog", "esperanto", "communism", "effekt", "tag", "blog", "tag", "blog", "social", "europe", "european", "SlashterBlog", "blog", "decentralized", "p2p", "crypto", "LBlaze", "Personal", "Project", "Blog", "Blog", "Personal", "Projects", "Encrypted", "Web", "Designer", "website", "coder", "developer", "website", "maker", "website", "coder", "job", "Mod", "Blog", "beginner", "new", "mod", "help", "programming", "tutorial", "guide", "blog", "tech", "technology", "zeronet", "support", "coffescript"];
		result = set(soup.get_text().split()) & tags#set(keywords)
		wr = title+"["+', '.join(list(result))+":"+siteaddr+" "+peer+"\n"
		print wr
		f.write(wr)

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