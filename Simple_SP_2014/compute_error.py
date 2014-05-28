import scipy,numpy
import pickle

tpAAE = {}
with open('Phon_AAE_target.txt','r') as f:
	for line in f:
		temp = line.strip().split()
		tpAAE[temp[0]] = temp[1:]
tpSAE = {}
with open('Phon_SAE_target.txt','r') as f:
	for line in f:
		temp = line.strip().split()
		tpSAE[temp[0]] = temp[1:]
tsSAE = {} # both use same sem
with open('Sem_SAE_target.txt','r') as f:
	for line in f:
		temp = line.strip().split()
		tsSAE[temp[0]] = temp[1:]


