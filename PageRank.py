import sys
from pyspark import SparkConf, SparkContext


conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

def makeM(spair):
    src = spair[0]
    dlist = list(set(spair[1]))   #deduplication
    l = len(dlist)
    return [(d, src, 1.0/l) for d in dlist]


#  make M
lines = sc.textFile(sys.argv[1])
pair = lines.map(lambda l: map(int, l.split('\t')))  #(src, dest)
spair = pair.groupByKey()
M = spair.flatMap(makeM)


# compute pagerank
beta = 0.9
N = 1000
v = [1.0/N for i in range(N)]
 
# 50 iteration
for i in range(50):

    # matrix vector multiplication
    v_rdd = M.map(lambda (d, s, pr): (d, pr*v[s-1]))\
            .reduceByKey(lambda v1, v2: v1+v2).collect()

    # update score
    for (dest, score) in v_rdd:
        v[dest-1] = beta*score + (1.0-beta)/N

# make (page, score) pair
result = [(p+1, score) for (p, score) in enumerate(v)]

# print output
for (p, score) in sorted(result, key = lambda r: -r[1])[:10]:
    print("%d\t%.5f" %(p, score))


sc.stop()
