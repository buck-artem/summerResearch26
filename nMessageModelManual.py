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
strategiesArr = [0.4, 0.6]  # arr of x_a, x_b, x_c etc
noiseAmp = 0.05     # sigma
effortAmp = 0.05    # k
# constants c_ab, c_bc etc, preceded by -inf and followed by inf for comparison
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


print("Total number of correct communications is", totalSuccessComms)
print("Estimated probability of a correct communication is", totalSuccessComms / numSimulations)
print("Total payoff is", totalPayoff)
print("Average payoff is", totalPayoff / numSimulations)