# nltk meme grammar parser for Markov chain
# reads from files toptext.txt and bottomtext.txt
# outputs to grammars.txt, which can be read into the textGen program

import random
import nltk

def main():
    top = open("toptext.txt", "r")
    bottom = open("bottomtext.txt", "r")
    texts = []
    for i in top:
        i = i[:-1]+" "
        texts.append(i)
    k = 0
    top.close()
    w = open("grammars.txt", "w+")
    for j in bottom:
        texts[k] = texts[k]+j
        texts[k] = nltk.word_tokenize(texts[k])
        texts[k] = nltk.pos_tag(texts[k])
        for i in texts[k]:
            w.write(" "+i[1])
        w.write(".\n")
        k += 1
    w.close()
    bottom.close()
    
main()
