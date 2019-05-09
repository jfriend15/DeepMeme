''' Builds the dictionary we need. '''

import nltk
import pickle

data_dict = {}

text = []
top = open("Data/toptext.txt", "r")
bottom = open("Data/bottomtext.txt", "r")
text.extend(top.readlines())
text.extend(bottom.readlines())
text = [t.strip() for t in text]
# TODO strip better. take out commas and weird characters.

words = [w for t in text for w in t.split(' ')]
word_set = set(words)

for w in word_set:
	token = nltk.word_tokenize(w)
	tag = nltk.pos_tag(token)[0][1]

	if tag in data_dict:
		data_dict[tag].append(token)
	else:
		data_dict[tag] = [token]
	
		
print(data_dict.keys())
print(data_dict['NNP'])

# for w in word_set:
	# find first/best 100 similar words in glove
	# tokenize and tag
	# add to bigger dictionary

# save both dictionaries with pickle

