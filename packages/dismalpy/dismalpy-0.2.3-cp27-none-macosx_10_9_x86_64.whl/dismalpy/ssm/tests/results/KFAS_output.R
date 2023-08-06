# KFAS output
library(KFAS)
options(digits=10)

getNileModel <- function(params) {
  modelNile <- SSModel(Nile ~ SSMtrend(2, Q=list(matrix(NA), matrix(NA))), H=matrix(NA))
  modelNile$H[1,1,1] = params[1]
  modelNile$Q[1,1,1] = params[2]
  modelNile$Q[2,2,1] = params[3]
  return(modelNile)
}

# Setup the basic model (local linear trend)
initModelNile <- SSModel(Nile ~ SSMtrend(2, Q=list(matrix(NA), matrix(NA))), H=matrix(NA))

# Fit the model with MLE
fitNile <- fitSSM(inits=c(log(var(Nile)), log(var(Nile)), log(var(Nile))), model=initModelNile,
                             method="BFGS", control=list(REPORT=1, trace=1))

# Save the fitted parameters
params <- c(fitNile$model$H[1,1,1], fitNile$model$Q[1,1,1], fitNile$model$Q[2,2,1])
print(params)  # 14682.10019, 1749.362846, 0.01180446767

# Note, dismalpy.ssm can match this likelihood value
# to 6 decimal places (-629.876027) when the initial
# (approximate) diffuse variance is 1e13, and the
# parameters are set to those found above.
print(fitNile$optim.out$value)  # 629.876027

# Using the estimated MLE parameters, filter with exact diffuse initialization
# for both states
modelNile <- getNileModel(params)
outNileBoth <- KFS(modelNile, filtering="state", smoothing="state")

# Using the estimated MLE parameters, filter with exact diffuse initialization
# only for the second state (and approximate diffuse initialization for the
# first state, with initial variance 1e6).
# This forces F_infty=0 even though P_infty not = 0.
modelNile <- getNileModel(params)
modelNile$P1[1,1] <- 1e6
modelNile$P1inf[1,1] <- 0
outNileSecond <- KFS(modelNile, filtering="state", smoothing="state")

# Using the estimated MLE parameters, filter with approximate diffuse initialization
# for both states, with initial variance 1e6.
modelNile <- getNileModel(params)
modelNile$P1[1,1] <- 1e6
modelNile$P1inf[1,1] <- 0
modelNile$P1[2,2] <- 1e6
modelNile$P1inf[2,2] <- 0
outNileNone <- KFS(modelNile, filtering="state", smoothing="state")

print(outNileBoth$P[,,1:2])
print('------')
print(outNileSecond$P[,,1:2])
print('------')
print(outNileNone$P[,,1:2])
