# -*- coding: UTF-8 -*-
import sqlite3
import json
import re

newsitesdb = '../1MeFqFfFFGQfa1J3gJyYYUvb5Lksczq7nH/merged-ZeroMe/ZeroMe.db'

conn = sqlite3.connect(newsitesdb)
c = conn.cursor()

followdict = {}
for row in c.execute('SELECT user_name, hub||"/"||auth_address, count(hub||"/"||auth_address) FROM follow GROUP by hub||"/"||auth_address ORDER BY count(hub||"/"||auth_address) desc'):
	followdict[row[1]] = row[2]

f = open("userdata.txt","w")
for row in c.execute('SELECT cert_user_id, hub, directory, user_name, intro FROM json WHERE hub IS NOT null and site==hub'):
	if row[0]:
		f.write(row[0])
	if row[3]:
		name = row[3].encode("UTF-8")
		name = name.replace(':','')
		name = name.replace('[','')
		name = name.replace(']','')
		name = name.replace("\n","")
		if(len(name) >= 34):
			name = name[:34]+"..."
		f.write(" - "+name)
	f.write("[")
	if row[4]:
		intro = row[4].encode("UTF-8")
		intro = re.sub(r"^Random ZeroNet user$","",intro)
		intro = re.sub(r"^新 ZeroNet 用户$","",intro)
		intro = re.sub(r"^Utilisateur ZeroNet aléatoire$","",intro)
		intro = re.sub(r"^Átlagos ZeroNet felhasználó$","",intro)
		intro = re.sub(r"^Utente ZeroNet casuale$","",intro)
		intro = re.sub(r'\n.+', '', intro)
		intro = re.sub(r'(?is)\((http|\/|\.).+\)', '', intro)
		intro = re.sub(r'(?is)http.+\/', '', intro)
		#intro = intro.replace('http.+(\/|\))','')
		intro = intro.replace(':','')
		intro = intro.replace('[','')
		intro = intro.replace(']','')
		intro = intro.replace("\n","")
		f.write(intro)
	f.write(":")
	if row[1] and row[2]:
		#"Me.ZeroNetwork.bit/?Profile/"+
		link = row[1]+"/"+row[2].replace('data/users/','')
		f.write(link)
		f.write(" "+str(followdict.get(link,'-')))
	f.write("\n")

f.close()