import pickle,random
from sys import argv,stdout
import tkFileDialog

filename = tkFileDialog.askopenfilename()
with open(filename,'rb') as f:
	D = pickle.load(f)

aae_phon = []
sae_phon = []
changes  = []
for w,d in D.items():
	aae_phon.append(d['AAE_phon'])
	sae_phon.append(d['phon'])
	changes.append(d['rule_applied'])

n = len(aae_phon)
aae_u = len(set(aae_phon))
sae_u = len(set(sae_phon))
print 'Homophones:'
print ' +---------------+'
print ' |  SAE  |  AAE  |'
print ' | % 4d  | % 4d  |' % (n-sae_u,n-aae_u)
print ' +---------------+'
