import sys
from itertools import combinations
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)

#make a list of friends in integer
def flist(l):
    if u'' in l:
        return []
    else:
        return map(int, l)

# make a list of real friends pair
# returns ((p1, f1), 0)
def realF(pid, friends):
    real_list = []
    if len(friends) != 0: 
        for f in friends:
            real_list.append((tuple(sorted([pid, f])), 0))
    return real_list

# make combinations in friends list (potential pair)
# returns ((f1, f2), 1)
def potentialF(friends):
    if len(friends) == 0:
        return []
    else:
        pot_list = list(combinations(sorted(friends), 2))
        return [(p, 1) for p in pot_list]
    
    
lines = sc.textFile(sys.argv[1])
person = lines.map(lambda x: (int(x.split('\t')[0]), flist(x.split('\t')[1].split(','))))
real = person.flatMap(lambda p: realF(p[0], p[1]))
potential = person.flatMap(lambda p: potentialF(p[1]))

# remove real friends pairs from potential friends pairs
# and sum up the result by reduceByKey
sub = potential.subtractByKey(real).reduceByKey(lambda a, b: a+b)

# take top 10 pairs  
order = sub.takeOrdered(10, key = lambda x: (-x[1], x[0][0], x[0][1]))

for x in order:
    print"%d\t%d\t%d" %(x[0][0], x[0][1], x[1])


sc.stop()
