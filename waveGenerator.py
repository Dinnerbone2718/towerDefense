import random
import numpy as np
layerWeights = {
    1: 1.5,
    2: 2,
    3: 4,
    4: 6,
    5: 12,
    6: 32,
    7: 64,  
    8: 1000,
    9: 5000,
    10: 20000,
    11: 100000, 
    12: 1000000
}

needsChange = {
    
    
}

def calculateWeightedDifficulty(rounds, weights):
    difficulties = []
    for rnd in rounds:
        roundDifficulty = sum(weights.get(layer, 1) * layer / spawnTime for layer, spawnTime in rnd)
        difficulties.append(roundDifficulty)
    return difficulties


def generateRounds(
    numRound = 100,
    roundLength = 20,
    introductionRounds = {1:1, 2:3, 3:5, 4:10, 5:12, 6: 20, 7:25, 8:35, 9:40, 10:45, 11:50, 12:62}
    
    ):

    rounds = []
    
    for i in range(1, numRound+1):
        currentRound = []
        eligibleItems = {
            item: round_ for item, round_ in introductionRounds.items()
            if round_<=i
        }
        
        odds = {
            item: int(-(.75 * i - round_)**2 + 30)
            for item, round_ in eligibleItems.items()
            if int(-(.75 * i - round_)**2 + 30) > 0
        }
        print(odds)
        totalSum = sum(odds.values())
        for key in odds.keys():
            for _ in range(int(np.floor((odds[key]/totalSum) * roundLength))):
                currentRound.append((key, 2))
        rounds.append(currentRound)
        print(i)
        print(currentRound)
        
    return rounds


roundNormal = generateRounds()
newRound = roundNormal
curve = 100000
for r in range(curve):
    print(f"{int((r/curve)*100)}% {'|' * int((r/curve)*100)}")
    # Calculate difficulties with weights
    roundDifficulties = calculateWeightedDifficulty(newRound, layerWeights)
    
    for i, difficulty in enumerate(roundDifficulties, 1):
        #print(f"({i},{difficulty:.2f})")
        diff = difficulty-(17.5595 * 1.2311**i)
        #print((17.5595 * 1.2311**i))
        needsChange[i] = .01 if 0 > (1-diff) else -.01
    
    adjustedRounds = []
    for i, roundData in enumerate(newRound, 1):
        adjustedRound = []
        for layer, spawnTime in roundData:
            newSpawnTime = max(0.1, round(spawnTime + needsChange.get(i, 0), 2))
            adjustedRound.append((layer, newSpawnTime))
        adjustedRounds.append(adjustedRound)
    newRound = adjustedRounds  

print("[")
for x in newRound:
    print(x, end="")
    print(",")
    print("")
print("]")







