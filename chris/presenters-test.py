import nltk
import random
import re
from nltk import word_tokenize, bigrams, tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

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
test_file = 'globestweets_test.txt'
full_file = 'globestweets.txt'

def process_text(file):
    f = open(file)
    txt = f.read()
    for line in txt.splitlines():
        line = clean_text(line)
        find_presenters(line)
    f.close()

def clean_text(txt):
    # want to get rid of 'RT @username: ', unicode/ emojis (\uXXXX), # symbol (not text), @ symbol (not text),
    regex_RT = r'RT '
    regex_user =  r'@[a-zA-Z0-9-_]*: '
    regex_unicode = r'\\u[a-zA-Z0-9]*'
    special_chars = ['-','!','.','\"','\'', ',', ':', '&'] #'@','#',
    s = txt
    s = re.sub(regex_RT, '', s)
    s = re.sub(regex_unicode, '', s)
    s = re.sub(regex_user, '',s)

    s = s.replace('&amp;', '&')
    s = s.replace('\n', ' ')
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    s = s.translate(None, ''.join(special_chars))
    return s

def find_presenters(ln):
    #   runs inside processing a tweet (aka a line of text)
    if ' present' in ln and 'Best' in ln:
        # st = word_tokenize(ln,'english')
        # tokens = [word for word in word_tokenize(ln,'english') if word not in stopwords.words('english')]
        tokens = word_tokenize(ln,'english')
        tokens = [word for word in nltk.pos_tag(tokens) if word[0] not in stopwords.words('english')]
        # from index of 'present', interate forward thru list until finding 'Best'
        #  then create String from best including all NNP's until it equals a dict key or is 'in' a dict key
        # then find the PRESENTERES
        #   move backwards thru list from 'present', adding to presenter str when it is '@', NNP, until its empty
        #   add presenter str to dict val of award key (values are list - 'append' presenter str


        # find index of 'present' in tokenized tweet
        verbi = None
        for i in ['present','presenting','presentation', 'presenter']:
            try:
                verbi = [word[0] for word in tokens].index(i) # finds index of the WORD i in the list of tuples...
                break
            except ValueError:
                continue
        if verbi == None:
            return

        #find name of award, iterating through list of tuples [('word',POS),(..,..),...]
        curr_award=''
        # make this porgramatically... see bottom of code
        award_strings_list = ['Best', 'Motion', 'Picture', 'Drama', 'Musical', 'Comedy', 'Director', 'Actor',
                              'Actress', 'Supporting', 'Screenplay', 'Original', 'Score', 'Song', 'Foreign',
                              'Language', 'Film', 'Animated', 'Feature', 'Cecil', 'B', 'DeMille', 'Award', 'Lifetime',
                              'Achievement', 'Pictures'] # performance was added afterwards
        # range is (present, len(tokens)]
        for i in range(verbi+1, len(tokens)):
            if tokens[i][0] == 'Best': # and tokens[i][1] == 'NPP'
                curr_award += tokens[i][0]
            # do i need award_strings list??
            elif tokens[i][1] == 'NNP' and tokens[i][0] in award_strings_list:
                curr_award += ' '+tokens[i][0]   # need to space the words so it matches
            else:
                continue

        # find name of presenter(s)
        award_strings_list.append('Performance')
        presenters=[]
        for i in range(0, len(tokens)):
            if tokens[i][0] == '@':
                presenters.append(tokens[i+1][0])
            elif tokens[i][1] == 'NNP' and tokens[i][0] not in award_strings_list and tokens[i][0] not in presenters:
                presenters.append(tokens[i][0])
            else:
                continue
        print '{0}: {1}'.format(curr_award, presenters)
        return curr_award, presenters


# probably want regex of approx format: x presents...      best x....
""" For each Tweet:
    want to search for an award name from list
    - look for keyword/ extension "present"
    - store tokens of proper nouns (potential presenters), keep count I suppose


    CHUNK (organize into subj-verb trees
    look through verbs for "present/presenting"
    in tweets with verb "present":
        acquiret he subject(s) (presenters)
        as well as the object (the award)
        store to DB or dict or table or something
"""
process_text(full_file)


s = "RT @goldenglobes: Kristen Wiig and @SteveCarell team up to present Best Motion Picture - Animated. #GoldenGlobes https://t.co/456617TZCG"
g = "RT @goldenglobes: .@johnlegend is now presenting a clip from @LaLaLand, nominated for Best Motion Picture - Comedy or Musical at the #Golde\u2026"
md = "RT @goldenglobes: Here to present Best Performance By An Actress in a Motion Picture - Musical or Comedy is Matt Damon! #GoldenGlobes https\u2026"

s = clean_text(s)
# st = word_tokenize(s,'english')
# st = [word for word in nltk.pos_tag(st) if word[0] not in stopwords.words('english')]
# print [word[0] for word in st].index('present') # see find_presenters()

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


