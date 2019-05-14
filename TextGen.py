'''
a text generator based on a Markov chain construction
takes 1 parameter: k = number of characters read in per link 
(larger = more accurate output)
'''

import sys
import Markov

# builds a dictionary of strings (length k) : Markov link pairs
def buildDict(inp, dict, k):
    q = [] # an array to hold current substring length k + 1
    c = inp.read(1)
    while c: # while current character read in is not EOF, build dict
        q.append(c)
        if len(q) >= k+1:
            a = q.pop(0)
            for i in range(0, k-1):
                a = a+q[i]
            if a not in dict.keys(): # if current substring not in dictionary, create entry
                mark = markov.Markov(a)
                mark.add(q[k-1])
                dict[a] = mark
            else: # otherwise update entry with suffix
                mark = dict[a]
                mark.add(q[k-1])
        c = inp.read(1)
    return dict

def main():
    if len(sys.argv) != 2: # produces an error if k, file not provided
        print("You need 1 argument!")
        sys.exit()
    k = int(sys.argv[1]) # number of characters per link
    inp = open("./Data/grammars.txt", "r") # read in file
    dict = {}
    try:
        dict = buildDict(inp, dict, k)
    except:
        print("Error reading from file: ./Data/grammars.txt")
    charList = "" # string to keep track of what should be printed/looked at
    inp.seek(1)
    out = open("./Data/genGrammars.txt", "a+")
    for i in range(0, k): # sets up charList at beginning of file
        next = inp.read(1)
        if next != -1:
            charList = charList+str(next)
            out.write(next) # prints first k characters
    inp.close()
    ran = ""
    while ran.find("|") == -1:
        ma = dict[charList]
        ran = ma.random() # chooses random suffix based on frequency in Markov link
        charList = charList+str(ran)
        charList = charList[1:len(charList)]
        out.write(ran) # prints randomly chosen new character
    while ran.find(".") == -1:
        ma = dict[charList]
        ran = ma.random() # chooses random suffix based on frequency in Markov link
        charList = charList+str(ran)
        charList = charList[1:len(charList)]
        if ran.find("|") != -1:
            continue
        out.write(ran) # prints randomly chosen new character
    out.write("\n")
    out.close()

if __name__ == '__main__':
    main()
