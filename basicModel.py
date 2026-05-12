import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize

F = norm.cdf

def effortUtility(x, k):    # function g(x) times k
    if x <= 0 or x >= 1:
        return np.inf
    return k * (1/(x * (1 - x)))

def runSimulation(strategiesArr, rng, cutoffsArr, stratInd, effortAmp):
    noise = rng.standard_normal()
    signal = strategiesArr[stratInd]
    receivedSignal = signal + noiseAmp * noise
    isCorrectComm = cutoffsArr[stratInd] < receivedSignal <= cutoffsArr[stratInd + 1]
    payoff = isCorrectComm - effortUtility(signal, effortAmp)
    return isCorrectComm, payoff

def successProb(a, b, sigma):
    return 0.5 * F( (0.5 - a) / sigma ) + 0.5 * (1- F( (0.5 - b) / sigma ))

def expectedPayoff(a, b, sigma, k):
    return successProb(a, b, sigma) - 0.5 * (effortUtility(a, k) + effortUtility(b, k))

def modifiedExpectedPayoff(vec, sigma, k):
    delta = vec[0]
    return -expectedPayoff(0.5 - delta, 0.5 + delta, sigma, k)

rng = np.random.default_rng()

### set these values ###
### set these values ###
numSimulations = 10_000
noiseAmp = 0.05     # sigma
effortAmp = 0.05    # k
### END OF set these values ###
### END OF set these values ###

strategiesArr = [0.4, 0.6]

numStrategies = len(strategiesArr)

# constants c_ab, c_bc etc, preceded by -inf and followed by inf for comparison
cutoffsArr = [-np.inf]
for i in range(numStrategies - 1):
    cutoffOptimal = (strategiesArr[i] + strategiesArr[i + 1]) / 2
    cutoffsArr.append(cutoffOptimal)
cutoffsArr.append(np.inf)

delta = 0.5 - strategiesArr[0]

x0 = np.array([delta])

res = minimize(
    modifiedExpectedPayoff,
    x0,
    args=(noiseAmp, effortAmp),
    method="Nelder-Mead",
)

# # debugging the minimizer
# print(res.x)      # minimizer
# print(res.fun)    # minimum value
# print(res.success)
# print(res.message)

delta = res.x[0]
strategiesArr[0] = 0.5 - delta
strategiesArr[1] = 0.5 + delta

print("The optimal found x_a and x_b are", *strategiesArr)

totalPayoff = 0
totalSuccessComms = 0
numSimsPerStrat = numSimulations // numStrategies

for stratInd in range(numStrategies):
    for _ in range(numSimsPerStrat):
        isCorrectComm, payoff = runSimulation(strategiesArr, rng, cutoffsArr, stratInd, effortAmp)
        totalSuccessComms += isCorrectComm
        totalPayoff += payoff


print("Total number of correct communications is", totalSuccessComms)
print("Estimated probability of a correct communication is", totalSuccessComms / numSimulations)
print("Total payoff is", totalPayoff)
print("Average payoff is", totalPayoff / numSimulations)