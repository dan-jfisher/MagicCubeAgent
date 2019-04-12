from Cube.cube_interactive import Cube as InteractiveCube
from CubeAgent.State import *
import matplotlib.pyplot as plt
import heapq
from CubeAgent.Heuristic import Heuristic


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class CubeAgent:
    possibleMoves = ['R', 'L', 'U', 'D', 'F', 'B']

    def __init__(self, cube):
        self.cube = cube
        self.moves = []
        self.heuristic = Heuristic()

    def rotateFace(self, face, turn=1, layer=0):
        self.cube.rotateFace(face, turn, layer)

    def solveCube(self):
        visitedStates = set()
        frontier = PriorityQueue()
        frontier.push((self.cube.cubelets[:], [], 0), 0)

        while not frontier.isEmpty():
            state, path, cost = frontier.pop()
            if self.isCubeSolved(state):
                return path
            if tuple(state) not in visitedStates:
                visitedStates.add(tuple(state))
                successors = [(self.cube.getDirectionallyRotatedCubelets(face, state, direction),
                               path + [(face, direction, 0)], cost + 1)
                              for face in self.possibleMoves for direction in [1, -1]]
                for successorState, path, newCost in successors:
                    frontier.push((successorState, path, newCost),
                                  newCost + self.heuristic.heuristicLookup(successorState))

    def isCubeSolved(self, cubelets):
        return cubelets == CubeState.solvedCubelets


if __name__ == '__main__':
    cube = InteractiveCube(2)
    cube.randomize(20)

    cubeState = CubeState()
    randomMoveList = cube.getMoveList()
    print(randomMoveList)
    for move in randomMoveList:
        face, dir, depth = move
        cubeState.rotateFace(face, dir)

    cubeAgent = CubeAgent(cubeState)
    solutionMoveList = cubeAgent.solveCube()
    print(solutionMoveList)

    cube.draw_interactive(solutionMoveList)
    plt.show()
