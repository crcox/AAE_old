import argparse, pickle, sys
import phoncodes, utils

parser = argparse.ArgumentParser(
		description='Generate AAE phonology by applying a set of rules.',
		epilog='The current set of rules were agreed upon by CRC, CL, MSS and MCM. See archived email, subject:"phon. decisions for AAE model", date: April 29, 2014.'
)
parser.add_argument('-i',
	metavar='dictionary', 
	dest='dictionary', 
	type=str, 
	nargs=1,
	default=False,
	help='Path to a pickled python dictionary that contains SAE phonological codes for each word (output from make_dictionaries.py). If not specified, user will be prompted to supply a path.'
)
args = parser.parse_args()

# If a dictionary was provided, use that as the filename;
# otherwise, ask for a filename with a GUI.
if args.dictionary:
	filename = args.dictionary[0]
else:
	filename = tkFileDialog.askopenfilename()

with open(filename,'rb') as f:
	D = pickle.load(f)

devoicing_rules = {
	'b':'p',
	'd':'t',
#	'g':'k',
	'v':'f',
	'z':'s'
	}

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
		dashes=utils.count_dashes(p)
		p=p.strip('_')
		pp=utils.parse_vowels(p)
		p=list(p)
		rule_applied = [False,False,False]
		# DEVOICING
		# Rule 1: Final phonemes /b/, /d/, /v/, or /z/ replaced with /p/, /t/,
		# /f/, and /s/, respectively.
		try:
			if pp[-2] in phoncodes.vowels and p[-1] in devoicing_rules.keys():
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
			if pp[-2] in phoncodes.consonants and p[-1] in ['t','d','s','z']:
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
			if pp[-2] in phoncodes.vowels and p[-1] == 'r':
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
	sys.stdout.write(' +'+'-'*41+'+\n')
	sys.stdout.write(' |')
	j=-1
	for k in logdict[rule].keys():
		if k=='total':
			continue
		j+=1
		sys.stdout.write('% 7s:% 4d' % (k,logdict[rule][k]))
		if (j%3) == 2:
			sys.stdout.write(' |\n')
			sys.stdout.write(' |')
		else:
			sys.stdout.write(' |')

	sys.stdout.write('\n')
	sys.stdout.write(' +'+'-'*41+'+\n\n')
