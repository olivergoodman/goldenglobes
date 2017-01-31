import re
<<<<<<< HEAD

=======
import nltk
from nltk import word_tokenize, bigrams
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


"""
process_text
	params:
		file ---- name of raw text file of tweets
	desc:
		takes in a raw file of tweets, and cleans each line.
		saves the result to the file 'clean_tweets.txt'
"""
def process_text(file):
    f = open(file)
    txt = f.read()
    for line in txt.splitlines():
        line = clean_text(line)
        with open('clean_tweets.txt', 'a') as f2:
        	f2.write(line + '\n')
    f.close()


"""
clean_text
	params:
		txt ----- line of text, string
	desc:
		given a line of text, removes any special chars, punctiation, etc.
		returns the string all cleaned up
"""
def clean_text(txt):
    # want to get rid of 'RT @username: ', unicode/ emojis (\uXXXX), # symbol (not text), @ symbol (not text),
    regex_RT = r'RT '
    regex_user =  r'@[a-zA-Z0-9-_]*: '
    regex_unicode = r'\\u[a-zA-Z0-9]*'
    special_chars = ['@','-','!','.', ',', ':']

    s = txt
    s = re.sub(regex_RT, '', s)
    s = re.sub(regex_unicode, '', s)
    s = re.sub(regex_user, '',s)

    s = s.replace('\n', ' ')
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    s = s.translate(None, ''.join(special_chars))
    return s


"""
findHost
	desc:
		reads from 'clean_tweets.txt', only looks at tweets that mention specific keywords,
		 and looks at most common bigrams in these tweets
	returns:
		name of the host
"""
def findHost():
	host_words = ["cold open", "Cold Open"]
	host_tweets = []

	f = open('clean_tweets.txt', "r")
	line = f.readline()

	## read thru each line
	while line:
		#only save tweets that mention cold open
		for w in host_words:
			if (w in line and line not in host_tweets):
				host_tweets.append(line)
		#go on to next line
		line = f.readline()
	f.close()

	## all host tweets
	host = "".join(host_tweets) #make tweets one big string
	host.decode('unicode_escape').encode('ascii','ignore') #convert to unicode chars
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(host) #remove punctiation
	ignorables = ['https', 'http', '#', 't', 'co']
	tokens = [word for word in tokens if word not in stopwords.words('english') and word not in ignorables] #remove stopwords and ignorable chars

	bg = list(bigrams(tokens)) #find bigrams

	#ignore the bigrams from host_words (we want to find most common bigrams besides the ones in host_words)
	for item in bg:
		if (item[0] + " " + item[1]) in host_words:
			bg.remove(item)

	words_fd = nltk.FreqDist(bg)
	answer = words_fd.most_common(1)[0][0][0] + " " + words_fd.most_common(1)[0][0][1]
	return answer


#################################################
#start of Chen's code
# read file from Chen
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

# find curse function from Chen
def findCurse(rageWords):
myfile = readfile("clean_tweets.txt")
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
#end of Chen's code
#######################################################################



"""
main
	params:
		file ----- name of the '.txt' file
	returns:
		a dictionary detailing everything we are looking for
"""
def main(file):
    rageWords=["fuck","shit","asshole","bitch"]
	process_text(file) #cleans globestweets.txt, saves result to clean_tweets.txt
	foundRageWords=findCurse(rageWords)
	answer = {
		'host': findHost()

	}
	return answer



# run everything
file_name = 'globestweets.txt'
print main(file_name);
>>>>>>> origin/master
