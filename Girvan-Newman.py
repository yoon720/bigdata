import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")


## preprocess
def makePApair(line):
    lst = map(int, line.split(','))
    return (lst[1], lst[2])  #(paper, author)
    
def makeEdge(papers):
    authors = list(set(papers[1]))  #deduplication, no order
    num = len(authors)
    edge = []
    # make combinations
    for i in range(num-1):
        for j in range(i+1, num):
            edge.append((authors[i], authors[j]))
            edge.append((authors[j], authors[i]))
    return edge

lines = sc.textFile(sys.argv[1])
header = lines.first()
rows = lines.filter(lambda x: x != header)
pair = rows.map(lambda row: makePApair(row))
papers = pair.groupByKey()
edges = papers.flatMap(makeEdge).distinct()
graph = edges.groupByKey().collectAsMap() #{author : list of connected authors}
authors = graph.keys()


## compute betweenness
def buildBFS(author):
    queue = []
    visited = []
    depth = {}
    shortest_path = {}
    reverse_tree = {}
    
    for a in authors:
        depth[a] = -1
    
    # root
    depth[author] = 0
    shortest_path[author] = 1
    reverse_tree[author] = []
    queue.append(author)

    # tree
    while queue:
        pre_node = queue.pop(0)
        visited.append(pre_node)
        for node in graph[pre_node]:
            if depth[node] == -1:  # never visited
                shortest_path[node] = 0
                reverse_tree[node] = []
                depth[node] = depth[pre_node] + 1
                queue.append(node)
            if depth[node] == depth[pre_node] + 1:
                shortest_path[node] += shortest_path[pre_node] # add new shortest paths
                reverse_tree[node].append(pre_node)
    
    return (visited, reverse_tree, shortest_path)
    
def getCredit(bfs_visited, bfs_reverse_tree, bfs_shortest_path):
    node_credit = {}
    edge_credit = {}

    for n in bfs_visited:
        node_credit[n] = 1.0

    while bfs_visited:
        child = bfs_visited.pop()
        for parent in bfs_reverse_tree[child]:
            credit = node_credit[child] * bfs_shortest_path[parent] / bfs_shortest_path[child]              # make ordered pair
            if parent < child:
                i, j = parent, child
            else:
                i, j = child, parent            
            # calculate credit
            edge_credit[(i,j)] = credit
            node_credit[parent] += credit
    return [(k, v) for (k, v) in edge_credit.items()]
    

bfs = sc.parallelize(authors).map(lambda a: buildBFS(a))
credits = bfs.flatMap(lambda b: getCredit(b[0], b[1], b[2]))
betweenness = credits.reduceByKey(lambda c1, c2: c1+c2).takeOrdered(10, key = lambda x: -x[1])

for ((u1, u2), b) in betweenness:
    print("%d\t%d\t%.5f" %(u1, u2, b/2))

sc.stop()
