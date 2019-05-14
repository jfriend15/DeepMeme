''' 
Visualizes Julia's gamma experiment. 
'''

import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import ast


gam = open('gammas_setstart.txt', 'r')
gams = {}
for line in gam.readlines()[2:]:
	
	if len(line) > 1:
		line2 = line.strip().split(':')
		gams[float(line2[0])] = ast.literal_eval(line2[1])

x = range(100)
plt.plot(x, gams[0.1], color='green')
plt.plot(x, gams[0.3], color='blue')
plt.plot(x, gams[0.5], color='purple')
plt.plot(x, gams[0.7], color='red')
plt.plot(x, gams[0.9], color='orange')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.title("Gamma's Affect on Reward")

red = mpatches.Patch(color='green', label='0.1')
blue = mpatches.Patch(color='blue', label='0.3')
green = mpatches.Patch(color='purple', label='0.5')
purple = mpatches.Patch(color='red', label='0.7')
orange = mpatches.Patch(color='orange', label='0.9')

plt.legend(handles=[red, blue, green, purple, orange])

plt.show()

