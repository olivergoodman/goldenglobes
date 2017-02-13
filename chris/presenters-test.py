import nltk
import random
import re
from nltk import word_tokenize, bigrams, tokenize
# from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# nltk.download('all')
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

movie_awards = [
"Best Motion Picture Drama",
"Best Motion Picture - Musical or Comedy",
"Best Director",
"Best Actor - Motion Picture Drama",
"Best Actor - Motion Picture Musical or Comedy",
"Best Actress - Motion Picture Drama",
"Best Actress - Motion Picture Musical or Comedy",
"Best Supporting Actor - Motion Picture",
"Best Supporting Actress - Motion Picture",
"Best Screenplay",
"Best Original Score",
"Best Original Song",
"Best Foreign Language Film",
"Best Animated Feature Film",
"Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures"
]
tv_awards=[
"Best Drama Series",
"Best Comedy Series",
"Best Actor in a (TV|Television) Drama Series",
"Best Actor in a (TV|Television) Comedy Series",
"Best Actress in a (TV|Television) Drama Series",
"Best Actress in a (TV|Television) Comedy Series",
"Best Limited Series or Motion Picture made for (TV|Television)",
"Best Actor in a Limited Series or Motion Picture made for (TV|Television)",
"Best Actress in a Limited Series or Motion Picture made for (TV|Television)",
"Best Supporting Actor in a Series, Limited Series or Motion Picture made for (TV|Television)",
"Best Supporting Actress in a Series, Limited Series or Motion Picture made for (TV|Television)"
]

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

test_file = 'globestweets_test.txt'
full_file = 'globestweets.txt'

def process_text(file):
    f = open(file)
    txt = f.read()
    for line in txt.splitlines():
        line = clean_text(line)
        print line
        # find_presenters(line)
    f.close()

def clean_text(txt):
    # want to get rid of 'RT @username: ', unicode/ emojis (\uXXXX), # symbol (not text), @ symbol (not text),
    regex_RT = r'RT '
    regex_user =  r'@[a-zA-Z0-9-_]*: '
    regex_unicode = r'\\u[a-zA-Z0-9]*'
    special_chars = ['-','!','.','\"','\'', ',', ':', '&', '#'] #'@','#',
    s = txt
    s = re.sub(regex_RT, '', s)
    s = re.sub(regex_unicode, '', s)
    s = re.sub(regex_user, '',s)

    s = s.replace('&amp;', '&')
    s = s.replace('\n', ' ')
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    s = s.translate(None, ''.join(special_chars))
    return s
presenter_list = ['Ben Affleck', 'Casey Affleck', 'Kristen Bell', 'Annette Bening', 'Pierce Brosnan', 'Naomi Campbell', 'Jessica Chastain', 'Leonardo DiCaprio', 'Gal Gadot', 'Hugh Grant', 'Jon Hamm', 'Chris Hemsworth', 'Felicity Jones', 'John Legend', 'Ryan Reynolds', 'Sting', 'Emma Stone', 'Carrie Underwood', 'Vince Vaughn', 'Carl Weathers', 'Kristen Wiig', 'Drew Barrymore', 'Steve Carell', 'Priyanka Chopra', 'Matt Damon', 'Viola Davis', 'Laura Dern', 'Goldie Hawn', 'Anna Kendrick', 'Nicole Kidman', 'Brie Larson', 'Diego Luna', 'Sienna Miller', 'Mandy Moore', 'Jeffrey Dean Morgan', 'Timothy Olyphant', 'Chris Pine', 'Eddie', 'Redmayne', 'Zoe', 'Saldana', 'Amy', 'Schumer', 'Sylvester', 'Stallone', 'Justin', 'Theroux', 'Milo', 'Ventimiglia', 'Sofia', 'Vergara', 'Reese', 'Witherspoon', 'Sunny', 'Pawar', 'Michael', 'Keaton', 'Cuba', 'Gooding', 'Jr.']


# what needs to be done:
    # ignore word 'and' when cleaning, search for and to separate 2 presenters
    # each presenter has own string var, append first+last name(if applicable/ not twitter handle)

    #dict stuff. Need function to match variations of award names to the specific dict key values to properly add them
        # maybe use list of variations (best motion picture animated, best fanimated feature film...
        # 2nd idea: use keywords if 'animated' in award, if 'actor/ actress', if 'TV/Television', etc. etc.
        #  if it's in the list then add it to the specific dict key
