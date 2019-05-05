# nltk meme grammar parser for Markov chain
# reads from files toptext.txt and bottomtext.txt
# outputs to grammars.txt, which can be read into the textGen program

import random
import nltk

def main():
    top = open("./Data/toptext.txt", "r")
    texts = []
    for i in top: # reads in the top texts
        i = i[:-1]+" "
        texts.append(i)
    k = 0
    top.close()
    bottom = open("./Data/bottomtext.txt", "r")
    w = open("./Data/grammars.txt", "w+")
    for j in bottom: # reads in the bottom texts, appends to top texts
        texts[k] = texts[k]+j
        texts[k] = nltk.word_tokenize(texts[k]) # separates words in text (tokenizes)
        texts[k] = nltk.pos_tag(texts[k]) # tags parts of speech in text
        for i in texts[k]: # writes tags for each meme grammar in grammars.txt
            w.write(" "+i[1])
        w.write(".\n")
        k += 1
    w.close()
    bottom.close()
    
main()
