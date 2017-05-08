# -*- coding: UTF-8 -*-
import sqlite3
import json
import re
import sys

zeromedb = '../1MeFqFfFFGQfa1J3gJyYYUvb5Lksczq7nH/merged-ZeroMe/ZeroMe.db'
user = '1NWh3WAty57FH8at1WtrZigMrdhrDkuPzh'
if(len(sys.argv) == 2):
	user = sys.argv[1]

conn = sqlite3.connect(zeromedb)
c = conn.cursor()

#Get approximate number of followers for all users
followdict = {}
for row in c.execute('SELECT user_name, auth_address, count(auth_address) FROM follow GROUP by auth_address ORDER BY count(auth_address) desc'):
	followdict[row[1]] = row[2]

#Find followers for a particular user, given an auth_adress
followers = set([])
for row in c.execute('SELECT json_id,user_name FROM follow WHERE auth_address=\"'+user+'\"'):
	followers.add(row[0])

#Run through list of followers and grab/format data
f = open("followers.txt","w")
for follow in followers:
	for row in c.execute('SELECT cert_user_id, hub, directory, user_name, intro FROM json WHERE json_id='+str(follow)):
		if row[0]:
			f.write(row[0])

			#Name formatting/cleanup
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

			#Intro formatting/cleanup
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
				intro = intro.replace(':','')
				intro = intro.replace('[','')
				intro = intro.replace(']','')
				intro = intro.replace("\n","")
				f.write(intro)
			f.write(":")

			#Generate ZeroMe link
			if row[1] and row[2]:
				link = row[1]+"/"+row[2].replace('data/users/','')
				f.write(link)
				f.write(" "+str(followdict.get(row[2].replace('data/users/',''),'0')))
			f.write("\n")
f.close()