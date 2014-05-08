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
