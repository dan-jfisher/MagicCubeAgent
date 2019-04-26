import unittest
from datetime import datetime
from CubeAgent.State import CubeState
from CubeAgent.Agent import CubeAgent
import pickle
import random
import matplotlib.pyplot as plt
import numpy as np



class TestCubeState(unittest.TestCase):

    def test360DegreeTurns(self):
        cubeState = CubeState()
        self.turn360('R', cubeState)
        self.turn360('L', cubeState)
        self.turn360('U', cubeState)
        self.turn360('D', cubeState)
        self.turn360('F', cubeState)
        self.turn360('B', cubeState)
        self.turn360('r', cubeState)
        self.turn360('l', cubeState)
        self.turn360('u', cubeState)
        self.turn360('d', cubeState)
        self.turn360('f', cubeState)
        self.turn360('b', cubeState)

    # def testNTurns(self):
    #     cube1 = CubeState()
    #     cube2 = CubeState()
    #
    #     cube1.rotateFace1Turn('R')
    #     cube1.rotateFace1Turn('R')
    #
    #     cube2.rotateFace('R', 2)
    #
    #     self.assertEqual(cube1.cubelets, cube2.cubelets)

    def turn360(self, face, cubeState):
        origCubelets = cubeState.cubelets[:]
        cubeState.rotateFace(face)
        cubeState.rotateFace(face)
        cubeState.rotateFace(face)
        cubeState.rotateFace(face)
        newCubelets = cubeState.cubelets[:]
        self.assertEqual(origCubelets, newCubelets)


class TestCubeAgent(unittest.TestCase):

    def search(self):
        cubeState = CubeState()
        cubeState.rotateFace('R')
        cubeState.rotateFace('U')
        cubeAgent = CubeAgent(cubeState)
        moveList = cubeAgent.solveCube()
        self.assertEqual([('U', -1, 0), ('R', -1, 0)], moveList)

    def testAndStoreRandomize(self):
        possibleMoves = ['R', 'L', 'U', 'D', 'F', 'B', 'r', 'l', 'u', 'd', 'f', 'b']
        cubeState = CubeState()

        stateList = []
        for _ in range(500):
            state = cubeState.cubelets
            for _ in range(20):
                state = cubeState.getRotatedCubelets(random.choice(possibleMoves), state)
            stateList.append(list(state))

        file = open("randomStateList", 'wb')
        pickle.dump(stateList, file)
        file.close()

    def testRuntineAve(self):
        cubeState = CubeState()
        file = open("randomStateList", 'rb')
        stateList = pickle.load(file)
        timeList = []
        for state in stateList:
            cubeState.cubelets = state
            tick = datetime.now()
            cubeAgent = CubeAgent(cubeState)
            moveList = cubeAgent.solveCube()
            tock = datetime.now()
            timeList.append((tock - tick).total_seconds())
        print('Average Runtime:')
        print(sum(timeList) / len(timeList))

    def testRuntimeSpread(self):
        cubeState = CubeState()
        file = open("randomStateList", 'rb')
        stateList = pickle.load(file)
        file.close()
        timeList = []
        visitedStatesList = []
        for state in stateList:
            cubeState.cubelets = state
            tick = datetime.now()
            cubeAgent = CubeAgent(cubeState)
            moveList = cubeAgent.solveCube()
            tock = datetime.now()
            timeList.append((tock - tick).total_seconds())
            visitedStatesList.append(cubeAgent.numVisitedStates)

        n, bins, patches = plt.hist(x=visitedStatesList, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Nodes Expanded', fontsize='20')
        plt.ylabel('Frequency', fontsize='20')
        plt.title('Frequency of the Number of Expanded Nodes', fontsize='20')
        maxfreq = n.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
        plt.show()
