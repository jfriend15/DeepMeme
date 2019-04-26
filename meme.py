"""
This is the Meme class, which will hold the top text of the meme.
The current plan is to generate the top text from nothing and the bottom text by translating from the top text.
currently it is attempting to take certain memes (just sentences) and attempting to transform them into new text.
I was coding this with no grammar checker or ratings, so its scope is rather limited.
The Translation function is currently unbuilt.  I could only work on one at a time.
"""


import random
import math
import sys
from collections import namedtuple


class Meme():
    #These are for comparitors and printing, to make things easier
    #For checking equal text check equals bellow
    __lt__=lambda self,other: self.score[1] < other.score[1] if self.score[0] == other.score[0] else self.score[0] < other.score[0]
    __le__=lambda self,other: self.score.humor <= other.score.humor
    __gt__=lambda self,other: not __lt__(self,other)
    __ge__=lambda self,other: not __le__(self,other)
    __eq__=lambda self,other: self.score[0] == other.score[0] and self.score[1] == other.score[1]
    __ne__=lambda self,other: not __eq__(self,other)
    __repr__=lambda self: ' '.join(self.text).lstrip()
    __str__=lambda self: self.__repr__()

    #This is the toplevel class that all memes will be subclasses of
    #This is the top level dictionary (that's why the _ is there)
    #Each decendent will have a Major_Dic of its own
    #They are to be utilized for later on
    _MAJOR_DIC={}

    #Just the init function
    #it can be blank incase we want to construct from scratch
    def __init__(self, text = [], score = [0.0,0.0]):
        self.text = text
        self.score = score

    #deep equals that checks for equal score and the same text
    def equals(self, other):
        return len(self.text)==len(self.text) and self==other and all(self.text[i]==other.text[i] for i in range(len(self.text)))

    #update's the score of the calling meme.
    #returns self incase we need it for something (we do bellow)
    #words that aren't known in _MAJOR_DIC are set to epsilon, but that's a number to be tweaked
    #for the subclasses they will do: self.MAJOR_DIC.get(self.text[x],self._MAJOR_DIC.get(self.text[x],sys.float_info.epsilon)) to update the score of words.  This is a mostly global scoring.
    def update_score(self):
        self.score[0] = math.fsum(map(lambda x: self._MAJOR_DIC.get(self.text[x], sys.float_info.epsilon), range(len(self.text))))
        self.score[1] = math.fsum(map(lambda x: self._MAJOR_DIC.get(self.text[x], -sys.float_info.epsilon), range(len(self.text))))
        return self

    #This is a very basic breeding function
    #returns a sorted list of 4 new random children that are scored.
    def breed(self, partner):
        genome = str(self.__str__()+" "+ partner.__str__()).split(' ')
        length1 = len(genome)//2
        length2 = len(genome) - length1
        return sorted(map(lambda x: x.update_score(), (Meme(text=random.sample(genome,length1)), Meme(text=random.sample(genome,length2)), Meme(text=random.choices(genome,k=length1)), Meme(text=random.choices(genome,k=length2)))),reverse=True)

    #kills a meme permanently.
    #useful for removing the old populace (we'll need this a lot)
    def kill(self):
        del self
        return True

#Useful for testing purposes
#building the top level dictionary will be necessary for the main function
#execing mem.py will let us populate _Major_Dic, which will be inheritted by all the other memes
#I didn't finish building it because I haven't gotten a chance to work on this since getting scores
#The contents of the dictionary will need to be determined later.
if __name__=='__main__':
    _MAJOR_DIC.clear()
    file = open(sys.argv[1], "r")
    for line in file:
        data = line.split(",")
        Meme._MAJOR_DIC[data[0]] = Score(data[1], data[2])
