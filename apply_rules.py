import pickle
from sys import stdout
# DEFINITIONS
vowels = ['A','a','@','&','c','E','e','I','i','O','o','U','u','^','W','w','Y']
consonants = ['d','F','f','G','g','H','h','J','j','K','k',
			'L','l','M','m','N','n','P','p','Q','q','R','r',
			's','t','V','v','x','z']
th = ['T','D']
fricatives = ['T','D','C','S','Z']
devoicing_rules = {
	'b':'p',
	'd':'t',
#	'g':'k',
	'v':'f',
	'z':'s'
	}

def count_dashes(s):
# Orth and Phon patterns are _ padded. They need to be tracked before they are
# stripped so they can be re-added to the modified solution.
	ind=0
	dashes=[0,0]
	for c in s:
		if c=='_':
			dashes[ind]+=1
		else:
			ind=1 # so the next dash encountered will increment the second
				  # counter.
	return tuple(dashes)

def parse_vowels(s):
# Some values are represented by multiple characters. For ease of processing,
# these will be reduced to arbitrary 1-character codes:
# ar --> &
#	s=s.replace('ar','&')
	return s

# Load desired dictionary.
with open('3kdict.pkl','rb') as f:
	D=pickle.load(f)

print ''
print 'Applying rules...'
with open('change_log','w') as log:
	logdict = {
			'devoice':{'total':0},
			'reduction_cc':{'total':0},
			'reduction_pv':{'total':0}
	        }
	for w in D.keys():
		p=D[w]['SAE_phon']
		dashes=count_dashes(p)
		p=p.strip('_')
		pp=parse_vowels(p)
		p=list(p)
		rule_applied = [False,False,False]
		# DEVOICING
		# Rule 1: Final phonemes /b/, /d/, /v/, or /z/ replaced with /p/, /t/,
		# /f/, and /s/, respectively.
		try:
			if pp[-2] in vowels and p[-1] in devoicing_rules.keys():
				rulecode=p[-1]+'-->'+devoicing_rules[p[-1]]
				log.write(w+": "+''.join(p)+"-->")
				p[-1] = devoicing_rules[p[-1]]
				logdict['devoice']['total']+=1
				try:
					logdict['devoice'][rulecode]+=1
				except KeyError:
					logdict['devoice'][rulecode]=1

				log.write(''.join(p)+"\n")
				rule_applied[0] = True
		except IndexError:
			pass

		# Consonant Cluster Reduction
		# Rule 2: If a word ends with a consonant cluster, and the cluster ends
		# with /t/ /d/ /s/ or /z/, drop it.
		try:
			if pp[-2] in consonants and p[-1] in ['t','d','s','z']:
				rulecode=p[-1]+'_drop'
				log.write(w+": "+''.join(p)+"-->")
				p[-1]='_'
				logdict['reduction_cc']['total']+=1
				try:
					logdict['reduction_cc'][rulecode]+=1
				except KeyError:
					logdict['reduction_cc'][rulecode]=1
				log.write(''.join(p)+"\n")
				rule_applied[1] = True
		except IndexError:
			pass

		# Post-vocalic Reduction
		# Rule 3: If a word ends with a vowel followed by an /r/, drop the /r/.
		try:
			if pp[-2] in vowels and p[-1] == 'r':
				rulecode=p[-1]+'_drop'
				log.write(w+": "+''.join(p)+"-->")
				p[-1]='_'
				logdict['reduction_pv']['total']+=1
				try:
					logdict['reduction_pv'][rulecode]+=1
				except KeyError:
					logdict['reduction_pv'][rulecode]=1
				log.write(''.join(p)+"\n")
				rule_applied[2] = True
		except IndexError:
			pass

		# Compose and record new phonology
		D[w]['AAE_phon']='_'*dashes[0] + ''.join(p) + '_'*dashes[1]
		D[w]['rule_applied']=tuple(rule_applied)


print ''
print 'Identifying homophones...'

words = []
aae_phon = []
sae_phon = []
for w,d in D.items():
	words.append(w)
	aae_phon.append(d['AAE_phon'])
	sae_phon.append(d['SAE_phon'])

for (W,A,S) in zip(words,aae_phon,sae_phon):
	sh = [w for (w,s) in zip(words,sae_phon) if s==S and not w==W]
	ah = [w for (w,a) in zip(words,aae_phon) if a==A and not w==W]
	D[W]['SAE_homo'] = sh
	D[W]['AAE_homo'] = ah
#	if len(sh) > 0:
#		print W
#		print sh
#		print ah

print 'DONE.'

with open('3kdict_with_aae.pkl','wb') as f:
	pickle.dump(D,f)
print 'Wrote binary file 3kdict_with_aae.pkl'

with open('3kdict_change_log.pkl','wb') as f:
	pickle.dump(logdict,f)
print 'Wrote binary file 3kdict_change_log.pkl'

with open('3kdict_with_aae','w') as f:
	for key in D.keys():
		s = ' '.join(
				[
					key,
					D[key]['orth'],
					D[key]['SAE_phon'],
					D[key]['AAE_phon'],
					str(D[key]['freq']),
					''.join([str(int(r)) for r in D[key]['rule_applied']])
				]
			)
		f.write(s+'\n')
print 'Wrote text file 3kdict_with_aae'

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
