import re
import nltk
import os
import pickle
import collections
from nltk import word_tokenize, bigrams
from nltk.tokenize import RegexpTokenizer

def process_text(file):
    """
    process_text
        params:
            file ---- name of raw text file of tweets
        desc:
            takes in a raw file of tweets, and cleans each line.
            saves the result to the file 'clean_tweets.txt'
    """
    f = open(file)
    txt = f.read()
    with open('clean_tweets.txt', 'w') as f2:
        for line in txt.splitlines():
            line = clean_text(line)
            f2.write(line + '\n')
    f.close()


def clean_text(txt):
    """
    clean_text
        params:
            txt ----- line of text, string
        desc:
            given a line of text, removes any special chars, punctiation, etc.
            returns the string all cleaned up
    """
    # want to get rid of 'RT @username: ', unicode/ emojis (\uXXXX), # symbol (not text), @ symbol (not text),
    regex_RT = r'RT '
    regex_user =  r'@[a-zA-Z0-9-_]*: '
    regex_unicode = r'\\u[a-zA-Z0-9]*'
    special_chars = ['-','!','.', ',', ':'] # remove '@'

    s = txt
    s = re.sub(regex_RT, '', s)
    s = re.sub(regex_unicode, '', s)
    s = re.sub(regex_user, '',s)

    s = s.replace('\n', ' ')
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    s = s.translate(None, ''.join(special_chars))
    return s


