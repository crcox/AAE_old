import pickle
from sys import stdout
# DEFINITIONS
vowels = ['a','@','&','E','e','I','i','O','o','U','u','^','w']
consonants = ['c','d','F','f','G','g','H','h','J','j','K','k',
			'L','l','M','m','N','n','P','p','Q','q','R','r',
			's','t','V','v','x','z']
th = ['T','D']
fricatives = ['T','D','C','S','Z']
devoicing_rules = {
	'b':'p',
	'd':'t',
	'g':'k',
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
	s=s.replace('ar','&')
	return s

# Load desired dictionary.
with open('3kdict.pkl','rb') as f:
	d=pickle.load(f)

with open('change_log','w') as log:
	logdict = {
			'rule1':{'total':0},
			'rule2':{'total':0},
			'rule3':{'total':0},
			'rule4':{'total':0},
			'rule5':{'total':0}
	}
	for w in d.keys():
		p=d[w]['phon']
		dashes=count_dashes(p)
		p=p.strip('_')
		pp=parse_vowels(p)
		p=list(p)
		rule_applied = [False,False,False,False,False]
		# REPLACEMENTS
		# Rule 1: If the pronunciation ends with a th sound (either T or D, in our
		# scheme) replace with f.
		if p[-1] in th:
			rulecode=p[0]+'-->f'
			log.write(w+": "+''.join(p)+"-->")
			p[-1] = 'f'
			logdict['rule1']['total']+=1
			try:
				logdict['rule1'][rulecode]+=1
			except KeyError:
				logdict['rule1'][rulecode]=1
			log.write(''.join(p)+"\n")
			rule_applied[0] = True

		# Rule 2: If the pronunciation begins with a th sound replace with /d/.
		if p[0] in th:
			rulecode=p[0]+'-->d'
			log.write(w+": "+''.join(p)+"-->")
			p[0] = 'd'
			logdict['rule2']['total']+=1
			try:
				logdict['rule2'][rulecode]+=1
			except KeyError:
				logdict['rule2'][rulecode]=1
			log.write(''.join(p)+"\n")
			rule_applied[1] = True

		# Rule 3: Final phonemes /b/, /d/, /g/, /v/, or /z/ replaced with /p/, /t/,
		# /k/, /f/, and /s/, respectively.
		if p[-1] in devoicing_rules.keys():
			rulecode=p[-1]+'-->'+devoicing_rules[p[-1]]
			log.write(w+": "+''.join(p)+"-->")
			p[-1] = devoicing_rules[p[-1]]
			logdict['rule3']['total']+=1
			try:
				logdict['rule3'][rulecode]+=1
			except KeyError:
				logdict['rule3'][rulecode]=1

			log.write(''.join(p)+"\n")
			rule_applied[2] = True

		# REDUCTIONS
		# Rule 4: If a word ends with a consonant cluster, and the cluster ends
		# with /t/ or /d/, drop the /t/ or /d/
		try:
			if p[-2] in consonants and p[-1] in ['t','d']:
				rulecode=p[-1]+'_drop'
				log.write(w+": "+''.join(p)+"-->")
				p=p[0:-1]
				logdict['rule4']['total']+=1
				try:
					logdict['rule4'][rulecode]+=1
				except KeyError:
					logdict['rule4'][rulecode]=1
				log.write(''.join(p)+"\n")
				rule_applied[3] = True
		except IndexError:
			pass

	#	Rule 5: If the pronunciation ends with a vowel followed by a consonant,
	#	drop the last phoneme.
	#	try:
	#		if pp[-2] in vowels and pp[-1] in ['t','d']:
	#			rulecode=p[-1]+'_drop'
	#			log.write(w+": "+''.join(p)+"-->")
	#			p=p[0:-1]
	#			logdict['rule5']['total']+=1
	#			try:
	#				logdict['rule5'][rulecode]+=1
	#			except KeyError:
	#				logdict['rule5'][rulecode]=1
	#			log.write(''.join(p)+"\n")
	#			rule_applied[4] = True
	#	except IndexError:
	#		pass

		# Compose and record new phonology
		d[w]['AAE_phon']='_'*dashes[0] + ''.join(p) + '_'*dashes[1]
		d[w]['rule_applied']=tuple(rule_applied)

with open('3kdict_with_aae.pkl','wb') as f:
	pickle.dump(d,f)
print 'Wrote binary file 3kdict_with_aae.pkl'

with open('3kdict_change_log.pkl','wb') as f:
	pickle.dump(logdict,f)
print 'Wrote binary file 3kdict_change_log.pkl'

with open('3kdict_with_aae','w') as f:
	for key in d.keys():
		s = ' '.join(
				[
					key,
					d[key]['orth'],
					d[key]['phon'],
					d[key]['AAE_phon'],
					str(d[key]['freq']),
					''.join([str(int(r)) for r in d[key]['rule_applied']])
				]
			)
		f.write(s+'\n')
print 'Wrote text file 3kdict_with_aae'

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
