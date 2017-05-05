import re
import collections
import sys
filename = 'data.txt'
if len(sys.argv) >= 2:
	filename = sys.argv[1]
textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()
#New method might not work on some site indexes, if they don't have a ':' in front of the address
matches = re.findall(":[a-zA-Z0-9]{30,34}", filetext)

#This old method gets false positives, when the name and address of a site are the same
#matches = re.findall("[a-zA-Z0-9]{30,34}", filetext)

#Convert to lowercase because some indexes don't care about accuracy
matches = [x.lower() for x in matches]

print "Total number of sites: ",len(matches)
dups = [item for item, count in collections.Counter(matches).items() if count > 1]
print "Number of Duplicates: ", len(dups)
print "Unique sites: ", len(matches)-len(dups)
print "Duplicated Sites: ", dups