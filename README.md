This program generates captions for the Success Kid meme format using Markov Chains and Reinforcement learning. Implementation details follow:

Requires the GloVe word vectors pretrained on Twitter; glove.twitter.27B.25d.txt can be found [here](https://github.com/stanfordnlp/GloVe).

grammarParser.py:

    Requirements: NLTK, download nltk_data at https://www.nltk.org/data.html
    Input: None
    Output: outputs all tagged data from toptext.txt and bottomtext.txt to grammars.txt in Data directory

dictBuilder.py

    Requirements: NLTK, pickle, numpy, string
    Input: toptext.txt, bottomtext.txt, glove.twitter.27B.25d.txt
    Output: grammarDict.pkl, gloveDict.pkl

markov.py

    Reqiurements: random

textGen.py:

    Requirements: sys, markov
    Input: k (the default input I have been using is k = 5)
    Output: outputs all generated grammars to ./Data/genGrammars.txt

memeBuilder.py

    Requirements: math, random, pickle, os, numpy, dictBuilder, grammarParser
    Input: iterations, alpha, and gamma for Q-learning
    Output: printed generated meme, record of rewards

We adhered to the Honor Code in this assignment.
Sam Chapin, Julia Friend, Marshall Lynn, Vic Olson
