import subprocess

def wccount(filename):
	out = subprocess.Popen(['wc', '-l', filename],
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT
			).communicate()[0]
	return int(x.strip().split()[0])
