"""
Agent that solves a rubix cube provided to it and returns the moves it used
Written by Daniel Fisher
Uses code written by Jake Vanderplas and David Hogg for cube simulation
    https://github.com/davidwhogg/MagicCube
"""

from Cube.cube_interactive import Cube as Cube
import numpy as np
import matplotlib.pyplot as plt


class CubeAgent:

    def __init__(self, cube):
        self.cube = cube

    def rotateFace(self, face, turn=1, layer=0):
        self.cube.rotate_face(face, turn, layer)

    def solveCube(self):
        self.rotateFace('R', -1, 0)

    def isFaceSolved(self, faceColors):
        firstColor = faceColors[0]
        for color in faceColors:
            if color != firstColor:
                return False
        return True

    def isCubeSolved(self):
        colors = self.cube.getColors()

        cubeColors = np.split(colors, 6)
        for faceColors in cubeColors:
            if not self.isFaceSolved(faceColors):
                return False
        return True


if __name__ == '__main__':
    cube = Cube(3)
    # cube.rotate_face('R')

    cubeAgent = CubeAgent(cube)
    if cubeAgent.isCubeSolved():
        cube.draw_interactive()
        plt.show()
