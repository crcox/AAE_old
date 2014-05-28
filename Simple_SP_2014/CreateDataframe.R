setwd('~/Documents/AAE/Simple_SP_2014')
substrRight <- function(x, n){
  substr(x, nchar(x)-n+1, nchar(x))
}
substrAllButFirst <- function(x, n){
  substr(x, n+1, nchar(x))
}
substrAllButLast <- function(x, n){
  substr(x, 1, nchar(x)-n)
}

# Load and save activations
x <- list.files()
x <- sort(x) # hack to make sure phon preceeds sem
x <- x[substr(x,1,3) %in% c("AAE","SAE")]

temp <- NULL
colClassesPhon <- c("NULL","character","NULL",rep("numeric",250))
colClassesSem  <- c("NULL","NULL","NULL",rep("numeric",200))

for (i in seq(1,length(x),by=2)) {
	fp <- x[i]
	fs <- x[i+1]
	info <- do.call(c,strsplit(fp,'_'))
	lang <- info[1]
	type <- info[2]
	nwords <- info[3]
	stage <- as.numeric(substrRight(info[4],1))
	unknown <- info[5]
	totalEpochs <- as.numeric(substrAllButLast(info[6],2))
	#outType <- info[7]
	subj <- as.numeric(substrAllButFirst(substrAllButLast(info[8],4),1))
	
	temp.phon <- read.delim2(fp,
		header=FALSE,sep=" ",dec=".",
		colClasses=colClassesPhon
	)
	
	info.trial <- do.call(rbind,strsplit(temp.phon[,1],split="_"))
	word <- info.trial[,1]
	cond <- info.trial[,2]
	temp.phon[,1] <- NULL
	
	temp.sem <- read.delim2(fs,
		header=FALSE,sep=" ",dec=".",
		colClasses=colClassesSem
	)
	
	temp.comb <- cbind(lang,type,nwords,stage,totalEpochs,subj,word,cond,temp.phon,temp.sem)
	
	temp <- rbind(temp,temp.comb)
}

names(temp)[9:(250+8)] <- paste('p',seq(1:250),sep='')
names(temp)[(250+9):dim(temp)[2]] <- paste('s',seq(1:200),sep='')

Activations <- temp

save(d,file="Activations.Rdata")

## Load and save targets
colClassesPhon <- c("character",rep("numeric",250))
colClassesSem  <- c("NULL",rep("numeric",200))

temp.AAE <- read.delim2("Phon_AAE_target.txt",
	header=FALSE,sep="\t",dec='.',
	colClasses=colClassesPhon
)

temp.SAE <- read.delim2("Phon_SAE_target.txt",
	header=FALSE,sep="\t",dec='.',
	colClasses=colClassesPhon
)

temp.sem <- read.delim2("Sem_SAE_target.txt",
	header=FALSE,sep="\t",dec='.',
	colClasses=colClassesSem
)

Targets <- cbind(rbind(temp.AAE,temp.SAE),temp.sem)
names(Targets)[1] <- 'word'
names(Targets)[2:(250+1)] <- paste('p',seq(1:250),sep='')
names(Targets)[(250+2):dim(Targets)[2]] <- paste('s',seq(1:200),sep='')
Targets$word <- as.factor(Targets$word)

str(Targets[,1:10])

save(Targets,file='Targets.Rdata')