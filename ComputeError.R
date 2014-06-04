setwd('~/AAE/')
load('UntrackedData/ActivationsAllEpochsS1.Rdata',verbose=T)
load('Simple_SP_2014//Targets.Rdata',verbose=T)
source('accCosineDistance.R')
source('sub2ind.R')

phon <- rep(FALSE, 450); phon[1:250] <- TRUE
sem <- rep(FALSE, 450); sem[251:450] <- TRUE
x <- matrix(0,3,2)


n <- length(unique(Activations$epoch))
lang <- c("AAE","SAE")
# Accuracy <- data.frame(matrix(ncol=6,nrow=n*500*2))
# names(Accuracy) <- c("lang","epoch","word","all","phon","sem")
load('UntrackedData/Accuracy.Rdata')

counter = 0
for (j in seq(1:2)) {
  TT <- as.matrix(Targets[,3:452])
  TT <- TT[Targets$lang == lang[j],]
  for (i in seq(1:n)) {
    counter <- counter + 1
    txtProgressBar(0,n*2,initial=counter,width=80,style=3)
    a <- sub2ind(c(500,n,2),1,i,j)
    b <- (a-1) + 500
    if (!is.na(Accuracy$epoch[a])) {next}
    AA <- subset(Activations,
                Activations$lang==lang[j] &
                Activations$epoch==(i * 10)
    )
    AA <- as.matrix(AA[,9:458])

    Accuracy$lang[a:b] <- lang[j]
    Accuracy$epoch[a:b] <- (i * 10)
    Accuracy$all[a:b] <- accCosineDistance(AA,TT)
    Accuracy$phon[a:b] <- accCosineDistance(AA[,phon],TT[,phon])
    Accuracy$sem[a:b] <- accCosineDistance(AA[,sem],TT[,sem])
  }
}
Accuracy <- Accuracy[!is.na(Accuracy$epoch), ]
save(Accuracy,file="UntrackedData/Accuracy.Rdata")

# 
# x[1,1] <- mean(apply(COS,2,which.max) == seq(1:500))
# 
# COS.phon <- TT[,phon] %*% t(AA[,phon])
# x[2,1] <- mean(apply(COS.phon,2,which.max) == seq(1:500))
# 
# COS.sem <- TT[,sem] %*% t(AA[,sem])
# x[3,1] <- mean(apply(COS.sem,2,which.max) == seq(1:500))
# 
# # SAE
# AA <- subset(Activations,
#             Activations$lang=="SAE" &
#             Activations$subj==3,
# )
# 
# AA <- as.matrix(AA[,9:458])
# s <- apply(AA,2,function(x) sqrt(sum(x^2)))
# S <- matrix(
#   rep(s,500),
#   nrow=500,byrow=TRUE
# )
# AA[,s!=0] <- AA[,s!=0]/S[,s!=0]
# rm(s)
# rm(S)
# 
# TT <- subset(Targets,
#             Targets$lang=="SAE"
# )
# 
# TT <- as.matrix(TT[,3:452])
# s <- apply(TT,2,function(x) sqrt(sum(x^2)))
# S <- matrix(
#   rep(s,500),
#   nrow=500,byrow=TRUE
# )
# TT[,s!=0] <- TT[,s!=0]/S[,s!=0]
# rm(s)
# rm(S)
# 
# COS <- TT %*% t(AA)
# x[1,2] <- mean(apply(COS,2,which.max) == seq(1:500))
# 
# COS.phon <- TT[,phon] %*% t(AA[,phon])
# x[2,2] <- mean(apply(COS.phon,2,which.max) == seq(1:500))
# 
# COS.sem <- TT[,sem] %*% t(AA[,sem])
# x[3,2] <- mean(apply(COS.sem,2,which.max) == seq(1:500))
# 
# # Plot
# bars <- barplot(t(x),beside=T,ylim=c(0,1))
# legend("top",legend=c("AAE","SAE"),fill=grey.colors(2))
# mtext(c("All","Phon","Sem"),side=1,line=1,at=colMeans(bars))
# mtext("Accuracy",side=2,line=3)
