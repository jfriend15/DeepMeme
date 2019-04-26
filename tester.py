import meme

"""
This is just here to test generic words and random scores.
Didn't update _Major_Dic because rescore was the last thing I got working
"""


if __name__=='__main__':
    one = meme.Meme(text=["001","010","100"], score = [-1.0,3.0])
    two = meme.Meme(text=["110","101","011"], score = [1.0,2.0])
    three = meme.Meme(text=["000","111","ass"], score = [3.0,1.0])
    listo = [two,three,one]
    listo.sort(reverse=False)
    print(listo)
    print(one.text,", ",two.text,", ",three.text)
    listo = one.breed(two)
    print("one and two:")
    for mime in listo:
        print(mime.__str__()+":", mime.score)
    #print("one and three:", one.breed(three))
    #print("two and three:", two.breed(three))
