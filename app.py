import re
import nltk
import os
import pickle
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
	return myfin
#end of Chen's code
#######################################################################


#######################################################################
################              Find winner                ##############
#######################################################################

# Usage:
# res = findWinner('goldenglobes.tab',award_category,win_word_bag)
# print_dic(findWinner('goldenglobes.tab',award_category,win_word_bag))

win_word_bag = ['win','winner','winners','wins','won','winning','goes to']

award_category = ['Best Motion Picture(.*)Drama',
'Best Actress(.*)Motion Picture(.*)Drama',
'Best Actor(.*)Motion Picture(.*)Musical(.*)Comedy',
'Best Animated Feature Film',
'Best Performance(.*)Actress(.*)(TV|Television) Series(.*)Drama',
'Best Performance(.*)Actress(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best Performance(.*)Actor(.*)(TV|Television) Series(.*)Drama',
'Best Actor(.*)Motion Picture(.*)Drama',
'Best Director(.*)Motion Picture',
'Cecil B. DeMille Award',
'Best Supporting Actor(.*)Motion Picture',
'Best Mini[\s-]*series(.*)(TV|Television) Film',
'Best Supporting Actor(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best Performance(.*)Actor(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best Motion Picture(.*)Musical(.*)Comedy',
'Best Actress(.*)Motion Picture(.*)Musical(.*)Comedy',
'Best Screenplay(.*)Motion Picture',
'Best Original Score',
'Best Performance(.*)Actress(.*)(TV|Television) Series(.*)Musical(.*)Comedy',
'Best Supporting Actress(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',
'Best (TV|Television) Series(.*)Drama',
'Best Supporting Actress(.*)Motion Picture',
'Best Original Song',
'Best Foreign Language Film',
'Best (TV|Television) Series(.*)Musical(.*)Comedy',
'Best Actor(.*)(TV|Television) Series(.*)Musical(.*)Comedy']

# return a dictionary
# {AwardName: Winner}
# e.g. {'Best Motion Picture Drama':'Moonlight'}
def findWinner(fin, award_list, win_word_bag):
	# Find tweets that mention award names
	awardDic = findTweetsContainAward(fin, award_list)
	
	# Find tweets that mention "win" words
	winAwardDic = findTweetsContainWin(awardDic, win_word_bag)

	# Find winner based on keyword 'goes to'
	goesToWinnerDic = findWinnerByWinWord(winAwardDic, 'goes to')

	# Find winner based on additional keywords
	for winWord in ['win','wins','has won','won','win for','Best']:
		winnerDic = findWinnerByWinWord(winAwardDic, winWord, curWinnerDic=winnerDic)

	# Extract winner name from possible winners list &
	# Format awards name for output
	award_winner_dic = rename_awards(extractName(winnerDic))

	return award_winner_dic

def rename_awards(award_winner_dic):
	dic = {}
	for award in award_winner_dic:
		newName = re.sub('(\s|\(\.\*\)|\(|\)|\|)','_',award)
		newName = re.sub(r'\[\\s\-\]\*','',newName)
		newName = re.sub(r'_+',' ',newName).rstrip(' ')
		newName = re.sub(r'\sfor(?= made)','',newName)
		newName = re.sub(r'\sTV(?= Television)','',newName)
		dic[newName] = award_winner_dic[award]
	return dic

def findTweetsContainAward(fin, award_list):
	dic = {}
	with open(fin) as f:
		for line in f:
			for award in award_list:
				if award not in dic:
					dic[award] = []
				m = re.findall(award ,line, re.IGNORECASE)
				if m:
					dic[award].append(line)
	for award in dic:
		if len(dic[award]) == 0:
			dic.pop(award, None)
	return dic

def findTweetsContainWin(dic, win_word_bag):
	new_dic = {}
	for award in dic:
		new_dic[award] = []
		for twts in dic[award]:
			for w in win_word_bag:
				m = re.findall(r"([^.]*?%s.*)"%w,twts,re.IGNORECASE)
				if m:
					new_dic[award].append(twts)
					break
		if len(new_dic[award]) == 0:
			for twts in dic[award]:
				new_dic[award].append(twts)
	return new_dic

