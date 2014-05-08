import pickle,random
from sys import argv,stdout
import tkFileDialog

import argparse

parser = argparse.ArgumentParser(
	description='Pick a subset of N words, subject to certain conditions.'
)
parser.add_argument('-i',
	metavar='dictionary',
	dest='dictionary',
	type=str, 
	nargs=1,
	default=False,
	help='Path to a pickled python dictionary that contains SAE and AAE phonological codes for each word (output from apply_rules.py).'
)
parser.add_argument('-n', 
	metavar="sample size",
	type=int,
	nargs=1,
	default=500,
	help='The number of words to select for the sample.'
)
parser.add_argument('--n_homo',
	metavar='homophones',
	dest='n_homophones',
	type=int, 
	nargs=1,
	default=20,
	help='Constrain the sample definition, such that there will be at least n SAE homophones in the sample. Note that this will first pick N words that are homophones in the corpus, and then grab all of the words that are homophonic with the selected words, so the number of SAE homophones in the sample will be higher than n. Note also that the AAE homophones are a superset of SAE, so there will be more homophones in AAE than SAE in the sample.'
)
parser.add_argument('--n_same',
	metavar='SAE==AAE',
	dest='n_same',
	type=int, 
	nargs=1,
	default=250,
	help='Contrain the sample definition, such that n words are pronounced identically in SAE and AAE. This constraint can be enforced exactly.'
)
args = parser.parse_args()

print ''
print 'PARAMETERS'
for k,v in vars(args).items():
	print '\t%s: %s' % (str(k), str(v))

print ''
	
if args.dictionary:
	filename = args.dictionary[0]
else:
	filename = tkFileDialog.askopenfilename()

with open(filename,'rb') as f:
	D = pickle.load(f)

words = D.keys()
diff  = [any(D[w]['rule_applied']) for w in words]

words_same = [w for w,d in zip(words,diff) if not d]
words_diff = [w for w,d in zip(words,diff) if d]
words_homo = [w for w in words if D[w]['SAE_homo']]

while True:
	samp = random.sample(words_homo,args.n_homophones)
	skip_list = []
	for w in samp:
		if w in skip_list:
			continue
		skip_list.append(w)
		samp.extend(D[w]['AAE_homo'])
	samp = list(set(samp))
	n_same = sum([1 for w in samp if w in words_same])
	n_diff = len(samp)-n_same

	i = 0
	random.shuffle(words_same)
	for w in words_same:
		if not w in samp:
			samp.append(w)
			i+=1

		if n_same+i == args.n_same:
			break

	i = 0
	random.shuffle(words_diff)
	for w in words_diff:
		if not w in samp:
			samp.append(w)
			i+=1

		if n_diff+i == args.n - args.n_same:
			break

	sae_samp = [D[w]['SAE_phon'] for w in samp]
	aae_samp = [D[w]['AAE_phon'] for w in samp]
	aae_u = len(set(aae_samp))
	sae_u = len(set(sae_samp))
	if (args.n-sae_u) > args.n_homophones:
		break

samp.sort()
fields = ['orth','SAE_phon','AAE_phon','freq']

filename = str(args.n)+'dict_with_aae'
with open(filename,'w') as f:
	for w in samp:
		f.write(' '.join([w]+[str(D[w][k]) for k in fields])+'\n')

print 'Wrote text file %ddict_with_aae.' % args.n

changes_samp = [D[w]['rule_applied'] for w in samp]
print '     Any change: %d' % sum([any(x) for x in changes_samp])
print '      Devoicing: %d' % sum([x[0] for x in changes_samp])
print ' Reduction (cc): %d' % sum([x[1] for x in changes_samp])
print ' Reduction (pv): %d' % sum([x[2] for x in changes_samp])
print ''

n = len(aae_samp)
aae_u = len(set(aae_samp))
sae_u = len(set(sae_samp))
print 'Homophones:'
print ' +---------------+'
print ' |  SAE  |  AAE  |'
print ' | % 4d  | % 4d  |' % (n-sae_u,n-aae_u)
print ' +---------------+'
print ''
