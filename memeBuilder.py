'''
Where the magic happens and the memes are built.
Calls GrammarParser, TextGen, and DictBuilder as necessary.
Builds meme with Q-Learning.
'''


import math
import random
import pickle
import os
import numpy as np

import DictBuilder
import GrammarParser


class memeBuilder:
    GENERICS = ['NNS', 'NN', 'JJ', 'IN', 'VBN', 'CD', 'DT', 'VB',
                '$', 'RB', '``', 'PRP', 'NNP', 'WP', 'CC', 'PRP$',
                'VBD', 'VBZ', 'WRB']

    FINISH_SENTENCE = (-1, "")

    ABSORB_STATE = 986700870805

    SENTENCE_BASE_reward = 100

    def __init__(self, iterations, alpha, gamma, randomStart=True):

        self.topStates = []
        self.bottomStates = []

        """Q is a dictionary whose reference is a (state, action) tuple. 
        We will add these as we encounter them"""
        self.Q = {}

        # Retrieve generated grammar in string
        startState = self.getStartState(randomStart).strip(".")
        splitText = self.splitText(startState)
        print("Start state: ", startState)

        self.glove = self.load_dict('Data/gloveDict.pkl')
        self.POSDict = self.load_dict('Data/grammarDict.pkl')

        # Store information
        self.rewardRecord = []   

        for i in range(iterations):
            tt = self.topText(alpha, gamma, splitText[0]) 
            print('Iteration', i, ': ', tt)
        
        for i in range(iterations):
            bt, btReward = self.bottomText(alpha, gamma, splitText[1], tt)
            print('Iteration', i, ': ', bt)
            # Record reward of of finished state on that iteration
            self.rewardRecord.append(btReward) 

        finishedMeme = (tt, bt)
        print(finishedMeme)


    """Helper function"""
    def load_dict(self, file):
        dict_file = open(file, "rb")
        return pickle.load(dict_file)

    """Retrives a generated grammar skeleton. Returns a string."""
    def getStartState(self, randomStart=True):
        grammarData = open('Data/genGrammars.txt', 'r')
        grammars = [line.strip() for line in grammarData.readlines()]
        
        if randomStart:
            # Ensure that the grammar has top and bottom text
            g =''
            while '|' not in g or 'RP' in g: # Take out commas for now
                g = grammars[random.randint(0, len(grammars)-1)]
            
            g = g.replace(',', '').replace("''", '').replace("  ", " ")
            return g
        else:
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

        finishedCount = 0
        while True:

            if self.isFinished(s):
                finishedCount += 1
                if not actions.__contains__(memeBuilder.FINISH_SENTENCE):
                    actions.append(memeBuilder.FINISH_SENTENCE)

            for action in actions:
                if (s, action) not in self.Q.keys():
                    self.Q[(s, action)] = 0

                actionValues[action] = self.Q[(s, action)]

            if finishedCount == 50:
                chosenAction = memeBuilder.FINISH_SENTENCE
            else:
                chosenAction = self.softMax(actionValues)
            #print('Chosen action is ', chosenAction)

            nextState = self.getNextState(s, chosenAction)
            #print('Next state is ', nextState)

            if nextState == memeBuilder.ABSORB_STATE:
                break

            if not self.topStates.__contains__(nextState):
                self.topStates.append(nextState)

            choiceValue = self.getWordReward(s, chosenAction[0], chosenAction[1], 0)

            r = choiceValue

            value = (1 - alpha) * self.Q.get((s, chosenAction)) + alpha * (
                        r + gamma * self.maxExpectedNextState(nextState, grammar, actions))

            #print('Overall value is', value)
            self.Q[chosenAction] = value

            s = nextState

        return s

    def bottomText(self, alpha, gamma, startState, topText):
        # s will change, grammar will not
        s = startState
        grammar = startState

        actions = self.getPossibleActions(s, grammar)
        actionValues = {}

        finishedCount = 0
        while True:

            if self.isFinished(s):
                if not actions.__contains__(self.FINISH_SENTENCE):
                    actions.append(self.FINISH_SENTENCE)

            for action in actions:
                if (s, action) not in self.Q.keys():
                    self.Q[(s, action)] = 0

                actionValues[action] = self.Q[(s, action)]

            # If it does not choose to finish, finish it manually
            if finishedCount == 50:
                chosenAction = memeBuilder.FINISH_SENTENCE
            else:
                chosenAction = self.softMax(actionValues)

            nextState = self.getNextState(s, chosenAction)

            if nextState == memeBuilder.ABSORB_STATE:
                break

            if not self.bottomStates.__contains__(nextState):
                self.bottomStates.append(nextState)

            choiceValue = self.getWordReward(s, chosenAction[0], chosenAction[1], topText)

            r = choiceValue

            value = (1 - alpha) * self.Q.get((s, chosenAction)) + alpha * (
                    r + gamma * self.maxExpectedNextState(nextState, grammar, actions))

            self.Q[chosenAction] = value

            s = nextState

        return s, self.sentenceReward(s)

    def getNextState(self, state, action):
        if action == memeBuilder.FINISH_SENTENCE:
            return memeBuilder.ABSORB_STATE

        newState = []
        for word in state.split(' '):
            newState.append(word)

        newState[action[0]] = action[1]
        return ' '.join(newState)

    def maxExpectedNextState(self, state, grammar, possibleActions):

        if state == self.ABSORB_STATE:
            return 0

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

    """Takes a dict with actions and their values, and chooses one 
    based on the softmax function"""
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
    
    '''Returns average Euclidean distance of the new word
    from the old words from embeddings in GLOVE.'''
    def reward(self, context, word):
        avg_dist = []
        if word not in self.glove.keys():
            return 50

        new_embd = self.glove[word]
        for old_word in context:
            # If either word isn't in glove or the old word is generic,
            # give it a far distance to motivate not picking it
            if self.isGeneric(old_word) or old_word not in self.glove.keys():
                dist = 50
            else:
                embd = self.glove[old_word]
                dist = np.linalg.norm(embd - new_embd)

            avg_dist.append(dist)

        return sum(avg_dist) / len(avg_dist)

    def sentenceReward(self, s):
        discount = 0

        for word in s:
            value = self.reward(s, word)
            discount += value

        discount /= len(s)
        return self.SENTENCE_BASE_reward/discount

    """Takes as parameters the sentence, the index of the word to be replaced, the new word, and top text if it's bottom
    text (otherwise topText is 0)"""
    def getWordReward(self, sentence, index, newWord, topText):
        if index == -1:
            sentence = sentence.split(' ')
            return self.sentenceReward(sentence)

        sentence = sentence.split(' ')
        oldWord = sentence[index]
        del sentence[index]

        if topText != 0:
            sentence.extend(topText.split(' '))

        oldreward = self.reward(sentence, oldWord)
        newreward = self.reward(sentence, newWord)

        return newreward - oldreward

    def getPossibleActions(self, sentence, grammar):
        possibleActions = []
        sentence = sentence.split(' ')
        grammar = grammar.split(' ')
        for i in range(len(sentence)):
            possibleWords = self.getWordsForPartOfSpeech(grammar[i])
            for word in possibleWords:
                possibleActions.append((i, ''.join(word)))

        return possibleActions

    def isFinished(self, sentence):
        for word in sentence:
            if self.isGeneric(word):
                return 0

        return 1

    """Returns list of tokenized words from dataset given a POS"""
    def getWordsForPartOfSpeech(self, partOfSpeech):
        if partOfSpeech in self.POSDict.keys():
            return self.POSDict[partOfSpeech]
        else:
            print(partOfSpeech, "not found in Part of Speech dictionary. Aborting.")
            exit()

    def isGeneric(self, word):
        if self.GENERICS.__contains__(word):
            return 1
        return 0

