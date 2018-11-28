import copy
import heapq
import sys


class PathFinding(object):
    graph = []
    start = -1
    end = -1
    tmp = []
    m = {}

    def __init__(self, maze):
        self.tmp = copy.deepcopy(maze)
        count = 2
        for i in range(len(self.tmp)):
            for j in range(len(self.tmp[i])):
                if self.tmp[i][j] != 1:
                    self.m[count] = (i, j)
                    self.tmp[i][j] = count
                    count += 1

        for i in range(count):
            self.graph.append([])
        for i in range(len(self.tmp)):
            for j in range(len(self.tmp[i])):
                if self.tmp[i][j] != 1:
                    if i - 1 >= 0 and self.tmp[i - 1][j] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i - 1][j])
                    if j - 1 >= 0 and self.tmp[i][j - 1] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i][j - 1])
                    if i + 1 < len(self.tmp) and self.tmp[i + 1][j] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i + 1][j])
                    if j + 1 < len(self.tmp[i]) and self.tmp[i][j + 1] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i][j + 1])
        print self.tmp

    def setStartEnd(self, maze):
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 2:  # start
                    self.start = self.tmp[i][j]
                elif maze[i][j] == 3:  # target
                    self.end = self.tmp[i][j]

    def countDist(self, x, y):
        '''
        manhattan distance as the estimate function
        :param coordinate:
        :param x:
        :param y:
        :return:
        '''
        tx = abs(self.m[x][0] - self.m[y][0])
        ty = abs(self.m[x][1] - self.m[y][1])
        return tx + ty

    @staticmethod
    def nodeToCoordinate(coordinate, x):
        return coordinate[x][0], coordinate[x][1]

    @staticmethod
    def coordinateToNode(x, y):
        '''
        still wonder how to do this
        :param x:
        :param y:
        :return:
        '''
        return None

    def aStar(self):
        s = self.start
        t = self.end
        father = [-1] * len(self.graph)
        path = []
        d = [sys.maxsize] * len(self.graph)
        d[s] = 0
        heap = [[d[s], s]]  # A*
        visited = set()
        while heap:
            while heap:
                tmp = heapq.heappop(heap)
                now = tmp[1]
                if now not in visited:
                    break
            if now in visited:
                break
            visited.add(now)
            if now == t:
                break
            for i in self.graph[now]:
                if d[now] + 1 < d[i]:
                    father[i] = now
                    d[i] = d[now] + 1
                    heapq.heappush(heap, [d[i] + self.countDist(i, t) * 0.3, i])  # A*
        i = t
        while i != -1:
            path.insert(0, i)
            i = father[i]

        # change node number to coordinate
        # for i in range(len(path)):
        #     path[i] = PathFinding.nodeToCoordinate(coordinate, path[i])
        return path


# maze will be a size of 65*40
# Testing

g = [[1, 4, 5], [0, 4, 5, 6, 2, 13], [1, 5, 6, 7, 3], [2, 6, 7], [4, 9], [1, 2, 4], [], [3, 2], [4, 5, 9, 12],
     [5, 8, 13, 10], [15], [], [], [], [], []]
cood = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3], [3, 0], [3, 1],
        [3, 2], [3, 3]]
maze = [[2, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 3]]
print maze
p = PathFinding(maze)
print p.graph
p.setStartEnd(maze)
print p.aStar()
# print PathFinding.aStar(g, cood, 0, 15)
