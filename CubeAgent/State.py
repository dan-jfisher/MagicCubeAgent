"""
Agent that solves a rubix cube provided to it and returns the moves it used
Written by Daniel Fisher
Uses code written by Jake Vanderplas and David Hogg for cube simulation
    https://github.com/davidwhogg/MagicCube
"""

from Cube.cube_interactive import Cube as InteractiveCube
import numpy as np
import matplotlib.pyplot as plt
import copy
import collections

# Location = collections.namedtuple("Location", field_names=['pos', 'ort'])

solvedCublets = [
            # top layer
            ((0, 2), 0),
            ((0, 3), 0),
            ((0, 1), 0),
            ((0, 0), 0),
            # bottom layer
            ((5, 0), 1),
            ((5, 1), 1),
            ((5, 3), 1),
            ((5, 2), 1)
        ]

rightTransforms = {
    0: (3, {1: 1, 2: 2}),
    1: (0, {1: 1, 2: 2}),
    2: (2, {0: 1, 1: 2, 2: 3, 3: 0}),
    3: (5, {1: 1, 2: 2}),
    4: (),
    5: (1, {1: 1, 2: 2}),
}

leftTransforms = {
    0: (1, {1: 1, 2: 2}),
    1: (5, {1: 1, 2: 2}),
    2: (),
    3: (0, {1: 1, 2: 2}),
    4: (4, {0: 1, 1: 2, 2: 3, 3: 0}),
    5: (3, {1: 1, 2: 2}),
}

UpTransforms = {
    0: (0, {0: 1, 1: 2, 2: 3, 3: 0}),
    1: (4, {0: 1, 1: 2}),
    2: (1, {0: 1, 3: 0}),
    3: (2, {2: 3, 3: 0}),
    4: (3, {1: 2, 2: 3}),
    5: ()
}

DownTransforms = {
    0: (),
    1: (2, {2: 1, 3: 2}),
    2: (3, {1: 0, 2: 1}),
    3: (4, {0: 3, 1: 0}),
    4: (1, {0: 3, 3: 2}),
    5: (5, {0: 1, 1: 2, 2: 3, 3: 0})
}

FrontTransforms = {
    0: (2, {3: 3, 2: 2}),
    1: (1, {0: 1, 1: 2, 2: 3, 3: 0}),
    2: (5, {2: 0, 3: 1}),
    3: (),
    4: (0, {1: 2, 2: 3}),
    5: (4, {0: 1, 1: 2}),
}

BackTransforms = {
    0: (4, {0: 0, 1: 1}),
    1: (),
    2: (0, {0: 0, 1: 1}),
    3: (3, {0: 1, 1: 2, 2: 3, 3: 0}),
    4: (5, {0: 2, 1: 3}),
    5: (2, {2: 0, 3: 1})
}

TransformDicts = {
    'R': rightTransforms,
    'L': leftTransforms,
    'U': UpTransforms,
    'D': DownTransforms,
    'F': FrontTransforms,
    'B': BackTransforms
}


class CubeState:

    def __init__(self):
        self.cubelets = copy.deepcopy(solvedCublets)
        self.transoformDicts = dict(TransformDicts)
        # create and store inverse transformations
        for faceKey, transforms in TransformDicts.items():
            inverseFaceKey = faceKey.lower()
            inverseTransforms = {}
            for key, transform in transforms.items():
                if transform:
                    fromPos = transform[0]
                    toPos = key
                    inverseDict = {}
                    for fromOrt, toOrt in transform[1].items():
                        inverseDict[toOrt] = fromOrt
                    inverseTransforms[fromPos] = (toPos, inverseDict)
                else:
                    inverseTransforms[key] = ()
            self.transoformDicts[inverseFaceKey] = inverseTransforms

    def rotateFace(self, face):
        for index, cubelet in enumerate(self.cubelets):
            transformDict = self.transoformDicts[face]
            loc, color = cubelet
            # assert isinstance(loc, Location)
            transform = transformDict[loc[0]]
            if transform:
                if loc[1] in transform[1]:
                    pos = transform[0]
                    ort = transform[1][loc[1]]
                    self.cubelets[index] = ((pos, ort), color)

    def rotateFaceByNTurns(self, face, numTurns):
        face = face.swapcase() if numTurns < 0 else face
        for i in range(0, abs(numTurns)):
            self.rotateFace(face)


class CubeAgent:

    def __init__(self, cube):
        self.cube = cube
        self.moves = []

    def rotateFace(self, face, turn=1, layer=0):
        self.cube.rotateFace(face, turn, layer)

    def solveCube(self):
        # self.cube.rotateFace()

        if self.isCubeSolved():
            return []
        else:
            return 'F', 1, 0

    def isCubeSolved(self):
        return self.cube.cubelets == solvedCublets


if __name__ == '__main__':
    cube = InteractiveCube(2)
    cube.randomize(3)

    cubeState = CubeState()
    randomMoveList = cube.getMoveList()

    cubeAgent = CubeAgent(cubeState)
    moveList = cubeAgent.solveCube()

    cube.draw_interactive(moveList)
    plt.show()
