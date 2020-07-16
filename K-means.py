import sys, re
from pyspark import SparkConf, SparkContext


# read text file
f = open(sys.argv[1], 'r')
points = []
while True:
    line = f.readline()
    if not line: break
    points.append([float(i) for i in re.split('[ \n]', line)[:-1]])
f.close()

# Euclidean distance
def distance(p1, p2):
    dist = 0
    for i in range(len(p1)):
        dist += (p1[i]-p2[i])**2
    return dist**0.5

# find initial k pooints
init = [0]
k = int(sys.argv[2])
for n in range(k-1):
    mindist = []
    for p in points:
        dist = []
        for i in init:
            dist.append(distance(p, points[i]))
        mindist.append(min(dist))
    init.append(mindist.index(max(mindist)))

# find the closest centroid and return its index
def findCluster(p):
    dist = 9999999  #large value
    for i in init:
        if dist > distance(p, points[i]):
            cluster = i
            dist = distance(p, points[i])
    return cluster

# find the farthest point pair in the cluster and return their distance as diameter
def diameter(p_list):
    d = 0
    for p1 in p_list:
        for p2 in p_list:
            if distance(p1, p2) > d:
                d = distance(p1, p2)
    return d
    
    
conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

lines = sc.textFile(sys.argv[1])
point = lines.map(lambda l: map(float,l.split()))
cluster = point.map(lambda p: (findCluster(p), p)).groupByKey()
diameter = cluster.map(lambda (k, p): diameter(p)).collect()

print(sum(diameter)/k)


sc.stop()