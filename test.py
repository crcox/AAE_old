import pickle
with open('3kdict_with_aae.pkl','rb') as f:
	D=pickle.load(f)

print 'cent'
print D['cent']['SAE_homo']
print D['cent']['AAE_homo']
