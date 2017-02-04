import re
import os
import pickle

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
				m = re.findall(award ,line, re.IGNORECASE)#.split('\t')[0])
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

print_dic(findWinner('goldenglobes.tab',award_category,win_word_bag))
