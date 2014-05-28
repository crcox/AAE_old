load('Activations.Rdata',verbose=T)
load('Targets.Rdata',verbose=T)

str(Activations[,1:10])
str(Targets[,1:10])

A = subset(Activations,
	Activations$lang=="AAE" &
	Activations$subj==1
)
for (w in )


dim(Activations)
dim(Targets)