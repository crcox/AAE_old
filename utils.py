import math, os, Tkinter

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

def guiGetConstraints(args):
	root = Tkinter.Tk()
	def getValuesAndClose():
		args.n = int(sampleSize_entry.get())
		args.n_same = int(nSame_entry.get())
		args.n_homo = int(nHomo_entry.get())
		root.destroy()

	def getValuesAndClose_bind(event):
		args.n = int(sampleSize_entry.get())
		args.n_same = int(nSame_entry.get())
		args.n_homo = int(nHomo_entry.get())
		root.destroy()

	root.title("Specify constraints")
	mainframe = Tkinter.Frame(root)
	mainframe.grid(column=0, row=0, sticky=('n','w','e','s'))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)

	sampleSize = Tkinter.StringVar()
	nSame = Tkinter.StringVar()
	nHomo = Tkinter.StringVar()

	sampleSize_entry = Tkinter.Entry(mainframe, width=7, textvariable=sampleSize)
	sampleSize_entry.grid(column=2,row=1, sticky=('w','e'))
	nSame_entry = Tkinter.Entry(mainframe, width=7, textvariable=nSame)
	nSame_entry.grid(column=2,row=2, sticky=('w','e'))
	nHomo_entry = Tkinter.Entry(mainframe, width=7, textvariable=nHomo)
	nHomo_entry.grid(column=2,row=3, sticky=('w','e'))

	Tkinter.Label(mainframe, text="Sample size:").grid(column=1,row=1,sticky='w')
	Tkinter.Label(mainframe, text="Number same:").grid(column=1,row=2,sticky='w')
	Tkinter.Label(mainframe, text="Number of homophones:").grid(column=1,row=3,sticky='w')

	Tkinter.Button(mainframe, text="OK", command=getValuesAndClose).grid(column=2, row=4)

	for child in mainframe.winfo_children():
		child.grid_configure(padx=5, pady=5)
	
	sampleSize_entry.focus()
	root.bind('<Return>',getValuesAndClose_bind)
	root.mainloop()
	return(args)

class LensEx:
	def __init__(self,WordToPhon,PhonToPattern,handle):
		self.D = WordToPhon
		self.pMap = PhonToPattern
		self.h = handle
		self.slen=len(self.D[self.D.keys()[0]]['sem_rep'])
		self.plen=len(self.pMap[self.pMap.keys()[0]])
		self.UnitRanges = {
				'all':'*',
				'phon':'%d-%d' % (0,self.plen),
				'sem':'%d-%d' % (self.plen,self.plen+self.slen)
				}

	def writeHeader(self,params):
		for k,v in params.items():
			self.h.write("%s: %d\n" % (k,v))
		self.h.write(';\n\n')

	def writeExample(self,word,itype,ttype,lang):
		self.word = word.lower()
		self.itype = itype.lower()
		self.ttype = ttype.lower()
		self.lang = lang.upper()
		
		self.parseExample()
		
		try:
			logfreq = math.log(self.example['freq'])
		except ValueError:
			logfreq = 0

		self.h.write('name: %s\n' % self.example['name'])
		self.h.write('freq: %.4f\n' % logfreq)
		self.h.write('%d\n' % self.example['nEvents'])
		for i,event in enumerate(self.example['events']):
			self.h.write('[%d] ' % i)
			# Input
			self.h.write('i: ')
			x = self.example['events'][i]['i']['null']
			if len(x) > 0:
				self.h.write('{-} %s ' % x)
	
			x = self.example['events'][i]['i']['active']
			if len(x) > 0:
				self.h.write('{1} %s ' % x)
	
			# Target
			self.h.write('t: ')
			x = self.example['events'][i]['t']['null']
			if len(x) > 0:
				self.h.write('{-} %s ' % x)
	
			x = self.example['events'][i]['t']['active']
			if len(x) > 0:
				self.h.write('{1} %s ' % x)
			
			self.h.write('\n')
	
		self.h.write(';\n\n')

	def parseExample(self):
		# This is not flexible---written for specific case.
		icode = '_'.join([self.lang,self.itype])
		if self.itype == "phon":
			ipattern = []
			for s in self.D[self.word][icode]:
				ipattern.extend(self.pMap[s])
		else:
			ipattern = self.D[self.word]['sem_rep']

		tcode = '_'.join([self.lang,self.ttype])
		if self.ttype == "phon":
			tpattern = []
			for s in self.D[self.word][icode]:
				tpattern.extend(self.pMap[s])
		else:
			tpattern = self.D[self.word]['sem_rep']

		self.example = {}
		self.example['name'] = '_'.join([self.word,self.itype,self.ttype,self.lang])
		self.example['freq'] = self.D[self.word]['freq']
		self.example['nEvents'] = 3
	
		E = self.initEvents()
		if self.itype == "phon":
			E[0]['i']['active'] = ' '.join([str(i) for i, e in enumerate(ipattern) if e != 0])
		else:
			E[0]['i']['active'] = ' '.join([i+self.plen for i, e in enumerate(ipattern) if e != 0])

		E[0]['t']['null'] = self.UnitRanges["all"]
		E[1]['i']['null'] = self.UnitRanges["all"]
		E[1]['t']['null'] = self.UnitRanges["all"]
		E[2]['i']['null'] = self.UnitRanges["all"]

		if self.ttype == "phon":
			E[2]['t']['null'] = self.UnitRanges["sem"]
			E[2]['t']['active'] = ' '.join([str(i) for i, e in enumerate(tpattern) if e != 0])
		else:
			E[2]['t']['null'] = self.UnitRanges["phon"]
			E[2]['t']['active'] = ' '.join([str(i+self.plen) for i, e in enumerate(tpattern) if e != 0])
		self.example['events'] = E

	def initEvents(self):
		E = []
		for i in range(self.example['nEvents']):
			e = {}
			e['i'] = {}
			e['t'] = {}
			e['i']['null'] = ''
			e['i']['active'] = ''
			e['t']['null'] = ''
			e['t']['active'] = ''
			E.append(e)
		
		return(E)

	def close(self):
		self.h.close()

