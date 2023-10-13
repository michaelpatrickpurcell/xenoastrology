import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

alpha = 0.1
min_dist = 5
np.random.seed(2020)
ngroups=25
nppg = 6
npoints = ngroups*nppg
ibox_size = 10
ibox_offset= 45
points = ibox_offset + ibox_size*np.random.random(size=(npoints,2))

plt.figure()
for i in range(6):
    plt.scatter(points[nppg*i:nppg*(i+1),0], points[nppg*i:nppg*(i+1),1])


iter = 0
dist_mat = pdist(points)
while np.min(dist_mat) < min_dist:
    print(iter)
    updates = np.zeros(points.shape)
    for i,point in enumerate(points):
        diffs = point - points
        norms = np.linalg.norm(diffs, axis=1, keepdims=True)
        directions = np.nan_to_num(diffs/norms)
        forces = alpha * directions * np.nan_to_num(1/norms**(1))
        updates[i] = np.sum(forces, axis=0)

    points += updates
    dist_mat = pdist(points)
    iter += 1

plt.figure()
for i in range(6):
    plt.scatter(points[nppg*i:nppg*(i+1),0], points[nppg*i:nppg*(i+1),1])

plt.show()  
