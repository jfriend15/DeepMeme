''' Builds the dictionary we need. '''

import nltk
import pickle
import numpy as np 
import string

def build_grammar_dict():
	data_dict = {}

	text = []
	top = open("Data/toptext.txt", "r")
	bottom = open("Data/bottomtext.txt", "r")
	text.extend(top.readlines())
	text.extend(bottom.readlines())

	punctuation = string.punctuation.replace("'", "")

	text = [t.strip().lower() for t in text]
	text = [t.translate(str.maketrans('', '', punctuation)) for t in text]

	words = [w for t in text for w in t.split(' ')]
	word_set = set(words)

	for w in word_set:
		token = nltk.word_tokenize(w)
		tag = nltk.pos_tag(token)[0][1]

		if tag in data_dict:
			data_dict[tag].append(token)
		else:
			data_dict[tag] = [token]

	return data_dict

# https://stackoverflow.com/questions/37793118/load-pretrained-glove-vectors-in-python
def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r',encoding='utf-8')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model
		
def save_dict(dictionary, filename):
	file = open('Data/' + filename + '.pkl', 'wb')
	pickle.dump(dictionary, file)
	file.close()


def main():
	g = build_grammar_dict()
	save_dict(g, 'grammarDict')
	m = loadGloveModel('Data/glove.twitter.27B.25d.txt')
	save_dict(m, 'gloveDict')


if __name__ == '__main__':
	main()
