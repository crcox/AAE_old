import pickle
from sys import argv,stdout

with open(argv[1],'rb') as f:
	logdict = pickle.load(f)

print ''
print 'SUMMARY OF CHANGES'
for i in range(4):
	rule='rule%d' % (i+1)
	print 'Rule %d (total:% 4d)' % (i+1,logdict[rule]['total'])
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
