import sys


# compute the utility matrix M
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
for u in M.keys():
    if u != 600:
        distance[u] = cosDistance(Mu_norm[u], Mu_norm[600])
        
# find similar users
sim_user = []
for w in sorted(distance, key=distance.get, reverse=True)[:10]:
    sim_user.append(w)

# calculate rating and print
rating = {}
for i in range(1, 1001):
    count = 0
    s = 0
    for u in sim_user:
        if i in M[u].keys():
            count += 1
            s += M[u][i]
    if count == 0:
        rating[i] = 0
    else:
        rating[i] = s/count

top5 = sorted(rating.items(), key=lambda x: (-x[1], x[0]))[:5]
for t in top5:
    print("%d\t%.1f" %(t[0], t[1]))
    
    
    
# 2. item-based
# rearrange norm dictionary for distance measure
Mi_norm = {}
for u in Mu_norm.keys():
    for i in Mu_norm[u].keys():
        if i not in Mi_norm.keys():
            Mi_norm[i] = {}
        Mi_norm[i][u] = Mu_norm[u][i]       
        
# measure distance                
distance2 = {}
for i1 in range(1, 1001):
    if i1 in Mi_norm.keys():
        distance2[i1] = {}
        for i2 in Mi_norm.keys():
            if i2 != i1:
                distance2[i1][i2] = cosDistance(Mi_norm[i1], Mi_norm[i2])
                
# find similar items for each items
sim_item = {}
for i in range(1, 1001):
    if i in Mi_norm.keys():
        sim_item[i] = [w for w in sorted(distance2[i], key=distance2[i].get, reverse=True)[:10]]
        
# calculate rating and print
rating = {}
for i in range(1, 1001):
    if i in Mi_norm.keys():
        count = 0
        s = 0
        for j in sim_item[i]:
            if j in M[600].keys():
                count += 1
                s += M[600][j]
            if count == 0:
                #print(0)
                rating[i] = 0
            else:
                #print(count, sum/count)
                rating[i] = s/count

top5 = sorted(rating.items(), key=lambda x: (-x[1], x[0]))[:5]
for t in top5:
    print("%d\t%.1f" %(t[0], t[1]))