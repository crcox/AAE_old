import pickle,random
from sys import argv,stdout

with open(argv[1],'rb') as f:
	D = pickle.load(f)

aae_phon = []
sae_phon = []
changes  = []
for w,d in D.items():
    aae_phon.append(d['AAE_phon'])
    sae_phon.append(d['phon'])
    changes.append(d['rule_applied'])

X = zip(sae_phon, aae_phon, changes)
s = random.sample(X,500)
sae_samp = [x[0] for x in s]
aae_samp = [x[1] for x in s]
changes_samp = [x[2] for x in s]
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