''' EXPERIMENTS ON HYPERPARAMS '''
def iterationExperiment(eName, itRange, alpha, gamma):
    output = open('Results/'+eName+'.txt', 'w+')
    output.write('Iteration range='+str(itRange)+',Alpha='+str(alpha)+',Gamma='+str(gamma)+'\n')
    for its in itRange:
        M = memeBuilder(its, alpha, gamma, randomStart=False)
        output.write(str(its)+':'+str(M.rewardRecord)+'\n')
    output.close()


def alphaExperiment(eName, its, alRange, gamma):
    output = open('Results/'+eName+'.txt', 'w+')
    output.write('Iterations='+str(its)+',Alpha range='+str(alRange)+',Gamma='+str(gamma)+'\n')
    for alpha in alRange:
        M = memeBuilder(its, alpha, gamma, randomStart=False)
        output.write(str(alpha)+':'+str(M.rewardRecord)+'\n')
    output.close()

def gammaExperiment(eName, its, alpha, gamRange):
    output = open('Results/'+eName+'.txt', 'w+')
    output.write('Iterations='+str(its)+',Alpha='+str(alpha)+',Gamma range='+str(gamRange)+'\n')
    for gamma in gamRange:
        M = memeBuilder(its, alpha, gamma, randomStart=False)
        output.write(str(gamma)+':'+str(M.rewardRecord)+'\n')
    output.close()


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

    # Input the range you want to test
    iterationExperiment('itertations_setstart', [50, 100, 200, 500], 0.5, 0.9)
    alphaExperiment('alphas_setstart', 10, [0.1,0.3,0.5,0.7,0.9], 0.9)
    gammaExperiment('gammas_setstart', 100, 0.5, [0.1,0.3,0.5,0.7,0.9])

main()
