import pickle
with open('3kdict.pkl','rb') as f:
	D=pickle.load(f)

print 'cent'
print D['cent']['SAE_phon']
print D['cent']['sem_rep']
print D['cent']['freq']
