Requires the GloVe word vectors pretrained on Twitter; can be found [here](https://github.com/stanfordnlp/GloVe).


grammarParser.py:

    Requirements: NLTK, download nltk_data at https://www.nltk.org/data.html
    Input: None
    Output: outputs all tagged data from toptext.txt and bottomtext.txt to grammars.txt in Data directory

textGen.py:

    Requirements: None
    Input: k (the default input I have been using is k = 5)
    Output: outputs all generated grammars to ./Data/genGrammars.txt
