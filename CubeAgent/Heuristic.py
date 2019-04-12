import pickle
import random
from CubeAgent.State import CubeState


class Heuristic:
    # maximum number of quarter turns needed to solve any state: 14
    def __init__(self):
        heuristicFile = open("cubeStateHeuristic", 'rb')
        self.heuristicValues = pickle.load(heuristicFile)
        heuristicFile.close()
        # print(self.heuristicValues)

    def heuristicLookup(self, state):
        if tuple(state) not in self.heuristicValues:
            return 14  # inconsistent heuristic returns a value that is >= the actual path cost
        else:
            return self.heuristicValues[tuple(state)]


class HeuristicTrainer:
    def __init__(self):
        self.filename = "cubeStateHeuristic"
        self.possibleMoves = ['R', 'L', 'U', 'D', 'F', 'B', 'r', 'l', 'u', 'd', 'f', 'b']

    def trainHeuristic(self):
        cube = CubeState()

        states = [cube.cubelets]
        stateCostDict = {}
        for i in range(1, 9):
            print(i)
            randomMoves = random.sample(self.possibleMoves, 6)
            temp = {tuple(cube.getRotatedCubelets(face, state)): i
                    for face in randomMoves for state in states}
            states = temp.keys()
            temp.update(stateCostDict)
            stateCostDict = temp
            print(len(stateCostDict))

        # state = cube.cubelets
        # firstRandomMoves = random.sample(self.possibleMoves, 6)
        # randomStates = {tuple(cube.getRotatedCubelets(face, state)): 1 for face in firstRandomMoves}
        # secondRandomMoves = random.sample(self.possibleMoves, 6)
        # tempDict = {tuple(cube.getRotatedCubelets(face, list(randState))): 2
        #             for face in secondRandomMoves for randState in randomStates}
        # randomStates.update(tempDict)
        heuristicFile = open(self.filename, 'wb')
        pickle.dump(stateCostDict, heuristicFile)
        heuristicFile.close()


if __name__ == '__main__':
    trainer = HeuristicTrainer()
    trainer.trainHeuristic()
    file = open("cubeStateHeuristic", 'rb')
    dict = pickle.load(file)
    file.close()