import math
import random

ABSORB_STATE = 55257680


"""TODO: Create S as two ordered lists of strings (top and bottom text)"""

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
        bt = bottomText(alpha, gamma, startState, tt)

    finishedMeme = (tt, bt)

    print(finishedMeme)


main()



def topText(alpha, gamma, startState):

    s = startState

    """This is just to remember which parts of speech are where once they start getting changed"""
    grammar = startState

    while not s == ABSORB_STATE:
        actions = getPossibleActions(s)

        actionValues = {}

        for action in actions:
            if not Q.__contains__((s, action)):
                Q[(s, action)] = 0

            actionValues[action] = Q[(s, action)]

        chosenAction = softMax(actionValues)

        nextState = getNextState(s, chosenAction)

        choiceValue = getWordScore(s, chosenAction[0], chosenAction[1], 0)

        r = choiceValue

        value = (1 - alpha) * Q.get(s, chosenAction) + alpha * (r + gamma * maxExpectedNextState(nextState))

        Q[chosenAction] = value

        s = nextState

    return s

def bottomText(alpha, gamma, startState, topText):
    s = startState

    """This is just to remember which parts of speech are where once they start getting changed"""
    grammar = startState

    while not s == ABSORB_STATE:
        actions = getPossibleActions(s)

        actionValues = {}

        for action in actions:
            if not Q.__contains__((s, action)):
                Q[(s, action)] = 0

            actionValues[action] = Q[(s, action)]

        chosenAction = softMax(actionValues)

        nextState = getNextState(s, chosenAction)

        choiceValue = getWordScore(s, chosenAction[0], chosenAction[1], topText)

        r = choiceValue

        value = (1 - alpha) * Q.get(s, chosenAction) + alpha * (r + gamma * maxExpectedNextState(nextState))

        Q[chosenAction] = value

        s = nextState

    return s


def getNextState(state, action):
    """TODO: return the resulting state of the chosen action"""
    return []

def maxExpectedNextState(state):
    """TODO: find the highest value action for the next state"""
    return 0

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

def getPossibleActions(sentence):
    """TODO: Return all possible actions as a list of tuples {index, word} where index is the index of the word you"""
    return ()

def isFinished(sentence):
    """"TODO: check if a sentence has unresolved parts of speech. Return 1 if no, 0 if yes"""
    return 0

def getDictionary(partOfSpeech):
    """TODO: getDictionary(string) return dictionary of given part of speech"""
    return {}


def isGeneric(word):
    """TODO: return 1 if the word is a part of speech, 0 if it's literal"""
    return 0

def getStartState():
    """TODO: generate a skeleton from the markov text and return it"""
    return 0