stopwords = ['and', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
             'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
             'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
             'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
             'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
             'did', 'doing', 'a', 'an', 'the', 'but', 'if', 'or', 'because', 'as', 'until',
             'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
             'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
             'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
             'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'theyre']

def findHost():
    """
    findHost
        desc:
            reads from 'clean_tweets.txt', only looks at tweets that mention specific keywords,
             and looks at most common bigrams in these tweets
        returns:
            name of the host
    """
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
    tokens = [word for word in tokens if word not in stopwords and word not in ignorables] #remove stopwords and ignorable chars

    bg = list(bigrams(tokens)) #find bigrams

    #ignore the bigrams from host_words (we want to find most common bigrams besides the ones in host_words)
    for item in bg:
        if (item[0] + " " + item[1]) in host_words:
            bg.remove(item)

    words_fd = nltk.FreqDist(bg)
    answer = words_fd.most_common(1)[0][0][0] + " " + words_fd.most_common(1)[0][0][1]
    return answer



trump=" trump "
rageWords=["fuck","shit","asshole","bitch"]

def readfile(file):
    """
    readFile
        desc:
            takes in a file, reads it line by line.
            helper function for findCurse
        returns
            list of tweets, read line by line
    """
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
def findCurse(rageWords,trump):
    """
    findCurse
        params:
            rageWords ---- list of curse words to search for
            trump ---- another keyword to narrow search down
        returns:
            a list of all tweets containing relating to our serach keywords
    """
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
    for each in filtSent:
        m=re.search(trump, each)
        if m!=None:
            filtSent.remove(each)
    for swords in rageWords:
        for each in filtSent:
            m=re.search(swords,each)
            if m != None :
                myfin.append (each+"\n")
    return myfin


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
    """
    findWinner
        params:
            fin ----- name of file
            award_list ----- list of award names
            win_word_bag ----- list of words to search by
        returns
            dict mapping award names and the found winner
        usage
            res = findWinner('goldenglobes.tab',award_category,win_word_bag)
            print_dic(findWinner('goldenglobes.tab',award_category,win_word_bag))
    """
    # Find tweets that mention award names
    awardDic = findTweetsContainAward(fin, award_list)

    # Find tweets that mention "win" words
    winAwardDic = findTweetsContainWin(awardDic, win_word_bag)

    # Find winner based on keyword 'goes to'
    winnerDic = findWinnerByWinWord(winAwardDic, 'goes to')

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

    winnerDic = read_dic('twt_goes_to.dict')
    if winnerDic is None:
        winnerDic = findWinnerByWinWord(winAwardDic, 'goes to')
        write_dic(winnerDic, 'twt_goes_to')

    winnerDic = read_dic('twt_winner.dict')
    if winnerDic is None:
        for winWord in ['win','wins','has won','won','win for','Best']:
            winnerDic = findWinnerByWinWord(winAwardDic, winWord, curWinnerDic=winnerDic)
        write_dic(winnerDic, 'twt_winner')

    award_winner_dic = rename_awards(extractName(winnerDic))

    return award_winner_dic

# Usage:
# 
# dic = findNominee('goldenglobes.tab')
# writeNominee(dic)

structure_words = ['A', 'a', 'And', 'and', 'But', 'but', 'The', 'the', 'You', 'you', 'Me', 'me', 'We', 'we', 'Our', 'our', 'Us', 'us' ,'He', 'he', 'She', 'she', 'I', 'It', 'it', 'That', 'that', 'They', 'they', 'Why', 'why', 'How', 'how', 'When', 'when', 'Where', 'where', 'Just', 'just', 'GoldenGlobes', 'goldenglobes', '']

def findNominee(fin):
    """
    findNominee
        desc:
            attempts to find the different nominees for each category given a file of tweets
        returns:
            a dictionary mapping awards to a list of nominees
    """
    patterns = [r'nomin(.*)Best', r'Best(.*)nominee']
    dic = {}
    with open(fin) as f:
        for line in f:
            for p in patterns:
                line = re.sub('RT', '', line)
                m = re.findall(p ,line)#, re.IGNORECASE)#.split('\t')[0])
                if m:
                    (award, nominee) = extractNominee(line)

                    if award not in dic:
                        dic[award] = set([])
                    if nominee not in structure_words:
                        dic[award].add(nominee)
    return dic

def extractNominee(text):
    sents = re.split(r'[:.!?]+',text)
    award = ''
    nominee = ''
    for s in sents:
        m = re.search(r'(.*)nominated.*(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if m:
            nominee = findNomineeName(m.group(1))
            award = m.group(2)

        m = re.search(r'(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)nominee [#@]*([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if m:
            award = m.group(1)
            nominee = m.group(2)

        m = re.search(r'presents(.*)(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*).*nominee', s)
        if m:
            nominee = findNomineeName(m.group(1))
            award = m.group(2)

        m = re.search(r'introduc[es|ed|ing|e]+(.*)as.*nominee[s]*.*(Best ((?<!@#)[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*))', s)
        if m:
            nominee = m.group(1)
            award = m.group(2)

        m = re.search(r'introduc[ing|es|ed|e]+(.*)nominated.*(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if m:
            nominee = findNomineeName(m.group(1))
            award = m.group(2)

        m = re.search(r'(.*)nominated for.*includ.*(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', s)
        if m:
            nominee = findNomineeName(m.group(1))
            award = m.group(2)

    award = award.rstrip(' ').lstrip(' ')
    nominee = nominee.rstrip(' ').lstrip(' ')
    return (award, nominee)

def findNomineeName(text):
    nominee = ''
    m = re.search(r'([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z\-]*)*)', text)
    if m:
        nominee = m.group(1)
    else:
        m = re.search(r'([@#]\w+)', text)
        if m:
            nominee = m.group(1)

    return nominee

def writeNominee(dic, folder):
    dic = collections.OrderedDict(sorted(dic.items()))
    fn = open('%s/nominee.txt'%folder,'w')
    for award in dic:
        if award == '':
            continue
        if len(dic[award]) == 0:
            continue
        fn.write('%s:\n%s\n\n'%(award, ', '.join(dic[award])))
    fn.close()


# start of presenter code...
# we have a list of presenters... it's released before the show
# search tweet for all the presenters, add to list, add to dict that matches award
# find the one that shows up the most...
def findPresenters():
    f = open('clean_tweets.txt', "r")
    txt = f.read()
    f.close()
    ## read thru each line
    new_list = []
    for line in txt.splitlines():
        if ' present' in line and 'Best ' in line and 'nominee' not in line and 'nominated' not in line:
            line = cleanPresenterTweet(line)
            temp = processPresenterTweet(line, award_words)
            if temp:
                (curr_award, presenters) = temp
                if temp not in new_list:
                    new_list.append(temp)
    return new_list

remove_words = ['GoldenGlobes', 'goldenglobes', 'golden', 'globes', 'Golden', 'Globes']
def cleanPresenterTweet(tweet):
    special_chars = ['-','!','.','\"','\'', ',', ':', '&', '#']
    # special_chars += remove_words
    s = tweet
    s = s.replace('&amp;', 'and')
    s = s.translate(None, ''.join(special_chars))
    for word in remove_words:
        if word in s:
            s = s.replace(word, '')
    return s

def matchAwards(info,award_list):
    tweet_award = word_tokenize(info)
    awards = cleanAwards(award_list)
    closest_match = ''
    best_ratio = -1.0
    for award in awards:
        match_count = 0.0
        for word in tweet_award:
            if word in award:
                match_count+=1
        curr_ratio = match_count / len(award)
        if curr_ratio > best_ratio:
            best_ratio = curr_ratio
            closest_match = award

    return closest_match

def cleanAwards(award_list):
    new_list = []
    for award in award_list:
        award = award.replace('(.*)', ' ')
        award = award.replace('|', ' ')
        award = award.replace('*', '')
        print word_tokenize(award)
        new_list.append(award)
    return new_list

award_words = ['Best', 'Motion', 'Picture', 'Drama', 'Musical', 'Comedy', 'Director', 'Actor',
                          'Actress', 'Supporting', 'Screenplay', 'Original', 'Score', 'Song', 'Foreign',
                          'Language', 'Film', 'Animated', 'Feature', 'Cecil', 'B', 'DeMille', 'Award', 'Lifetime',
                          'Achievement', 'Pictures','Role', 'Television', 'Series', 'TV']

""" takes in list of presenter tweets
    returns"""
def processPresenterTweet(tweet, award_words):
    #   runs inside processing a tweet (aka a line of text)
    award_strings_list = award_words
    # st = word_tokenize(ln,'english')
    # tokens = [word for word in word_tokenize(ln,'english') if word not in stopwords.words('english')]
    tokens = word_tokenize(tweet,'english')
    tokens = [word for word in nltk.pos_tag(tokens) if word[0].lower()=='and' or word[0] not in stopwords] #.words('english')]
    # from index of 'present', interate forward thru list until finding 'Best'
    #  then create String from best including all NNP's until it equals a dict key or is 'in' a dict key
    # then find the PRESENTERES
    #   move backwards thru list from 'present', adding to presenter str when it is '@', NNP, until its empty
    #   add presenter str to dict val of award key (values are list - 'append' presenter str


    # find index of 'present' in tokenized tweet
    verb_index = None
    for i in ['present','presenting','presentation', 'presenter']:
        try:
            verb_index = [word[0] for word in tokens].index(i) # finds index of the WORD i in the list of tuples...
            break
        except ValueError:
            continue
    if verb_index == None:
        return

    #find name of award, iterating through list of tuples [('word',POS),(..,..),...]
    curr_award=''
    # range is (present, len(tokens)]
    for i in range(verb_index, len(tokens)):
        if tokens[i][0] in award_strings_list and tokens[i][0] not in curr_award: #tokens[i][0] == 'Best': # and tokens[i][1] == 'NPP'
            curr_award += (tokens[i][0] + ' ')
        else:
            continue
    curr_award = curr_award.strip()
    # find name of presenter(s)
    presenters=[]
    curr_presenter=''
    # look for names up until the verb 'present' to avoid junk data
    for i in range(0, verb_index+1):
        if tokens[i][0] == '@':
            if curr_presenter:
                presenters.append(curr_presenter)
                curr_presenter = ''
            presenters.append(tokens[i+1][0])
        elif tokens[i][1] == 'NNP' and tokens[i][0] not in award_strings_list and tokens[i][0] not in presenters:
            # presenters.append(tokens[i][0])
            if curr_presenter: # there is already a first name in the current string
                curr_presenter += ' '
            curr_presenter += tokens[i][0]
        elif tokens[i][0] == 'and':
            if curr_presenter:
                presenters.append(curr_presenter)
            curr_presenter=''
        else:
            if curr_presenter:
                presenters.append(curr_presenter)
                curr_presenter=''
    if 0 < len(presenters) <= 2 and len(curr_award) > 1:
        return curr_award, presenters

def main(file):
    """
    main
        params:
            file ----- name of the '.tab' file
        returns:
            a dictionary detailing everything we are looking for
    """
    process_text(file) #cleans globestweets.tab, saves result to clean_tweets.txt
    answer = {
        'host': findHost(),
        'other': findCurse(rageWords,trump),
        'winner': findWinner(file,award_category,win_word_bag),
        'presenter': findPresenters(),
        'nominee': findNominee(file)
    }

    if not os.path.exists('answer'):
        os.makedirs('answer')

    fn = open('answer/host.txt','w')
    fn.write(answer['host'])
    fn.close()

    fn = open('answer/ragewords.txt','w')
    for twt in answer['other']:
        fn.write('%s\n\n'%twt)
    fn.close()

    fn = open('answer/winners.txt','w')
    for award in answer['winner']:
        fn.write('Award: %s\nWinner: %s\n\n'%(award,(answer['winner'][award])))
    fn.close()

    fn = open('answer/presenters.txt','w')
    for award in answer['presenter']:
        fn.write('Award: %s\nPresenter: %s\n\n'%(award[0], ', '.join(award[1])))
    fn.close()

    writeNominee(answer['nominee'], 'answer')

    print 'Please check \'answer\' folder'


# run everything
file_name = 'goldenglobes.tab'
main(file_name)

# print findPresenters()