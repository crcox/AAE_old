import pickle,random
from sys import argv,stdout
import tkFileDialog

try:
	filename = argv[1]
except IndexError:
	filename = tkFileDialog.askopenfilename()

with open(filename,'rb') as f:
	D = pickle.load(f)

words = D.keys()
diff  = [any(D[w]['rule_applied']) for w in words]

words_same = [w for w,d in zip(words,diff) if not d]
words_diff = [w for w,d in zip(words,diff) if d]
words_homo = [w for w in words if D[w]['SAE_homo']]

while True:
	samp500 = random.sample(words_homo,20)
	skip_list = []
	for w in samp500:
		if w in skip_list:
			continue
		skip_list.append(w)
		samp500.extend(D[w]['AAE_homo'])
	samp500 = list(set(samp500))
	n_same = sum([1 for w in samp500 if w in words_same])
	n_diff = len(samp500)-n_same

	i = 0
	random.shuffle(words_same)
	for w in words_same:
		if not w in samp500:
			samp500.append(w)
			i+=1

		if n_same+i == 250:
			break

	i = 0
	random.shuffle(words_diff)
	for w in words_diff:
		if not w in samp500:
			samp500.append(w)
			i+=1

		if n_diff+i == 250:
			break

	sae_samp500 = [D[w]['SAE_phon'] for w in samp500]
	aae_samp500 = [D[w]['AAE_phon'] for w in samp500]
	aae_u = len(set(aae_samp500))
	sae_u = len(set(sae_samp500))
	if (500-sae_u) > 20: #and (500-aae_u) > 40:
		break

samp500.sort()
fields = ['orth','SAE_phon','AAE_phon','freq']
with open('500dict_with_aae','w') as f:
	for w in samp500:
		f.write(' '.join([w]+[str(D[w][k]) for k in fields])+'\n')

print 'Wrote text file 500dict_with_aae.'

changes_samp500 = [D[w]['rule_applied'] for w in samp500]
print '     Any change: %d' % sum([any(x) for x in changes_samp500])
print '      Devoicing: %d' % sum([x[0] for x in changes_samp500])
print ' Reduction (cc): %d' % sum([x[1] for x in changes_samp500])
print ' Reduction (pv): %d' % sum([x[2] for x in changes_samp500])
print ''

n = len(aae_samp500)
aae_u = len(set(aae_samp500))
sae_u = len(set(sae_samp500))
print 'Homophones:'
print ' +---------------+'
print ' |  SAE  |  AAE  |'
print ' | % 4d  | % 4d  |' % (n-sae_u,n-aae_u)
print ' +---------------+'
print ''
