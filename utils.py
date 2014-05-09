import Tkinter

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
    def __init__(self,dictPath,phonMap):
	self.dictPath = dictPath
	self.phonMap = phonMap
	fileparts = os.path.splitext(dictPath)
	self.exPath = fileparts[0] + '.ex'
	self.h = open(self.exPath,'w')
    
    def writeHeader(self,params):
	for k,v in params.items():
	    self.h.write("%s: %d\n" % (k,v))
	self.h.write(';\n\n')

    def parseExample(self,word,data,type,lang):
	# This is not flexible---written for specific case.
	self.example = {}
	self.example['name'] = '_'.join([word,type,lang])
	self.example['freq'] = data['freq']
	self.example['nEvents'] = 3
	
	E = initEvents()
	pattern = [self.phonMap[s] for s in data[]
	E[0]['i']

	self.example['events']
	self.example['events']

    def initEvents(self):
	e = {}
	e['i'] = {}
	e['i']['null'] = []
	e['i']['active'] = []
	e['t']['null'] = []
	e['t']['active'] = []
	E = [e for i in self.example['nEvents']]
	return E


    def writeExample(self,params):
	self.h.write('name: %s\n' % params['name'])
	self.h.write('freq: %s\n' % params['freq'])
	self.h.write('%d\n' % params['nEvents'])
	for i,event in params['events']:
	    self.h.write('[%d] ' % i)
	    # Input
	    self.h.write('i: ')
	    ix = params['events'][i]['i']['null']
	    if len(ix) > 0:
		self.h.write('{-} ')
		self.h.write('%d ' % ix)

	    ix = params['events'][i]['i']['active']
	    if len(ix) > 0:
		self.h.write('{1} ')
		self.h.write('%d ' % ix)

	    # Target
	    self.h.write('t: ')
	    ix = params['events'][i]['t']['null']
	    if len(ix) > 0:
		self.h.write('{-} ')
		self.h.write('%d ' % ix)

	    ix = params['events'][i]['t']['active']
	    if len(ix) > 0:
		self.h.write('{1} ')
		self.h.write('%d ' % ix)

	self.h.write(';\n\n')


