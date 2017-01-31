## searching for host in tweets
import nltk
from nltk import word_tokenize, bigrams
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


def findHost(tweets):
	host_words = ["cold open", "Cold Open"]
	host_tweets = []

	f = open(tweets, "r")
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
	words_fd = nltk.FreqDist(bg) #create freqdist of bigrams

	answer = " ".join(words_fd.most_common(1)[0][0])

	return {'Host': answer}


print findHost('globestweets.txt')