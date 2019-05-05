'''
Perplexity object returns perplexity score for grammatical structure with the 
"perplexity" function. (Sorry.)

Currently returns the probability of consecutive grammar tags. We create a probability
distribution of all possible tags following a certain "context" (preceding tags.)
'''

import numpy as np
import nltk
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist, ELEProbDist


class Perplexity():

	def __init__(self):
		# We rely on the grammar-tagged data
		self.cfdist = self.init_grammar_freqdist('Data/grammars.txt')
		self.cpdist = ConditionalProbDist(self.cfdist, ELEProbDist, 10)

	# @ https://stackoverflow.com/questions/37793118/load-pretrained-glove-vectors-in-python
	def load_glove(gloveFile):
		''' Not currently in use 

		# to evaluate word choice
		# build dictionary from top text and bottom text
		# use glove twitter to get 100 closest words to each word in set(dict)
		# if those words are of the types that should come next, great
		'''
		print("Loading Glove Model")
		f = open(gloveFile,'r')
		model = {}
		for line in f:
			splitLine = line.split()
			word = splitLine[0]
			embedding = np.array([float(val) for val in splitLine[1:]])
			model[word] = embedding
		print("Done.",len(model)," words loaded!")
		return model

	def perplexity(self, caption):
		''' Takes in a string and returns the perplexity of its grammatical structure. '''
		words = nltk.word_tokenize(caption)
		tags = nltk.pos_tag(words)
		tags = [tag[1] for tag in tags]

		N = len(tags)
		P = 1
		for t in range(len(tags)):
			context = ' '.join(tags[:t])
			word = tags[t]
			P *= 1 / self.probability(context, word)

		perplexity = P ** (float(1/N))
		return perplexity

	def init_grammar_freqdist(self, grammar_file, context_length=30):
		grammars = open(grammar_file, 'r')
		cfdist = ConditionalFreqDist()

		cl = context_length
		for line in grammars.readlines():
			line = line[1:].strip('\n').split(' ')
			for t in range(len(line)):
				if t-cl>0:
					context = ' '.join(line[t-cl:t])
				else:
					context = ' '.join(line[:t])
				cfdist[context][line[t]] += 1

		grammars.close()
		return cfdist

	def probability(self, context, word):
		return self.cpdist[context].prob(word)
