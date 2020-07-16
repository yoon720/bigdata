import numpy as np
import sys

# function for measuring cosine distance
def cosDistance(m1, m2):
    len1 = sum([i**2 for i in m1.values()]) ** 0.5
    len2 = sum([i**2 for i in m2.values()]) ** 0.5
    dot = 0
    for j in m1.keys():
        if j in m2.keys():
            dot += m1[j]*m2[j]

    if len1==0 or len2 ==0:
        return 0
    else:
        return dot/(len1*len2)
    
def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


# utility matrix M
M = {}
f = open(sys.argv[1], 'r')
while True:
    line = f.readline()
    if not line:  break
        
    line = line.split(',')
    

    if int(line[0]) not in M.keys():
        M[int(line[0])] = {}
    M[int(line[0])][int(line[1])] = float(line[2])

f.close()

# test data
M_test = {}
f = open(sys.argv[2], 'r')
while True:
    line = f.readline()
    if not line:  break
        
    line = line.split(',')
    M_test[(int(line[0]),int(line[1]), line[3])] = 0
    
f.close()


# 1. user-based    
# normalize
Mu_norm = {}
for u in M.keys():
    Mu_norm[u] = {}
    user_avg = sum([i for i in M[u].values()]) / len(M[u].keys())
    for i in M[u].keys():
        Mu_norm[u][i] = M[u][i] - user_avg
        
# measure distance        
distance = {}
for u1 in M.keys():
    distance[u1] = {}
    for u2 in M.keys():
        if u1 != u2:
            distance[u1][u2] = cosDistance(Mu_norm[u1], Mu_norm[u2])

# find similar user and items
sim_user = {}
for u in M.keys():
    sim_user[u] = {}
    for w in sorted(distance[u], key=distance[u].get, reverse=True)[:330]:
        sim_user[u][w] = distance[u][w]
        
# compute ratings
rating = {}
for (u, i, t) in M_test.keys():
    #find users who have item i
    score, dist = [], []
    for (v, d) in sim_user[u].items():
        if i in M[v].keys():
            score.append(M[v][i])
            dist.append(d)

    if len(dist) == 0:
        user = [i for i in M[u].values()]
        rating[(u, i)] = sum(user)/len(user)

    else:
        rating[(u, i)] = np.matmul(score, np.transpose(softmax(dist)))        
        
            
# 2. item-based
# rearrange norm dictionary for item-based distance measure
Mi_norm = {}
for u in Mu_norm.keys():
    for i in Mu_norm[u].keys():
        if i not in Mi_norm.keys():
            Mi_norm[i] = {}
        Mi_norm[i][u] = Mu_norm[u][i]       
        
# measure distance                
distance2 = {}
for i1 in Mi_norm.keys():
    distance2[i1] = {}
    for i2 in Mi_norm.keys():
        if i1 != i2:
            distance2[i1][i2] = cosDistance(Mi_norm[i1], Mi_norm[i2])
                      
# find similar user and items
sim_item = {}
for i in Mi_norm.keys():
    sim_item[i] = {}
    for w in sorted(distance2[i], key=distance2[i].get, reverse=True)[:1240]:
        sim_item[i][w] = distance2[i][w]        
        
# compute ratings
rating2 = {}
for (u, i, t) in M_test.keys():
    if i not in sim_item.keys():
        user = [i for i in M[u].values()]
        rating2[(u, i)] = sum(user)/len(user)

    else:
        #find items which are rated by user u
        score, dist = [], []
        for (j, d) in sim_item[i].items():
            if j in M[u].keys():
                score.append(M[u][j])
                dist.append(d)

        if len(dist) == 0:
            user = [i for i in M[u].values()]
            rating2[(u, i)] = sum(user)/len(user)

        else:
            rating2[(u, i)] = np.matmul(score, np.transpose(softmax(dist)))  
                
                
# save avg of two ratings as result
for (u, i, t) in M_test.keys():
    M_test[(u, i, t)] = (rating[(u, i)]*2 + rating2[(u, i)]*5)/7
    
    
# save output file
f = open("./output.txt", 'w')

for (u, i, t), r in M_test.items():
    data = "%d,%d,%f,%s" %(u, i, r, t)
    f.write(data)

f.close()