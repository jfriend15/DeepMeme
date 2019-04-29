# a text generator based on a Markov chain construction
# takes 3 parameters:
# (1) k = number of characters read in per link (larger = more accurate output),
# (2) M = number of characters output,
# (3) file to read in

import sys
import markov

def main():
    if len(sys.argv) != 4: # produces an error if k, M, file not provided
        print("You need 3 arguments!")
        sys.exit()
    k = int(sys.argv[1]) # number of characters per link
    M = int(sys.argv[2]) # number of characters output
    try:
        inp = open(sys.argv[3], "r") # read in file
    except:
        print("There is no file", sys.argv[3])
        sys.exit()
    dict = {} # a dictionary of strings (length k) : Markov link pairs
    try:
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
    except:
        print("Error reading from file", sys.argv[3])
    charList = "" # string to keep track of what should be printed
    inp.seek(0)
    for i in range(0, k): # sets up charList at beginning of file
        next = inp.read(1)
        if next != -1:
            charList = charList+str(next)
            print(next, end="") # prints first k characters
    index = M - k # index ensures we print out M characters
    while index > 0:
        ma = dict[charList]
        ran = ma.random() # chooses random suffix based on frequency in Markov link
        charList = charList+str(ran)
        charList = charList[1:len(charList)]
        index -= 1
        print(ran, end="") # prints randomly chosen new character
    print()

main()
