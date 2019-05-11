import math
import random
import pickle
import os
import numpy as np

import dictBuilder
import grammarParser


class memeBuilder:
    ABSORB_STATE = 55257680
    GENERICS = ['NNS', 'NN', 'JJ', 'IN', 'VBN', 'CD', 'DT', 'VB',
                '$', 'RB', '``', 'PRP', 'NNP', 'WP', 'CC', 'PRP$',
                'VBD', 'VBZ', 'WRB']

    FINISH_SENTENCE = (-1, "")

    SENTENCE_BASE_SCORE = 100

    def __init__(self):  # input alpha, gamma, its, dicts
        self.topStates = []
        self.bottomStates = []

        """Q is a dictionary whose reference is a (state, action) tuple. 
        We will add these as we encounter them"""
        self.Q = {}

        iterations = 100
        alpha = 0.5
        gamma = 0.9

        self.finishedMeme = ((), ())

        # Retrieve generated grammar in string
        startState = self.getStartState().strip(".")
        splitText = self.splitText(startState)
        print("Start state is ", startState)

        self.glove = self.load_dict('Data/gloveDict.pkl')
        self.POSDict = self.load_dict('Data/grammarDict.pkl')

        # print(self.POSDict)

        for i in range(iterations):
            tt = self.topText(alpha, gamma, splitText[0])  # top start

        for i in range(iterations):
            bt = self.bottomText(alpha, gamma, splitText[1], tt)  # bottom start

        finishedMeme = (tt, bt)

        print(finishedMeme)

    def load_dict(self, file):
        """Helper function"""
        dict_file = open(file, "rb")
        return pickle.load(dict_file)

    def getStartState(self):
        """Retrives a generated grammar skeleton. Returns a string."""
        grammarData = open('Data/genGrammars.txt', 'r')
        grammars = [line.strip() for line in grammarData.readlines()]
        # return grammars[random.randint(0, len(grammars)-1)]
        return grammars[0]

    """Returns the top and bottom text in list format"""

    def splitText(self, sentence):
        texts = sentence.split(' | ')
        return texts

    def topText(self, alpha, gamma, startState):
        # s will change, grammar will not
        s = startState
        grammar = startState

        actions = self.getPossibleActions(s, grammar)
        actionValues = {}

        while not s == memeBuilder.ABSORB_STATE:

            if self.isFinished(s):
                actions.append(self.FINISH_SENTENCE)

            for action in actions:
                if (s, action) not in self.Q.keys():
                    self.Q[(s, action)] = 0

                actionValues[action] = self.Q[(s, action)]

            chosenAction = self.softMax(actionValues)
            print('Chosen action is ', chosenAction)

            nextState = self.getNextState(s, chosenAction)
            print('Next state is ', nextState)

            if not self.topStates.__contains__(nextState):
                self.topStates.append(nextState)

            choiceValue = self.getWordScore(s, chosenAction[0], chosenAction[1], 0)

            r = choiceValue

            value = (1 - alpha) * self.Q.get((s, chosenAction)) + alpha * (
                        r + gamma * self.maxExpectedNextState(nextState, grammar, actions))

            print('Overall value is', value)
            self.Q[chosenAction] = value

            s = nextState

        return s

    def bottomText(self, alpha, gamma, startState, topText):
        s = startState
        grammar = startState

        actions = self.getPossibleActions(s, grammar)
        actionValues = {}

        while not s == memeBuilder.ABSORB_STATE:

            for action in actions:
                if (s, action) not in self.Q.keys():
                    self.Q[(s, action)] = 0

                actionValues[action] = self.Q[(s, action)]

            chosenAction = self.softMax(actionValues)

            nextState = self.getNextState(s, chosenAction)

            if not self.bottomStates.__contains__(nextState):
                self.bottomStates.append(nextState)

            choiceValue = self.getWordScore(s, chosenAction[0], chosenAction[1], topText)

            r = choiceValue

            value = (1 - alpha) * self.Q.get(s, chosenAction) + alpha * (
                        r + gamma * self.maxExpectedNextState(nextState, grammar))

            self.Q[chosenAction] = value

            s = nextState

        return s

    def getNextState(self, state, action):

        if state == self.FINISH_SENTENCE:
            return self.ABSORB_STATE

        newState = []

        for word in state.split(' '):
            newState.append(word)

        newState[action[0]] = action[1]
        return ' '.join(newState)

    def maxExpectedNextState(self, state, grammar, possibleActions):

        pair = (state, possibleActions[0])
        if pair not in self.Q.keys():
            self.Q[pair] = 0

        bestValue = self.Q[pair]

        for action in possibleActions:
            if (state, action) not in self.Q.keys():
                self.Q[(state, action)] = 0
            v = self.Q[(state, action)]
            if v > bestValue:
                bestValue = v

        return v

    """Takes a dict with actions and their values, and chooses one based on the softmax function"""

    def softMax(self, actionValues):
        actionProbs = {}
        # print(actionValues)
        denom = 0
        for action, value in actionValues.items():
            denom += math.pow(math.e, value)

        for action, value in actionValues.items():
            actionProbs[action] = math.pow(math.e, value) / denom

        rand = random.random()

        total = 0
        for action, prob in actionProbs.items():
            total += prob
            if rand < total:
                return action

        return 0

    """Takes as parameters the sentence, the index of the word to be replaced, the new word, and top text if it's bottom
    text (otherwise topText is 0)"""

    def getWordScore(self, sentence, index, newWord, topText):
        """TODO: give the value of replacing the word at index index with the given word"""

        def sentenceScore(s):

            discount = 0

            for word in s:
                value = score(s, word)
                discount += value

            discount /= len(s)

            return self.SENTENCE_BASE_SCORE/discount



        def score(context, word):
            '''Returns average Euclidean distance of the new word
            from the old words from embeddings in GLOVE.'''
            avg_dist = []
            if word not in self.glove.keys():
                return 20

            new_embd = self.glove[word]
            for old_word in context:
                # If either word isn't in glove or the old word is generic,
                # give it a far distance to motivate not picking it
                if self.isGeneric(old_word) or old_word not in self.glove.keys():
                    dist = 20
                else:
                    embd = self.glove[old_word]
                    dist = np.linalg.norm(embd - new_embd)

                avg_dist.append(dist)

            return sum(avg_dist) / len(avg_dist)

        if index == -1:
            sentence = sentence.split(' ')
            return sentenceScore(sentence)

        sentence = sentence.split(' ')
        oldWord = sentence[index]
        del sentence[index]

        oldScore = score(sentence, oldWord)
        newScore = score(sentence, newWord)

        # print('Old words: ', sentence)
        # print(oldWord, oldScore)
        # print(newWord, newScore)

        return newScore - oldScore

    def getPossibleActions(self, sentence, grammar):
        # TODO why for all words at once?
        # for all words not filled yet? for the next word
        possibleActions = []
        sentence = sentence.split(' ')
        grammar = grammar.split(' ')
        for i in range(len(sentence)):
            # print(grammar[i])
            possibleWords = self.getWordsForPartOfSpeech(grammar[i])
            for word in possibleWords:
                possibleActions.append((i, ''.join(word)))

        return possibleActions

    def isFinished(self, sentence):
        for word in sentence:
            if self.isGeneric(word):
                return 0

        return 1

    def getWordsForPartOfSpeech(self, partOfSpeech):
        """Returns list of tokenized words from dataset given a POS"""
        return self.POSDict[partOfSpeech]

    def isGeneric(self, word):
        if self.GENERICS.__contains__(word):
            return 1
        return 0


def main():
    if not os.path.exists("Data/grammars.txt"):
        print("Parsing grammar of data...", end="")
        grammarParser.main()
        print("done.")

        print("Generating new gammars...", end="")
        os.system("TextGen.py 5")
        print("done.")

    if not os.path.exists("Data/grammarDict.pkl"):
        dictBuilder.main()

    M = memeBuilder()


main()
