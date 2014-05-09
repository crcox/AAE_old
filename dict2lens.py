import argparse, pickle, os
import tkFileDialog
from utils import *

parser = argparse.ArgumentParser(
	description='Translate a dictionary for a training sample into Lens .ex.'
)
parser.add_argument('-i',
	metavar='dictionary',
	dest='dictionary',
	type=str, 
	default=False,
	help='Path to a pickled python dictionary that contains SAE and AAE phonological codes for each word (output from pick_subset.py).'
)
parser.add_argument('-m',
	metavar='pmap',
	dest='pmap',
	type=str, 
	default=False,
	help='Path to a pickled python dictionary that contains mapping between phonological symbols and binary patterns (output from make_dictionaries.py).'
)
args = parser.parse_args()

if args.dictionary==False:
#	args = utils.guiGetConstraints(args)
	print "Select a pickled WordToPhon dictionary with AAE phonology..."
	args.dictionary = tkFileDialog.askopenfilename()

if args.pmap==False:
#	args = utils.guiGetConstraints(args)
	print "Select a pickled PhonToPattern dictionary..."
	args.dictionary = tkFileDialog.askopenfilename()

with open(args.dictionary,'rb') as f:
	D = pickle.load(f)

with open(args.pmap,'rb') as f:
	M = pickle.load(f)

# Reminders about Lens example files:
# - Files begin with a header that set defaults.
# - The header is terminated with a semi-colon.
# - Each ``trial'' can be composed of many events.
# - In this model, there are three events:
#   1. Presentation
#   2. Settling---letting the recurrent dynamics happen
#   3. Evaluation---the targets are presented, and error assessed.
# - Each event lasts two ticks, so a full trial is 6 ticks.

fileparts = os.path.splitext(args.dictionary)
filename = fileparts[0] + '.ex'
header = {'defI': 0, 'defT': 0, 'actI': 1, 'actT': 1, 'min': 2, 'max': 2, 'grace': 0}
words = D.keys()
words.sort()
with open(filename,'w') as f:
	Ex = LensEx(D,M,f)
	Ex.writeHeader(header)

	for word in words:
		Ex.writeExample(word,itype='Phon',ttype='Phon',lang='AAE')
