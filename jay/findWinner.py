import re
import os
import pickle

# 1.30 problem
# Series, miniseries, limited series
# awards name containing 'series' in tweets differ from actual award name
# 
# Best Performance by an Actor in a Limited Series or a Motion Picture Made for Television

capitalized_word_pattern = '[A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*'
# '(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z\-][a-zA-Z]*)*)'
# '(Best [A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[\-([A-Z][a-zA-Z]+))]*)'

win_word_bag = ['win','winner','winners','wins','won','winning','goes to']

award_category = ['Best Motion Picture - Drama',
'Best Actress - Motion Picture - Drama',
'Best Actor - Motion Picture Musical or Comedy',
'Best Animated Feature Film',
'Best Performance by an Actress In A Television Series - Drama',
'Best Performance by an Actress In A Mini-series or Motion Picture Made for Television',
'Best Performance by an Actor in a Television Series - Drama',
'Best Actor - Motion Picture - Drama',
'Best Director - Motion Picture',
'Cecil B. DeMille Award',
'Best Supporting Actor - Motion Picture',
'Best Miniseries or Television Film',
'Best Supporting Actor in a Series, Miniseries, or Motion Picture Made for Television',
'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television',
'Best Motion Picture - Musical or Comedy',
'Best Actress - Motion Picture - Musical or Comedy',
'Best Screenplay - Motion Picture',
'Best Original Score',
'Best Performance by an Actress in a Television Series - Musical or Comedy',
'Best Supporting Actress in a Series, Miniseries, or Motion Picture Made for Television',
'Best Television Series - Drama',
'Best Supporting Actress - Motion Picture',
'Best Original Song',
'Best Foreign Language Film',
'Best Television Series - Musical or Comedy',
'Best Actor - Television Series Musical or Comedy']

# 1.30
# (.*)(for|made for) (TV|Television), no (.*)
# 'Best Supporting Actress(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)'
# 'Best Supporting Actor(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)'
l1 = ['Best Motion Picture(.*)Drama',
'Best Actress(.*)Motion Picture(.*)Drama',
'Best Actor(.*)Motion Picture(.*)Musical(.*)Comedy', #1.30 'Best Actor(.*)Motion Picture Musical(.*)Comedy'
'Best Animated Feature Film',
'Best Performance(.*)Actress(.*)(TV|Television) Series(.*)Drama',
'Best Performance(.*)Actress(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',#'Best Performance by an Actress In A Mini-series or Motion Picture Made for Television',
'Best Performance(.*)Actor(.*)(TV|Television) Series(.*)Drama',
'Best Actor(.*)Motion Picture(.*)Drama',
'Best Director(.*)Motion Picture',
'Cecil B. DeMille Award',
'Best Supporting Actor(.*)Motion Picture',
'Best Mini[\s-]*series(.*)(TV|Television) Film',
'Best Supporting Actor(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',#'Best Supporting Actor in a Series, Miniseries, or Motion Picture Made for Television',
'Best Performance(.*)Actor(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',#'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television',
'Best Motion Picture(.*)Musical(.*)Comedy',
'Best Actress(.*)Motion Picture(.*)Musical(.*)Comedy',
'Best Screenplay(.*)Motion Picture',
'Best Original Score',
'Best Performance(.*)Actress(.*)(TV|Television) Series(.*)Musical(.*)Comedy',
'Best Supporting Actress(.*)Series(.*)Mini[\s-]*series(.*)Motion Picture(.*)(for|made for) (TV|Television)',#'Best Supporting Actress in a Series, Miniseries, or Motion Picture Made for Television',
'Best (TV|Television) Series(.*)Drama',
'Best Supporting Actress(.*)Motion Picture',
'Best Original Song',
'Best Foreign Language Film',
'Best (TV|Television) Series(.*)Musical(.*)Comedy',
'Best Actor(.*)(TV|Television) Series(.*)Musical(.*)Comedy']

