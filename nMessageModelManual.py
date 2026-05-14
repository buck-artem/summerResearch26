# sigma, k, but also x_a, x_b, x_c... and c_ab, c_bc... are set manually inside the code


import numpy as np


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


rng = np.random.default_rng()

### set these values ###
### set these values ###
numSimulations = 10_000
# size of strategiesArr determines the number of messages in your model
strategiesArr = [0.4, 0.6]  # arr of x_a, x_b, x_c etc   #for now set manually, should be optimized
noiseAmp = 0.05     # sigma
effortAmp = 0.05    # k
# constants c_ab, c_bc etc, preceded by -inf and followed by inf for comparison
# len of cutoffsArr should be len(strategiesArr) + 1
cutoffsArr = [-np.inf, 0.5, np.inf]
### END OF set these values ###
### END OF set these values ###

totalPayoff = 0
totalSuccessComms = 0
numStrategies = len(strategiesArr)
numSimsPerStrat = numSimulations // numStrategies

for stratInd in range(numStrategies):
    for _ in range(numSimsPerStrat):
        isCorrectComm, payoff = runSimulation(strategiesArr, rng, cutoffsArr, stratInd, effortAmp)
        totalSuccessComms += isCorrectComm
        totalPayoff += payoff


print("Parameters: sigma = ", noiseAmp, "; k = ", effortAmp, sep = "", end="")
print("; x's = ", end="")
print(*strategiesArr, sep = ", ", end="")
print("; c's = ", end="")
print(*cutoffsArr[1:-1], sep = ", ")
print("Total number of successful communications is", totalSuccessComms, "out of", numSimulations, "simulations")
print("Estimated probability of a successful communication is", totalSuccessComms / numSimulations)
print("Total payoff is", totalPayoff)
print("Average payoff is", totalPayoff / numSimulations)