def findWinnerByWinWord(dic, winWord, curWinnerDic=None):
	if curWinnerDic is None:
		new_dic = {}
	else:
		new_dic = curWinnerDic
	for award in dic:
		if award not in new_dic:
			new_dic[award] = []
		for twts in dic[award]:
			if winWord == 'goes to' or winWord == 'win for':
				m = re.search(r'%s ((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*)'%winWord,twts)#,re.IGNORECASE)
			elif winWord == 'win':
				m = re.search(r'%s(?!\sfor) ((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*)'%winWord,twts)#,re.IGNORECASE)
			elif winWord == 'wins' or winWord == 'has won' or winWord == 'won':
				m = re.search(r'((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*) %s(?![a-zA-Z])'%winWord,twts)#,re.IGNORECASE)
			elif winWord == 'Best':
				m = re.search(r'((?<!@)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*) Best',twts)#,re.IGNORECASE)
			if m:
				new_dic[award].append(m.group(1))
	return new_dic

def extractName(winnerCandidateDic):
	award_winner_dic = {}

	for award in winnerCandidateDic:
		award_winner_dic[award] = topFrequentName(winnerCandidateDic[award])

	return award_winner_dic

def topFrequentName(namelist):
	ndic = {}
	maxFreq = 0
	mostFreqName = ''
	for name in namelist:
		if name in ndic:
			ndic[name] += 1
		else:
			ndic[name] = 1
		if ndic[name] > maxFreq:
			maxFreq = ndic[name]
			mostFreqName = name
	if mostFreqName == '':
		return 'not found'
	return mostFreqName

def read_dic(fn):
	if os.path.isfile(fn):
		with open(fn, 'r') as f:
			awardDic = pickle.load(f)
		return awardDic
	else:
		return None

def write_dic(dic, folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
	with open('%s.dict'%folder,'w') as f:
		pickle.dump(dic,f)
	for award in dic:
		fn = open('%s/%s.txt'%(folder,re.sub('(\s|\(\.\*\)|\(|\)|\|)','_',award)),'w')
		for twts in dic[award]:
			fn.write('%s\n'%twts)
		fn.close()

def print_dic(dic):
	for key in dic:
		print '%s\n%s\n'%(key,dic[key])

def findWinnerWithWritingFiles():
	awardDic = read_dic('twt_Award.dict')
	if awardDic is None:
		awardDic = findTweetsContainAward(fin, award_list)
		write_dic(awardDic, 'twt_Award')

	winAwardDic = read_dic('twt_Win_Award.dict')
	if winAwardDic is None:
		winAwardDic = findTweetsContainWin(awardDic, win_word_bag)
		write_dic(winAwardDic, 'twt_Win_Award')
	
	goesToWinnerDic = read_dic('twt_goes_to.dict')
	if goesToWinnerDic is None:
		goesToWinnerDic = findWinnerByWinWord(winAwardDic, 'goes to')
		write_dic(goesToWinnerDic, 'twt_goes_to.dict')

	winnerDic = read_dic('twt_winner')
	if winnerDic is None:
		for winWord in ['win','wins','has won','won','win for','Best']:
			winnerDic = findWinnerByWinWord(winAwardDic, winWord, curWinnerDic=winnerDic)
		write_dic(winnerDic, 'twt_winner')

	award_winner_dic = rename_awards(extractName(winnerDic))

	return award_winner_dic


#######################################################################
################              /Find winner               ##############
#######################################################################



"""
main
	params:
		file ----- name of the '.tab' file
	returns:
		a dictionary detailing everything we are looking for
"""
def main(file):
	process_text(file) #cleans globestweets.tab, saves result to clean_tweets.txt

	rageWords=["fuck","shit","asshole","bitch"]
	foundRageWords=findCurse(rageWords)
	
	answer = {
		'host': findHost(), ## <------ add your answers here. we will return an object with all the found results
		'other': foundRageWords
	}
	return answer



# run everything
file_name = 'goldenglobes.tab'
print main(file_name);
