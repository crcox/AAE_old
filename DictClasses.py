import pickle, os

class AAEDict:
	def __init__(self,filepath):
		self.textpath=filepath
		pathparts = os.path.splitext(filepath)
		self.dictpath=pathparts[0] + '.pkl'
		self.d = {}
		
	def save(self):
		with open(self.dictpath,'wb') as f:
			pickle.dump(self.d,f)
	

class WordToPhon(AAEDict):
	def parse(self):
		with open(self.textpath,'r') as f:
			for line in f:
				x = line.strip().split()
				try:
					self.d[x[0]] = {
							'orth':x[1],
							'SAE_phon':x[2],
							'freq':int(x[3])
						}
				except ValueError:
					self.d[x[0]] = {
							'orth':x[1],
							'SAE_phon':x[2],
							'freq':int(float(x[3]))
						}

class PhonToPattern(AAEDict):
	def parse(self):
		with open(self.textpath,'r') as f:
			for line in f:
				x = line.strip().split()
				self.d[x[0]] = x[1:]


