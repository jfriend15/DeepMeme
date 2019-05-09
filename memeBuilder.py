import math
import random

ABSORB_STATE = 55257680

GENERICS = ['NNS', 'NN', 'JJ', 'IN', 'VBN', 'CD', 'DT', 'VB', '$', 'RB', '``', 'PRP', 'NNP', 'WP', 'CC', 'PRP$', 'VBD', 'VBZ', 'WRB']

topStates = []
bottomStates = []

"""TODO: Get dictionaries for possible words for each part of speech (these will be our actions)"""

"""Q is a dictionary whose reference is a (state, action) tuple. We will add these as we encounter them"""
Q = {}

def main():

    iterations = 100

    finishedMeme = ((), ())

    alpha = 0.5
    gamma = 0.9

    startState = getStartState()

    tt = ()
    bt = ()

    for i in range(iterations):
        tt = topText(alpha, gamma, startState)

    for i in range(iterations):
        bt = bottomText(alpha, gamma, startState, tt)

    finishedMeme = (tt, bt)

    print(finishedMeme)


main()



def topText(alpha, gamma, startState):

    s = startState

    """This is just to remember which parts of speech are where once they start getting changed"""
    grammar = startState

    while not s == ABSORB_STATE:
        actions = getPossibleActions(s, grammar)

        actionValues = {}

        for action in actions:
            if not Q.__contains__((s, action)):
                Q[(s, action)] = 0

            actionValues[action] = Q[(s, action)]

        chosenAction = softMax(actionValues)

        nextState = getNextState(s, chosenAction)

        if not topStates.__contains__(nextState):
            topStates.__add__(nextState)

        choiceValue = getWordScore(s, chosenAction[0], chosenAction[1], 0)

        r = choiceValue

        value = (1 - alpha) * Q.get(s, chosenAction) + alpha * (r + gamma * maxExpectedNextState(nextState, grammar))

        Q[chosenAction] = value

        s = nextState

    return s

def bottomText(alpha, gamma, startState, topText):
    s = startState

    """This is just to remember which parts of speech are where once they start getting changed"""
    grammar = startState

    while not s == ABSORB_STATE:
        actions = getPossibleActions(s, grammar)

        actionValues = {}

        for action in actions:
            if not Q.__contains__((s, action)):
                Q[(s, action)] = 0

            actionValues[action] = Q[(s, action)]

        chosenAction = softMax(actionValues)

        nextState = getNextState(s, chosenAction)

        if not bottomStates.__contains__(nextState):
            bottomStates.__add__(nextState)

        choiceValue = getWordScore(s, chosenAction[0], chosenAction[1], topText)

        r = choiceValue

        value = (1 - alpha) * Q.get(s, chosenAction) + alpha * (r + gamma * maxExpectedNextState(nextState, grammar))

        Q[chosenAction] = value

        s = nextState

    return s


def getNextState(state, action):

    newState = []

    for word in state:
        newState.append(word)

    newState[action[0]] = action[1]
    return newState

def maxExpectedNextState(state, grammar):
    possibleActions = getPossibleActions(state, grammar)


    bestValue = Q[(state, possibleActions[0])]

    for action in possibleActions:

        v = Q[(state, action)]

        if v > bestValue:
            bestValue = v

    return v


"""Takes a dict with actions and their values, and chooses one based on the softmax function"""
def softMax(actionValues):
    actionProbs = {}

    denom = 0
    for action, value in actionValues.items():
        denom += math.pow(math.e, value)

    for action, value in actionValues.items():
        actionProbs[action] = math.pow(math.e, value)/denom


    rand = random.random()

    total = 0
    for action, prob in actionProbs:
        total += prob
        if rand < total:
            return action

    return 0


"""Takes as parameters the sentence, the index of the word to be replaced, the new word, and top text if it's bottom
text (otherwise topText is 0)"""
def getWordScore(sentence, index, newWord, topText):
    """TODO: give the value of replacing the word at index index with the given word"""
    return 0

def getPossibleActions(sentence, grammar):

    possibleActions = ()

    for i in range(len(sentence)):
        possibleWords = getWordsForPartOfSpeech(grammar[i])
        for word in possibleWords:
            possibleActions.__add__((i, word))

    return possibleActions

def isFinished(sentence):
    for word in sentence:
        if isGeneric(word):
            return 0

    return 1

def getWordsForPartOfSpeech(partOfSpeech):
    """TODO: getDictionary(string) return list of words of given part of speech"""
    return ()


def isGeneric(word):
    if GENERICS.__contains__(word):
        return 1
    return 0

def getStartState():
    """TODO: generate a skeleton from the markov text and return it"""
    return 0
