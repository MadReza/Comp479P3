#!/usr/bin/python

from afinn import Afinn
import nltk.data

def score(data):
	ans = 0
	len = 0

	afinn = Afinn()
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	for block in data:
		for p in (tokenizer.tokenize(block)):
			ans += afinn.score(p)
			len += 1
			print(p + ' (' + str(afinn.score(p)) + ')')
	print('')
	return ans/len


print(score(['This is utterly excellent! this is a good test. this is a bad text. This is utterly terrible! really cool restaurant!']))
