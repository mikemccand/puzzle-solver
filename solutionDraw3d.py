import sys
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']

pieces = [
        np.array([[0,3,1], [0,0,0], [0,0,1], [0,3,0], [3,2,0], [3,2,2], [0,3,2], [1,2,0], [2,2,0], [1,0,0], [1,3,0], [3,2,1], [1,1,0]]),
        np.array([[3,3,1], [2,3,3], [2,2,3], [1,2,3], [3,3,2], [3,2,3], [2,3,2], [3,3,3], [2,2,2]]),
        np.array([[3,1,2], [3,1,3], [3,0,3], [2,1,3], [3,0,2], [3,1,1], [1,1,3], [1,1,2]]),
        np.array([[0,3,3], [0,2,3], [1,0,3], [1,3,1], [1,3,2], [1,3,3], [0,1,3], [0,0,3]]),
        np.array([[2,1,2], [2,0,1], [2,0,2], [2,0,3], [2,0,0], [3,0,1]]),
        np.array([[2,1,0], [3,0,0], [1,1,1], [2,1,1], [3,1,0], [1,2,1]]),
        np.array([[0,2,1], [0,1,0], [1,2,2], [0,2,2], [0,2,0]]),
        np.array([[1,0,1], [0,1,2], [0,0,2], [0,1,1], [1,0,2]]),
        np.array([[2,3,0], [3,3,0], [2,3,1], [2,2,1]]),
        ]

check = set()
for pc in pieces:
    for p in pc:
        tp = tuple(p)
        if tp not in check:
            check.add(tp)
        else:
            print(p)
            sys.exit(1)


# Create a 3D scatter plot of the points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
k = 8
if len(sys.argv) != 1:
    k = int(sys.argv[1])

for i in range(0, k):
    c = colors[i]
    points = pieces[i]
    marker = "s"
    if i == k - 1:
        marker = "o"
    ax.scatter(points[:,0], points[:,1], points[:,2], s = 100, c=c, marker=marker)

ax.set_xlim3d(0, 4)
ax.set_ylim3d(0, 4)
ax.set_zlim3d(0, 4)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
