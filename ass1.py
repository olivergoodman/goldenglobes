import re

rageWords=["fuck","shit","asshole"]
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
    
    
myfile = readfile("globestweets.txt")
mysent= []
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
print("***************************************************************")
print("***************************************************************")
print("*****The following are all tweets that contain curse words*****")
print("***************************************************************")
print("***************************************************************")
for swords in rageWords:
	for each in filtSent:
		m=re.search(swords,each)
		if m != None : 
			print (each)
			
