import re
import collections
import sys

#DO NOT USE ON DATA.TXT WITH EXISTING SITE RANK
#This tool is only for the initial appending of site rank.
#A separate tool will be developed to update site rank. Sit tight!

#Get site ranks
filename = 'peerlist.txt'
textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()
newsites = dict(item.split(" ") for item in filetext.split('\n'));

#Get existing sites
filename = 'data.txt'
textfile = open(filename, 'r')
data = textfile.read().split('\r')
textfile.close()

#Append rank to existing sites and store to a new data file
f = open("datanew.txt","w")
for line in data:
	siteaddress = line.split(":")[1].strip()
	f.write(line+" "+newsites.pop(siteaddress, '-'))
f.close()

#Store new sites in a separate file for tagging
f = open("newsites.txt","w")
for site in newsites:
	f.write("New Site[:"+site+" "+newsites.get(site,'-')+"\n\r")
f.close()