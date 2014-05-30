sub2ind <-function(siz,...) {
  siz <- as.numeric(siz)
  varargin <- as.list(match.call())[-1L]
  nargin <- length(varargin)
  
  # number of dimensions (rank) of subs
  d <- nargin-1
  
  s <- dim(do.call(as.matrix,varargin[2]))
  
  if (d == 1) {
    #   Assume 2nd arg is matrix whose cols are subscripts
    #   s(1): num of dimensions, must be equal to length(siz)
    #   s(2): num of indices to output
    d <- s[1];
    m <- varargin[[2]]
  } 
  else {
    m <- as.matrix(do.call(cbind,varargin[2:nargin]))
  }
  
  if (length(siz) != d) {
    if (length(siz)<d) {
      siz <- c(siz, rep(1,d-length(siz)))
    }
    else {
      siz = c(siz[1:d-1], prod(siz[d:length(siz)]))
    }
  }
  
  #Compute linear indices
  k = c(1, cumprod(siz[1:length(siz)-1]))
  
  return(as.numeric(1 + matrix(k,ncol=d) %*% t(matrix((m-1),ncol=2))))
  
}
