"""
Agent that solves a rubix cube provided to it and returns the moves it used
Written by Daniel Fisher
Uses code written by Jake Vanderplas and David Hogg for cube simulation
    https://github.com/davidwhogg/MagicCube
"""

import numpy as np
import copy
import collections

# Location = collections.namedtuple("Location", field_names=['pos', 'ort'])

rightTransforms = {
    0: (3, {1: 1, 2: 2}),
    1: (0, {1: 1, 2: 2}),
    2: (2, {0: 1, 1: 2, 2: 3, 3: 0}),
    3: (5, {1: 1, 2: 2}),
    4: (),
    5: (1, {1: 1, 2: 2}),
}

leftTransforms = {
    0: (1, {0: 0, 3: 3}),
    1: (5, {0: 0, 3: 3}),
    2: (),
    3: (0, {0: 0, 3: 3}),
    4: (4, {0: 1, 1: 2, 2: 3, 3: 0}),
    5: (3, {0: 0, 3: 3}),
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

# FrontTransforms = {
#     0: (2, {3: 3, 2: 2}),
#     1: (1, {0: 1, 1: 2, 2: 3, 3: 0}),
#     2: (5, {2: 0, 3: 1}),
#     3: (),
#     4: (0, {1: 2, 2: 3}),
#     5: (4, {0: 1, 1: 2}),
# }

FrontTransforms = {
    0: (2, {3: 3, 2: 2}),
    1: (1, {0: 1, 1: 2, 2: 3, 3: 0}),
    2: (5, {2: 0, 3: 1}),
    3: (),
    4: (0, {2: 2, 3: 3}),
    5: (4, {0: 2, 1: 3}),
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
    solvedCubelets = [
        # top layer
        (0, 2),
        (0, 3),
        (0, 1),
        (0, 0),
        # bottom layer
        (5, 0),
        (5, 1),
        (5, 3),
        (5, 2)
    ]

    def __init__(self):
        self.cubelets = self.solvedCubelets[:]
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

    def getRotatedCubelets(self, face, cubelets):
        newCubelets = list(cubelets)
        for index, loc in enumerate(cubelets):
            transformDict = self.transoformDicts[face]
            # assert isinstance(loc, Location)
            transform = transformDict[loc[0]]
            if transform:
                if loc[1] in transform[1]:
                    pos = transform[0]
                    ort = transform[1][loc[1]]
                    newCubelets[index] = (pos, ort)
        return newCubelets

    def rotateFace(self, face, dir=1):
        for i in range(abs(dir)):
            self.cubelets = self.getDirectionallyRotatedCubelets(face, self.cubelets, dir)

    def getDirectionallyRotatedCubelets(self, face, cubelets, dir):
        face = face.swapcase() if dir < 0 else face
        return self.getRotatedCubelets(face, cubelets)
