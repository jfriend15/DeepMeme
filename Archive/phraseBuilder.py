import collections

NOUN = '[NOUN]'
PRO = '[PRONOUN]'
VERB = '[VERB]'
AUX = '[AUXILIARY]'
DET = '[DETERMINER]'
ADJ = '[ADJECTIVE]'
ADV = '[ADVERB]'
PREP = '[PREPOSITION]'
CONJ = '[CONJUGATION]'
INTJ = '[INTERJECTION]'

partsOfSpeech = (NOUN, PRO, VERB, AUX, DET, ADJ, ADV, PREP, CONJ, INTJ)

class PhraseBuilder:

    phrase = []

    phrasePointer = 0

    """Resolve an abstract word like [NOUN] to a specific word"""
    def resolve(self, s):

        if not partsOfSpeech.__contains__(s):
            print('This value is already resolved to a literal string!')
            return 0

        self.phrase[self.phrasePointer] = s
        return 1

    """Add a new value (either abstract or literal) at the pointer, pushing all other values to the right."""
    def insert(self, s):
        newPhrase = []

        """If the pointer is not in the list, use the append function instead and correct the pointer"""
        if self.phrasePointer >= len(self.phrase):
            print('The pointer was not on the list. Appending value to end and resetting pointer')
            self.phrasePointer = len(self.phrase)
            return self.append(s)

        for i in range(self.phrasePointer):
            newPhrase.append(self.phrase[i])

        newPhrase.append(s)

        for i in range(len(self.phrase) - self.phrasePointer):
            newPhrase.append(self.phrase[self.phrasePointer + i])

    """move the pointer one space to the right, if it can do so"""
    def pointerRight(self):
        if self.phrasePointer >= len(self.phrase)-1:
            print('The pointer cannot go further right')
            self.phrasePointer = len(self.phrase)-1
            return 0

        self.phrasePointer += 1
        return 1

    """move the pointer one space to the left, if it can do so"""
    def pointerLeft(self):
        if self.phrasePointer <= 0:
            print('The pointer cannot go any further left')
            self.phrasePointer = 0
            return 1

        self.phrasePointer -= 1
        return 1

    """Sets pointer to a new place in the phrase. If this is out of bounds returns false and does nothing"""
    def setPointer(self, i):
        if i < 0 or i >= len(self.phrase):
            print('That index is out of bounds')
            return 0

        self.phrasePointer = i
        return 1

    """Sets the pointer to the next unresolved word after the current pointer location. If there are none, returns false and does nothing"""
    def nextUnresolved(self):
        for i in range(len(self.phrase) - self.phrasePointer):
            if partsOfSpeech.__contains__(self.phrase[i]):
                self.phrasePointer = i
                return self.phrase[i]

        print('There are no unresolved words after this point')
        return 1

    """Sets pointer back to 0, the starting location of the phrase"""
    def resetPointer(self):
        self.phrasePointer = 0
        return 1

    """Sets pointer to the last position in the phrase"""
    def advanceFully(self):
        self.phrasePointer = len(self.phrase)-1
        return 1

    """Appends a value to the end of the phrase, and moves the pointer to it"""
    def append(self, s):
        self.phrase.append(s)
        self.advanceFully()
        return 1

    """Inserts a word at the given index if possible, and sets the pointer to that location"""
    def insertAt(self, word, index):

        possible = self.setPointer(index)

        if not possible:
            return 1

        self.insert(word)
        return 1

    """Creates a string out of the phrase so we can print it and make sure everything is working right. The pointer is indicated by surrounding the word or token with
    angle brackets, ie <Hello> ir <[DETERMINER]>"""
    def toString(self):
        phraseString = ""

        for i in range(len(self.phrase)-1):

            if i == self.phrasePointer:
                phraseString = phraseString + '<'

            phraseString = phraseString + self.phrase[i]

            if i == self.phrasePointer:
                phraseString = phraseString + '>'

            phraseString = phraseString + ' '

        return phraseString

    def printPhrase(self):
        print(self.toString())
        return 1
