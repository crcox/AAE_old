accCosineDistance <- function(AA,TT) {
  cossim <- function(AA,TT) {
    unitnorm <- function(x) {
      s <- apply(x,2,function(x) sqrt(sum(x^2)))
      S <- matrix(
        rep(s,500),
        nrow=500,byrow=TRUE
      )
      x[,s!=0] <- x[,s!=0]/S[,s!=0]
      return(x)
    }
    return(unitnorm(TT) %*% t(unitnorm(AA)))
  }
  COSSIM <- cossim(AA,TT)
  return(apply(COSSIM,2,which.max) == seq(1:dim(COSSIM)[2]))
}