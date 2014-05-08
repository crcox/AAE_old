import argparse, pickle, os
import DictClasses

parser = argparse.ArgumentParser(
	description='Pick a subset of N words, subject to certain conditions.'
)
parser.add_argument('-w',
	metavar='WordToPhon',
	dest='WordToPhon',
	type=str, 
	nargs='+',
	default=False,
	help='Path to a text file that maps between a word and its orth, phon, and freq data. File is assumed to be white-space delimited.'
)
parser.add_argument('-p', 
	metavar="PhonToPattern",
	dest="PhonToPattern",
	type=str,
	nargs='+',
	default=False,
	help='Path to a text file that maps between phon symbols and their binary patterns (for training the network in Lens. File is assumed to be white-space delimited.'
)

# This script will take the text files and create python dictionaries. These
# dictionaries will be referenced rather than the text files themselves in all
# python scrips. This script should be re-run any times the files 3kdict or
# 6kdict are changed.

for p in args.WordToPhon:
	D = DictClasses.WordToPhon(p);
	print ''
	D.parse()
	print 'Parsed text file %s...' % D.textpath
	D.save()
	print 'Wrote binary file %s.' % D.dictpath

for p in args.PhonToPattern:
	D = DictClasses.PhonToPatten(p);
	print ''
	D.parse()
	print 'Parsed text file %s...' % D.textpath
	D.save()
	print 'Wrote binary file %s.' % D.dictpath
