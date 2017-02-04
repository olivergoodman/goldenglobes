import re

rageWords=["fuck","shit","asshole","bitch"]
def readfile(file):
    file = open(file, "r")
    elements = []
    current = ""
    for line in file:
            elements.append(current)
            current = line.rstrip()
    elements.append(current)
    file.close()
return elements
    
def findCurse(rageWords):
myfile = readfile("globestweets.txt")
mysent= []
myfin = []
# mysent stores list of list of strings. 
# filtSent stores each filtered line of text in a list of strings.
filtSent =[]
for each in myfile:
	each =each.decode('unicode_escape').encode('ascii','ignore')
	each = each.replace('"',"").replace("?","").replace("!","").replace(".","").rstrip().split()
	mysent.append(each)

for each in mysent:
	myrem=[]
	for every in each:
		if every[0:4] in ("http", "Http"):
			myrem.append(every)
	for i in myrem:
		each.remove(i)
	filtSent.append(" ".join(each))
filtSent.pop(0)

#search through filtSent to find a sentence that contains the keyword.
myfin.append("***************************************************************\n")
myfin.append("***************************************************************\n")
myfin.append("*****The following are all tweets that contain curse words*****\n")
myfin.append("***************************************************************\n")
myfin.append("***************************************************************\n")
for swords in rageWords:
	for each in filtSent:
		m=re.search(swords,each)
		if m != None : 
			myfin.append (each+"\n")
return myFin

print(findCurse(rageWords))


