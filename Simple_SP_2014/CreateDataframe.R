# setwd('~/Documents/AAE/Simple_SP_2014')
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
# x <- sort(x) # hack to make sure phon preceeds sem
x <- x[substr(x,1,3) %in% c("AAE","SAE") & substrRight(x,3)=="txt"]
xsplit <- as.data.frame(do.call(rbind,strsplit(x,"_")),stringsAsFactors=FALSE)
names(xsplit) <- c("lang","cond","nwords","stage","unknown","nepochs","type","subj")
str(xsplit)
xsplit$nepochs <- as.numeric(substrAllButLast(xsplit$nepochs,2))
xsplit$subj <- as.numeric(substrAllButFirst(substrAllButLast(xsplit$subj,4),1))
str(xsplit)
ix <- with(xsplit, order(lang,subj,nepochs,type))
x <- x[ix]
xsplit <- xsplit[ix,]

colClassesPhon <- c("NULL","character","NULL",rep("numeric",250))
colClassesSem  <- c("NULL","NULL","NULL",rep("numeric",200))

ff <- subset(x, xsplit$subj==1)

n <- (length(ff)/2) * 500
Activations <- data.frame(matrix(ncol=458,nrow=n))
names(Activations)[1:8] <- c("lang","cond","nwords","stage","task","epoch","subj","word")
names(Activations)[9:(250+8)] <- paste('p',seq(1:250),sep='')
names(Activations)[(250+9):458] <- paste('s',seq(1:200),sep='')

for (i in seq(1,length(ff)/2)) {
  a <- ((i-1)*500)+1
  b <- 500*i
  
	fp <- ff[(i*2)-1]
	fs <- ff[i*2]
	info <- do.call(c,strsplit(fp,'_'))
	Activations$lang[a:b] <- info[1]
  Activations$cond[a:b] <- info[2]
  Activations$nwords[a:b] <- info[3]
  Activations$stage[a:b] <- as.numeric(substrRight(info[4],1))
  Activations$epoch[a:b] <- as.numeric(substrAllButLast(info[6],2))
	#outType <- info[7]
  Activations$subj[a:b] <- as.numeric(substrAllButFirst(substrAllButLast(info[8],4),1))
	
	temp.phon <- read.delim2(fp,
		header=FALSE,sep=" ",dec=".",
		colClasses=colClassesPhon
	)
	
	info.trial <- do.call(rbind,strsplit(temp.phon[,1],split="_"))
	Activations$word[a:b] <- info.trial[,1]
	Activations$task[a:b] <- info.trial[,2]
	temp.phon[,1] <- NULL
	
	temp.sem <- read.delim2(fs,
		header=FALSE,sep=" ",dec=".",
		colClasses=colClassesSem
	)
	
  Activations[a:b,9:458] <- cbind(temp.phon,temp.sem)
}
rm(temp.sem, temp.phon)
rm(info, info.trial)
rm(fp, fs)

Activations$lang <- as.factor(Activations$lang)
Activations$cond <- as.factor(Activations$cond)
Activations$nwords <- 5000
Activations$stage <- as.factor(Activations$stage)
Activations$word <- as.factor(Activations$word)

save(Activations,file="../UntrackedData/ActivationsAllEpochsS1.Rdata")

## Load and save targets
colClassesPhon <- c("character",rep("numeric",250))
colClassesSem  <- c("NULL",rep("numeric",200))

temp.AAE <- read.delim2("Phon_AAE_target.txt",
	header=FALSE,sep="\t",dec='.',
	colClasses=colClassesPhon
)
temp.AAE <- cbind("AAE", temp.AAE)
names(temp.AAE)[1] <- "lang"

temp.SAE <- read.delim2("Phon_SAE_target.txt",
	header=FALSE,sep="\t",dec='.',
	colClasses=colClassesPhon
)
temp.SAE <- cbind("SAE", temp.SAE)
names(temp.SAE)[1] <- "lang"

temp.sem <- read.delim2("Sem_SAE_target.txt",
	header=FALSE,sep="\t",dec='.',
	colClasses=colClassesSem
)

Targets <- cbind(rbind(temp.AAE,temp.SAE),temp.sem)
names(Targets)[1:2] <- c('lang','word')
names(Targets)[3:(250+2)] <- paste('p',seq(1:250),sep='')
names(Targets)[(250+3):dim(Targets)[2]] <- paste('s',seq(1:200),sep='')
Targets$word <- as.factor(Targets$word)
Targets$lang <- as.factor(Targets$lang)


str(Targets[,1:10])

# save(Targets,file='Targets.Rdata')
