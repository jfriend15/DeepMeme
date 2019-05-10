# nltk meme grammar parser for Markov chain
# reads from files toptext.txt and bottomtext.txt
# outputs to grammars.txt, which can be read into the textGen program

import random
import nltk
import string

def main():
    top = open("./Data/toptext.txt", "r")
    punctuation = string.punctuation.replace("'", "")
    topTexts = []
    bottomTexts = []
    for i in top: # reads in the top texts
        i = i[:-1]+" "
        i = i.lower()
        i = i.translate(str.maketrans('', '', punctuation))
        i = nltk.word_tokenize(i) # separates words in text (tokenizes)
        i = nltk.pos_tag(i) # tags parts of speech in text
        topTexts.append(i)
    k = 0
    top.close()
    bottom = open("./Data/bottomtext.txt", "r")
    w = open("./Data/grammars.txt", "w+")
    for j in bottom: # reads in the bottom texts, appends to top texts
        j = j.lower()
        j = j.translate(str.maketrans('', '', punctuation))
        j = nltk.word_tokenize(j)
        j = nltk.pos_tag(j)
        bottomTexts.append(j)
        for i in topTexts[k]: # writes tags for each meme grammar in grammars.txt
            w.write(" "+i[1])
        w.write(" |")
        for i in bottomTexts[k]:
            w.write(" "+i[1])
        w.write(".\n")
        k += 1
    w.close()
    bottom.close()

if __name__ == '__main__':
    main()
