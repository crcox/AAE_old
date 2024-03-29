import pickle
from sys import argv,stdout
import tkFileDialog

try:
	filename = argv[1]
except IndexError:
	filename = tkFileDialog.askopenfilename()

with open(filename,'rb') as f:
	logdict = pickle.load(f)

print ''
print 'SUMMARY OF CHANGES'
rules=['devoice','reduction_cc','reduction_pv']
for i in range(3):
	rule=rules[i]
	print '%s (total:% 4d)' % (rule,logdict[rule]['total'])
	stdout.write(' +'+'-'*41+'+\n')
	stdout.write(' |')
	j=-1
	for k in logdict[rule].keys():
		if k=='total':
			continue
		j+=1
		stdout.write('% 7s:% 4d' % (k,logdict[rule][k]))
		if (j%3) == 2:
			stdout.write(' |\n')
			stdout.write(' |')
		else:
			stdout.write(' |')

	stdout.write('\n')
	stdout.write(' +'+'-'*41+'+\n\n')
