'''
Evaluating correlation between perplexity score and our comprehensibility
and humor scores.
'''

from Perplexity import *
import pandas as pd 
import matplotlib.pyplot as plt 

data = pd.read_csv('Data/SuccessKidData.csv')
P = Perplexity()

texts = []
comps = []
humors = []
perplexs = []
for i in range(len(data['Top Text'])):
	top = data['Top Text'][i]
	bot = data['Bottom Text'][i]
	caption = top + ' ' + bot

	texts.append(caption)
	comps.append(data['comp avg'][i])
	humors.append(data['humor avg'][i])
	perplexs.append(P.perplexity(caption))

# Graph 
f, (ax1, ax2) = plt.subplots(1,2,sharey=True)

# Comp. vs. Perplexity
ax1.scatter(comps, perplexs, color='r')
ax1.title.set_text('Our comp. score vs. Perplexity')
ax1.set(xlabel='Comp',ylabel='Perp')

# Humor vs. Perplexity
ax2.scatter(humors, perplexs, color='b')
ax2.title.set_text('Our humor score vs. Perplexity')
ax2.set(xlabel='Humor',ylabel='Perp')

t = f.suptitle('Perplexity evaluation', fontsize=14)
f.tight_layout()

t.set_y(0.95)
f.subplots_adjust(top=0.8, wspace=0.4, bottom=0.2)

plt.show()