def find_presenters(ln):
    #   runs inside processing a tweet (aka a line of text)
    if ' present' in ln and 'Best' in ln and 'nominee' not in ln:
        # st = word_tokenize(ln,'english')
        # tokens = [word for word in word_tokenize(ln,'english') if word not in stopwords.words('english')]
        tokens = word_tokenize(ln,'english')
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
        # make this programatically... see bottom of code
        award_strings_list = ['Best', 'Motion', 'Picture', 'Drama', 'Musical', 'Comedy', 'Director', 'Actor',
                              'Actress', 'Supporting', 'Screenplay', 'Original', 'Score', 'Song', 'Foreign',
                              'Language', 'Film', 'Animated', 'Feature', 'Cecil', 'B', 'DeMille', 'Award', 'Lifetime',
                              'Achievement', 'Pictures','Role', 'Television', 'Series', 'TV'] # performance was added afterwards
        # range is (present, len(tokens)]
        for i in range(verb_index+1, len(tokens)):
            if tokens[i][0] == 'Best': # and tokens[i][1] == 'NPP'
                curr_award += tokens[i][0]
            # do i need award_strings list??
            elif tokens[i][1] == 'NNP' and tokens[i][0] in award_strings_list:
                curr_award += ' '+tokens[i][0]   # need to space the words so it matches
            else:
                continue

        # find name of presenter(s)
        award_strings_list.append('Performance')
        award_strings_list.append('GoldenGlobes')
        presenters=[]
        curr_presenter=''
        found_and=''
        # look for names up until the verb 'present' to avoid junk data
        for i in range(0, verb_index+1):
            if tokens[i][0] == '@':
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
        print '{0}: {1}'.format(curr_award, presenters)
        return curr_award, presenters

def findPresenters():
    f = open('clean_tweets.txt', "r")
    txt = f.read()
    f.close()
    ## read thru each line
    for line in txt.splitlines():
        if ' present' in line and 'Best ' in line and 'nominee' not in line and 'nominated' not in line:
            line = cleanPresenterTweet(line)
            processPresenterTweet(line, award_words)
            # print line
    return

# remove_words = ['GoldenGlobes', 'goldenglobes', 'golden', 'globes', 'Golden', 'Globes']
def cleanPresenterTweet(tweet):
    special_chars = ['-','!','.','\"','\'', ',', ':', '&', '#']
    # special_chars += remove_words
    s = tweet
    s = s.replace('&amp;', 'and')
    s = s.translate(None, ''.join(special_chars))
    return s

common_words = ['Best', 'Picture','Motion','Screenplay', '']


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
    if 0 < len(presenters) <= 2 and curr_award:
        print '{0}: {1}'.format(curr_award, presenters)
        return curr_award, presenters

# s = clean_text(s)
# st = word_tokenize(s,'english')
# print st
# st = [word for word in nltk.pos_tag(st) if word[0].lower()=='and' or word[0] not in stopwords] #.words('english')]
# print st

print findPresenters()
string = "Eddie will be presenting the Best Film Comedy/Musical award alongside Jessica Chastain at the GoldenGlobes ceremon"


# probably want regex of approx format: x presents...      best x....
""" For each Tweet:
    want to search for an award name from list
    - look for keyword/ extension "present"
    - store tokens of proper nouns (potential presenters), keep count I suppose
"""
process_text(full_file)


s = "RT @goldenglobes: Kristen Wiig and @SteveCarell team up to present Best Motion Picture - Animated. #GoldenGlobes https://t.co/456617TZCG"
g = "RT @goldenglobes: .@johnlegend is now presenting a clip from @LaLaLand, nominated for Best Motion Picture - Comedy or Musical at the #Golde\u2026"
md = "RT @goldenglobes: Here to present Best Performance By An Actress in a Motion Picture - Musical or Comedy is Matt Damon! #GoldenGlobes https\u2026"
z = "RT @goldenglobes: .@amyschumer &amp; @goldiehawn present Best Performance by an Actor in a Motion Picture - Musical or Comedy. #GoldenGlobes ht\u2026"

s = clean_text(s)

st = word_tokenize(s,'english')
# print st
st = [word for word in nltk.pos_tag(st) if word[0].lower()=='and' or word[0] not in stopwords] #.words('english')]
# print st

# print find_presenters(s)

def make_tokenized_award_list(lst):
    mov_award = [clean_text(string) for string in lst]
    mov_award = [word_tokenize(word,'english') for word in mov_award] #if word not in stopwords.words('english')]
    mov_award = [[str for str in word if str not in stopwords.words('english')] for word in mov_award]
    mov_award = [' '.join(movie) for movie in mov_award]
    return mov_award

def make_presenter_dict(lst1):
    awards = make_tokenized_award_list(movie_awards)
    presenter_dict = {award: [] for award in awards}
    return presenter_dict
# print make_presenter_dict(movie_awards)

# makes list of all words used in award names (e.g. best, screenplay, originla, actor, actress, etc.)
# awards = [clean_text(string) for string in movie_awards]
# awards = [word_tokenize(word,'english') for word in awards] #if word not in stopwords.words('english')]
# awards = [[str for str in word if str not in stopwords.words('english')] for word in awards]
# award_strings = []
# for i in awards:
#     print i
#     for j in i:
#         if j not in award_strings:
#             award_strings.append(j)
# print award_strings


