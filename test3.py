import pickle

with open('mapping.pkl','rb') as f:
	M = pickle.load(f)

print "/a/"
print M['a']

