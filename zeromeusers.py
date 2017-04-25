# -*- coding: UTF-8 -*-
import sqlite3
import json
import re

newsitesdb = '../1MEaLzSbzXmStAowrivK1Vu4iSEWLxgZLJ/merged-ZeroMe/ZeroMe.db'

conn = sqlite3.connect(newsitesdb)
c = conn.cursor()

f = open("userdata.txt","w")
for row in c.execute('SELECT cert_user_id, hub, directory, user_name, intro FROM json WHERE hub IS NOT null and site==hub'):
	if row[0]:
		f.write(row[0])
	if row[3]:
		f.write(" - "+row[3].encode("UTF-8"))
	f.write("[")
	if row[4]:
		intro = row[4].replace("新 ZeroNet 用戶".decode("UTF-8"),"").encode("UTF-8")
		intro = intro.replace("Random ZeroNet user","").replace("新 ZeroNet 用户","").replace("Utilisateur ZeroNet aléatoire","")
		intro = intro.replace("Átlagos ZeroNet felhasználó","").replace("Utente ZeroNet casuale","")
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
		f.write(row[1]+"/"+row[2].replace('data/users/',''))
	f.write("\n")

f.close()