# Best 
# (role) [Actress, Actor, Performance Actress, Performance Actor, Director, Supporting Actor, Supporting Actress]*
# (special role) [screenplay, Original Score, Original Sone, Foreign Language Film]*
# (prefix) [Mini-Series (Miniseries)]*
# [Motion Picture, (TV|Television) Series, (TV|Television) Film]+
# (suffix) [Drama, Musical&Comedy, (for|made for) (TV|Television)]*

# Other: Cecil B. DeMille Award

keyword_list = {'role':['Actress', 'Actor', 'Performance(.*)Actress', 'Performance(.*)Actor', 'Director', 'Supporting Actor', 'Supporting Actress', ''],
'special_role':['Screenplay(.*)Motion Picture', 'Original Score', 'Original Song', 'Foreign Language Film', 'Animated Feature Film', ''],
'prefix':['Mini[\s-]*series', '',''],
'picture_type':['Motion Picture', '(TV|Television) Series', '(TV|Television) Film'],
'play_type':['Drama', 'Musical(.*)Comedy', '(for|made for) (TV|Television)', ''],
'special_award':['Cecil B. DeMille Award']}
# print keyword_list['role']

def addWildMatcher(s):
	if s != '':
		return s+'(.*)'
	else:
		return s

def makeAwardList(keyword_list):
	award_list = []
	for r in keyword_list['role']:
		r = addWildMatcher(r)
		for pf in keyword_list['prefix']:
			pf = addWildMatcher(pf)
			for pict in keyword_list['picture_type']:
				pict = addWildMatcher(pict)
				for playt in keyword_list['play_type']:
					playt = addWildMatcher(playt)
					award_list.append(re.sub(r'\(\.\*\)$', '', 'Best %s%s%s%s'%(r,pf,pict,playt)))

	for sr in keyword_list['special_role']:
		award_list.append('Best %s'%sr)

	for sa in keyword_list['special_award']:
		award_list.append(sa)

	return award_list


# award_list = makeAwardList(keyword_list)
# print award_list
# for award in l1:
# 	if award not in award_list:
# 		print award


def findWinner(fin, award_list, win_word_bag):
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
		write_dic(winnerDic, 'twt_goes_to.dict')

	for winWord in ['win','wins','has won','won']:
		winnerDic = findWinnerByWinWord(winAwardDic, winWord, curWinnerDic=winnerDic)
	write_dic(winnerDic, 'twt_winner')

def findTweetsContainAward(fin, award_list):
	dic = {}
	with open(fin) as f:
		for line in f:
			for award in award_list:
				if award not in dic:
					dic[award] = []
				m = re.findall(award ,line, re.IGNORECASE)#.split('\t')[0])
				if m:
					dic[award].append(line)
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
			if winWord == 'goes to':
				m = re.search(r'%s ([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*)'%winWord,twts,re.IGNORECASE)
			elif winWord == 'win' or winWord == 'wins' or winWord == 'has won' or winWord == 'won':
				m = re.search(r'([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*) %s(?![a-zA-Z])'%winWord,twts,re.IGNORECASE)
			if m:
				new_dic[award].append(m.group(1))
	return new_dic

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

findWinner('goldenglobes.tab',l1,win_word_bag)

# twts = 'RT @FIDM: Best Motion Picture: Drama goes to Moonlight. #GoldenGlobes https://t.co/5Zthi4cG09	karishma 	2463863802	818307524906643457	2017-01-09 04:04:52'
# winWord = 'goes to'
# m = re.search(r"%s ([A-Z][a-zA-Z]*(?=\s[A-Z])*(?:\s[A-Z][a-zA-Z\-]*)*)"%winWord,twts,re.IGNORECASE)
# print m.group(1)

# print re.sub('(\s|\(\.\*\)|\(|\)|\|)','_','Best Actor(.*)(TV|Television) Series Musical(.*)Comedy')



# '-' problem:
# Best Screenplay - La La Land
# Congratulations to Zootopia (@DisneyZootopia) - Best Animated Feature Film - #GoldenGlobes
# Best Motion Picture - Animated
# Best Motion Picture - Comedy or Musical

# could follow '-':
# Drama, Musical or Comedy, Motion Picture, Animated, Foreign Language

# Best Television Limited Series or Motion Picture Made for Television