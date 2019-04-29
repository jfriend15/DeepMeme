# 4/23/19
# A Markov link class for our text generator
# these can be strung together into a chain

import random

class Markov():
    
    def __init__(self, sub):
        self.sub = sub # the substring for this link
        self.count = 0 # the number of suffixes in this link
        self.suffix = {} # a dictionary of char : count/freq pairs

    # adds to the suffix dictionary
    # input c is the suffix character being counted
    def add(self, c):
        self.count += 1
        # if the character is already in suffix, update the dictionary
        if c in self.suffix.keys():
            a = self.suffix[c]
            self.suffix[c] = a + 1
        # otherwise, create a new entry
        else:
            self.suffix[c] = 1

    # chooses a random suffix character based on frequency
    def random(self):
        if self.count == 0:
            print("This Markov has no suffixes.")
        r = random.randrange(self.count) + 1
        for pair in self.suffix.items():
            key = pair[0]
            value = pair[1]
            r = r - value
            if r <= 0:
                return key
        return 1


