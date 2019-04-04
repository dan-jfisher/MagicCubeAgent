import unittest
from CubeAgent.State import CubeState


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

    def testNTurns(self):
        cube1 = CubeState()
        cube2 = CubeState()

        cube1.rotateFace('R')
        cube1.rotateFace('R')

        cube2.rotateFaceByNTurns('R', 2)

        self.assertEqual(cube1.cubelets, cube2.cubelets)

    def turn360(self, face, cubeState):
        origCubelets = cubeState.cubelets[:]
        cubeState.rotateFace(face)
        cubeState.rotateFace(face)
        cubeState.rotateFace(face)
        cubeState.rotateFace(face)
        newCubelets = cubeState.cubelets[:]
        self.assertEqual(origCubelets, newCubelets)