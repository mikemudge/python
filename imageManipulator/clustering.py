#!/usr/bin/env python

import random
import numpy as np
from PIL import Image

def manipulate():
    myimage = Image.open('color-medium.jpg')
    myimage.load()

    arr = np.array(myimage)
    # arr.shape 120, 160, 3

    # How many clusters we want.
    k = 32

    # Iterate pixels and assign them to their closest cluster.
    # Then update clusters to be the averate of their assigned pixels.
    # Repeat until no pixels are reassigned to a new cluster or x iterations?

    # TODO load image width and height?
    (height, width, _) = arr.shape
    print width, height
    # Assign to a random cluster initially.
    assignedCluster = [[random.randint(0, k - 1) for x in range(width)] for y in range(height)]

    for i in range(20):
        clusters = updateClusters(assignedCluster, arr, k)
        reassignedCount = assignToClusters(clusters, arr, assignedCluster)
        print i, reassignedCount, 'changed cluster'
        if reassignedCount == 0:
            break

    # Update pixels to be the color of their closest cluster.
    for x in range(width):
        for y in range(height):
            c = clusters[assignedCluster[y][x]]
            arr[y][x] = (c[0], c[1], c[2])

    output = Image.fromarray(arr)
    output.save("output.jpg")
    output.show()

def updateClusters(assignedCluster, arr, k):
    # Update clusters to be the average of all pixels assigned to them.
    clusterAverage = [np.array([0, 0, 0]) for i in range(k)]
    clusterCount = [0 for i in range(k)]
    xAverage = [0 for i in range(k)]
    yAverage = [0 for i in range(k)]
    (height, width, _) = arr.shape
    for x in range(width):
        for y in range(height):
            pixelClusterIndex = assignedCluster[y][x]
            clusterCount[pixelClusterIndex] += 1
            clusterAverage[pixelClusterIndex] += arr[y][x]
            xAverage[pixelClusterIndex] += x
            yAverage[pixelClusterIndex] += y

    clusters = [(clusterAverage[i] / clusterCount[i]) if clusterCount[i] > 0 else np.array(randomColor()) for i in range(k)]
    for i in range(k):
        if clusterCount[i] > 0:
            clusters[i] = (clusters[i][0], clusters[i][1], clusters[i][2], xAverage[i] / clusterCount[i], yAverage[i] / clusterCount[i])
        else:
            clusters[i] = randomColor() + (width / 2, height / 2)
        # The color and the number assigned to each cluster.
        # print str(clusters[i]), clusterCount[i]
    return clusters

def randomColor():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

def assignToClusters(clusters, arr, assignedCluster):
    # Update pixels to be the color of their closest cluster.
    changed = 0
    (height, width, _) = arr.shape
    for x in range(width):
        for y in range(height):
            cluster = closestCluster(np.array(tuple(arr[y][x]) + (x, y)), clusters)
            # TODO did this change?
            if assignedCluster[y][x] != cluster:
                changed += 1
            assignedCluster[y][x] = cluster
    return changed

def closestCluster(pixel, options):
    minDis = np.linalg.norm(pixel - options[0])
    best = 0
    for i, cluster in enumerate(options):
        # dis = np.linalg.norm(pixel - cluster)
        dis = sum(abs(pixel - cluster))
        if dis < minDis:
            best = i
            minDis = dis
    return best

if __name__ == '__main__':
    manipulate()
