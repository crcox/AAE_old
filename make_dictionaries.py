import pickle
# This script will take the text files and create python dictionaries. These
# dictionaries will be referenced rather than the text files themselves in all
# python scrips. This script should be re-run any times the files 3kdict or
# 6kdict are changed.
def parse_to_dict(filename):
	d={}
	with open(filename,'r') as f:
		for line in f:
			x = line.strip().split()
			try:
				d[x[0]] = {'orth':x[1],'phon':x[2],'freq':int(x[3])}
			except ValueError:
				d[x[0]] = {'orth':x[1],'phon':x[2],'freq':int(float(x[3]))}
	return d

d = parse_to_dict('3kdict')
print ''
print 'Parsed text file 3kdict...'
with open('3kdict.pkl','wb') as f:
	pickle.dump(d,f)
print 'Wrote binary file 3kdict.pkl.'

d = parse_to_dict('6kdict')
print ''
print 'Parsed text file 6kdict...'
with open('6kdict.pkl','wb') as f:
	pickle.dump(d,f)
print 'Wrote binary file 6kdict.pkl.'
print ''
