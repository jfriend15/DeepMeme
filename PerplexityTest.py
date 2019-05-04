from Perplexity import *
import pandas as pd 
import matplotlib.pyplot as plt 

#text = "STUDIES MATERIALS SCIENCE / DOESN'T CRACK UNDER PRESSURE"
	#text2 = "I DO STUDY MATERIALS SCIENCE, AND I DO NOT CRACK UNDER PRESSURE"
	#print(perplexity(text))
	#print(perplexity(text2))

data = pd.read_csv('SuccessKidData.csv')
P = Perplexity()

texts = []
comps = []
humors = []
perplexs = []
for i in range(len(data['Top Text'])):
	top = data['Top Text'][i]
	bot = data['Bottom Text'][i]
	#texts[top + ' ' + bot] = (data['comp avg'][i], data['humor avg'][i])\
	caption = top + ' ' + bot

	texts.append(caption)
	comps.append(data['comp avg'][i])
	humors.append(data['humor avg'][i])
	perplexs.append(P.perplexity(caption))


sorted_all = sorted(zip(texts,comps,humors,perplexs), key=lambda text: text[1])
#print(sorted_all)
stexts, scomps, shumors, sperplexs = zip(*sorted_all)

#print(texts)
x = range(len(data['Top Text']))

f, (ax1, ax2) = plt.subplots(1,2,sharey=True)
#plt.xlabel('# of clusters')
#plt.gcf().text(0.1,0.05, 'Optimal K (GSM): ' + str(optK[0]), fontsize=14)
#plt.gcf().text(0.6,0.05, 'Optimal K (MaxGap): ' + str(optK[1]), fontsize=14)

ax1.scatter(scomps, sperplexs, color='r')
ax1.title.set_text('Our comp. score vs. Perplexity')
ax1.set(xlabel='Comp',ylabel='Perp')

ax2.scatter(shumors, sperplexs, color='b')
ax2.title.set_text('Our humor score vs. Perplexity')
ax2.set(xlabel='Humor',ylabel='Perp')

t = f.suptitle('Perplexity evaluation', fontsize=14)
f.tight_layout()

t.set_y(0.95)
f.subplots_adjust(top=0.8, wspace=0.4, bottom=0.2)

#plt.savefig('Gaps/v3/GSM_' + dataset + '_v2.png')
plt.show()

	# for all top text + bottom text combos,
	# plot perplexity, our rated comprehens, and our rated humor