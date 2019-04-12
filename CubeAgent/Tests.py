import unittest
from datetime import datetime
from CubeAgent.State import CubeState
from CubeAgent.Agent import CubeAgent


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

    def testBfs(self):
        cubeState = CubeState()
        cubeState.rotateFace('R')
        cubeState.rotateFace('U')
        cubeAgent = CubeAgent(cubeState)
        moveList = cubeAgent.solveCube()
        self.assertEqual([('U', -1, 0), ('R', -1, 0)], moveList)

    def BfsRuntine(self):
        tick = datetime.now()
        cubeState = CubeState()
        cubeState.rotateFace('R')
        cubeState.rotateFace('U')
        cubeState.rotateFace('L')
        cubeState.rotateFace('F')
        cubeState.rotateFace('b')
        cubeAgent = CubeAgent(cubeState)
        moveList = cubeAgent.solveCube()
        tock = datetime.now()
        print(tock - tick)
