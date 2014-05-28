import pickle, os
from itertools import izip

class AAEDict:
	def __init__(self,filepath,semrepspath=''):
		self.textpath=filepath
		self.semrepspath=semrepspath
		pathparts = os.path.splitext(filepath)
		self.dictpath=pathparts[0] + '.pkl'
		self.d = {}
		
	def save(self):
		with open(self.dictpath,'wb') as f:
			pickle.dump(self.d,f)
	

class WordToPhon(AAEDict):
	def parse(self):
		with open(self.textpath,'r') as f, open(self.semrepspath,'r') as s:
			for line,rep in izip(f,s):
				x = line.strip().split()
				semrep = [int(b) for b in rep.strip().split()]
				try:
					self.d[x[0]] = {
							'orth':x[1],
							'SAE_phon':x[2],
							'freq':int(x[3]),
							'sem_rep':semrep
						}
				except ValueError:
					self.d[x[0]] = {
							'orth':x[1],
							'SAE_phon':x[2],
							'freq':int(float(x[3])),
							'sem_rep':semrep
						}
	
	def setSemRepsPath(self,filepath):
		self.semrepspath=filepath

class PhonToPattern(AAEDict):
	def parse(self):
		with open(self.textpath,'r') as f:
			for line in f:
				x = line.strip().split()
				self.d[x[0]] = [int(i) for i in x[1:]]

	def getDict(self):
		return(self.d)


