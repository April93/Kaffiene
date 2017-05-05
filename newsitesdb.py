import sqlite3
import json

newsitesdb = '../1LtvsjbtQ2tY7SCtCZzC4KhErqEK3bXD4n/data/zerosites.db'
zeronamedb = '../1Name2NXVi1RDPDgf5617UoW7xA6YrhM9F/data/names.json'

conn = sqlite3.connect(newsitesdb)
c = conn.cursor()

#Get a list of site addresses and domains submitted to 'New 0net sites'
sites = set([])
domains = set([])
for row in c.execute('SELECT address FROM sites ORDER BY added desc'):
	if ".bit" not in row[0]: 
		sites.add(row[0])
	else:
		domains.add(row[0])

#Initial site count, not including domains
print len(sites)


#Look up domain names
with open(zeronamedb) as data_file:    
    data = json.load(data_file)
for d in domains:
	if d.lower() in data:
		if data[d.lower()] in sites:
			print d.lower(), " already in sites."
		else:
			sites.add(data[d.lower()])
	else:
		print d.lower(), " not found in ZeroName."

domainlookup = dict(zip(data.values(),data.keys()))

#New site count, after parsing domains
print len(sites)

#Get newsites list
newsites = {}
for site in sites:
	newsites[site] = site

#Get existing sites
filename = 'data.txt'
textfile = open(filename, 'r')
existingsitedata = textfile.read().split('\n')
textfile.close()

for line in existingsitedata:
	lsplit = line.split(":")
	asplit = lsplit[1].strip().split(" ")
	siteaddress = asplit[0]
	newsites.pop(siteaddress, '-')



#Write sites to file
f = open("peerlist.txt","w")
for site in sites:
	site = newsites.pop(site, '')
	if site is not '':
		title = "";
		if site in domainlookup:
			title = domainlookup[site];
		f.write(site+" - "+title+"\n")
f.close()