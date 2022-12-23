import os
import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QSize

def path(arr, s, t):
    temp = [t]
    i = t
    while arr[i] != -9999:
        temp.append(arr[i])
        i = arr[i]
    return temp[::-1]

def find_bottleneck(G, arr):
    min_val = np.inf
    for i in range(1, len(arr)):
        start, end = arr[i - 1], arr[i]
        if G[start][end] < min_val:
            min_val = G[start][end]
    return min_val


def augment(G1, short_path, bottleneck_edge):
    for i in range(1, len(short_path)):
        start, end = short_path[i - 1], short_path[i]
        G1[start][end] -= bottleneck_edge
        G1[end][start] += bottleneck_edge
    return G1


def edmonds_karp(G, s, t):
    flow = 0
    paths = []
    source, sink = s, t
    g = G
    nodes, predecessor = breadth_first_order(csr_matrix(g), 0, directed=True, return_predecessors=True)
    shortest_path = path(predecessor, source, sink)
    while source in shortest_path:
        paths.append(shortest_path)
        bottleneck_edge = find_bottleneck(g, shortest_path)
        flow += bottleneck_edge
        g = augment(g, shortest_path, bottleneck_edge)
        nodes, predecessor = breadth_first_order(csr_matrix(g), 0, directed=True, return_predecessors=True)
        shortest_path = path(predecessor, source, sink)
    return flow, paths


def escape(d, st):
    # Total number of nodes = d * d * 2 + 2
    g = d * d * 2 + 2
    x1 = np.zeros((g, g), dtype=np.int)

    # Vin-Vout edges changed to 1
    for j in range(1, d * d * 2, 2):
        x1[j][j + 1] = 1

    # Border to Sink
    # Upper + Lower
    for j in range(1, d + 1):
        x1[2 * j][g - 1] = 1
        x1[2 * (d - 1) * d + 2 * j][g - 1] = 1
    # left + right
    for j in range(d):
        x1[j * 2 * d + 2][g - 1] = 1
        x1[2 * d * (j + 1)][g - 1] = 1

    # Source to given vertices
    # S to Vin
    for l in st:
        x1[0][(l[0] - 1) * 2 * d + (2 * (l[1] - 1)) + 1] = 1
    # From each vertex to its neighbours
    # Right
    for l in range(2, d * d * 2 + 1, 2):
        if l % (2 * d) != 0:
            x1[l][l + 1] = 1
            # x[l + 2][l - 1] = 1
    # Left
    for l in range(2, d * d * 2 + 1, 2):
        if (l - 2) % (2 * d) != 0:
            x1[l][l - 3] = 1
    # Up
    for l in range(2, d * d * 2 + 1, 2):
        if l - (2 * d) > 0:
            x1[l][l - (2 * d) - 1] = 1
    # Down
    for l in range(2, d * d * 2 + 1, 2):
        if l + (2 * d) < d * d * 2 + 1:
            x1[l][l + (2 * d) - 1] = 1
    max_flow, paths = edmonds_karp(x1, 0, g - 1)
    return max_flow, paths


# pyqt UI
class MyApp(QWidget):
    def __init__(self, grid_dimension, start_vertices, path):
        super().__init__()
        self.grid_dimension = grid_dimension
        self.start_vertices = start_vertices
        self.path = path
        self.initUI()

    def initUI(self):
        self.setFixedSize(QSize(grid_dimension * 50 + 50, grid_dimension * 50 + 50))
        self.setWindowTitle('escape-problem')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        # draw a 9*9 grid
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        for i in range(grid_dimension):
            qp.drawLine(50, 50 + 50 * i, grid_dimension * 50, 50 + 50 * i)
            qp.drawLine(50 + 50 * i, 50, 50 + 50 * i, grid_dimension * 50)
        # draw white vertices
        qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        for i in range(grid_dimension):
            for j in range(grid_dimension):
                qp.drawEllipse(40 + 50 * i, 40 + 50 * j, 20, 20)
        # draw paths
        qp.setPen(QPen(Qt.blue, 7, Qt.SolidLine))
        for path in paths:
            prev = 0
            for vertice in path[1:-1:2]:
                if (prev != 0):
                    qp.drawLine(50 + 50 * ((prev // 2) // grid_dimension),
                                50 + 50 * ((prev // 2) % grid_dimension),
                                50 + 50 * ((vertice // 2) // grid_dimension),
                                50 + 50 * ((vertice // 2) % grid_dimension))
                prev = vertice
        # draw black vertices (start_vertices)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        for start in start_vertices:
            qp.drawEllipse(40 + 50 * (start[0] - 1), 40 + 50 * (start[1] - 1), 20, 20)


if __name__ == '__main__':
    l = []
    file_path = os.path.join(os.curdir, "data.txt")
    with open(file_path) as f:
        for line in f:
            l.append((map(int, line.strip().split())))

    g1, g2, tc = l[0]
    grid_dimension = g1

    if g1 != g2:
        print("Not a square grid")
    else:
        start_vertices = []
        for k in range(tc):
            x, y = l[k + 1]
            start_vertices.append((x, y))
        # print start_vertices
        final_flow, paths = escape(grid_dimension, start_vertices)
        print("Max Flow :", final_flow)
        print("Start Point :", tc)
        print("Result : possible" if final_flow == len(start_vertices) else "Result : impossible")

    app = QApplication(sys.argv)
    ex = MyApp(grid_dimension, start_vertices, paths)
    sys.exit(app.exec_())
