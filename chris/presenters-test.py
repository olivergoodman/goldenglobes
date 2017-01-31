import nltk
import random
import re

movie_awards = [
"Best Motion Picture - Drama",
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
"Best Actor in a Television Drama Series",
"Best Actor in a Television Comedy Series",
"Best Actress in a Television Drama Series",
"Best Actress in a Television Comedy Series",
"Best Limited Series or Motion Picture made for Television",
"Best Actor in a Limited Series or Motion Picture made for Television",
"Best Actress in a Limited Series or Motion Picture made for Television",
"Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television",
"Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television"
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
    special_chars = ['@','#','-','!','.','\'', ',', ':']

    s = txt
    s = re.sub(regex_RT, '', s)
    s = re.sub(regex_unicode, '', s)
    s = re.sub(regex_user, '',s)

    s = s.replace('\n', ' ')
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    s = s.translate(None, ''.join(special_chars))
    return s
def find_presenters(ln):
    #   runs inside processing a tweet (aka a line of text)
    count = 0
    if ' present' in ln and 'Best' in ln:
        #want to look for award NAMe
        # additionally look proper noun token that preceeds token "present"
        print ln


# probably want regex of approx format: x presents...      best x....
""" For each Tweet:
    want to search for an award name from list
    -l ook for keyword/ extension "present"
    - store tokens of proper nouns (potential presenters), keep count I suppose


    CHUNK (organize into subj-verb trees
    look through verbs for "present/presenting"
    in tweets with verb "present":
        acquiret he subject(s) (presenters)
        as well as the object (the award)
        store to DB or dict or table or something
"""
process_text(full_file)
# s = "RT @MarkDice: Meryl Streep Begs Hollywood to Stop Donald Trump at #GoldenGlobes \ud83d\ude02\ud83d\ude02\ud83d\ude02\u2744\ufe0f\u2744\ufe0f\u2744\ufe0f\ud83d\udc8a\u26a0\ufe0f\u26a0\ufe0f https://t.co/YwpPOGMOsE"

#print re.sub()
# string = movie_awards[0].strip()
# st = nltk.word_tokenize(s)
# print nltk.pos_tag(st)
