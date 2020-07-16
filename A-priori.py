from itertools import combinations
import sys


#define a function for reading data
def readData(fdir):
    f = open(fdir, 'r')

    basket = []
    while True:
        line = f.readline()
        if not line: break
    
        basket.append(line.split(' ')[:-1])

    f.close()
    return basket


### PASS 1 ###
basket = readData(sys.argv[1])
                  
#make item list and corresponding count list with same index
items, counts = [], []

n = 0
for b in basket:
    for item in b:
        if item not in items:
            items.append(item)
            counts.append(0)
            counts[n] = 1
            n += 1
        else:
            id = items.index(item)
            counts[id] += 1


#find frequent items and print number of them
freq = []

for i in range(len(items)):
    if counts[i] >= 200:
        freq.append(items[i])

m = len(freq)        
print(m)


### PASS 2 ###
# make triangle list filled with 0
triangle = [0 for k in range(int(m*(m-1)/2))]
    
# find frequent items from basket(session)
# make pairs with them, and count
basket2 = readData(sys.argv[1])

for b in basket2:
    b_freq = []
    for item in b:
        if item in freq:
            b_freq.append(item)
    pairs = list(combinations(b_freq, 2))
    for p in pairs:
        index1 = freq.index(p[0])
        index2 = freq.index(p[1])
        [i, j] = sorted([index1, index2])
        k = int(i*(m-(i+1)/2)+j-i-1)
        triangle[k] += 1
        
            
#count the number of frequent pairs and print it
freq_pair = 0
for t in triangle:
    if t >= 200:
        freq_pair += 1

print(freq_pair)

            
#take top 10 counts 
top = sorted(triangle, key = lambda a: -a)[:10]


#find index(k) of each count and get user1(i), user2(j) using it.
for count in top:
    k = triangle.index(count)
    for i in range(m):
        if i*(m-(i+1)/2) <= k < (i+1)*(m-(i+2)/2):   
            user1 = i
            user2 = int(k - i*(m-(i+1)/2)+i+1)
            
            print("%s\t%s\t%d" %(freq[user1], freq[user2], triangle[k]))
