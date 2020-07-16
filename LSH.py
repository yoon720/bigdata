from itertools import combinations
import sys, re, random
import numpy as np


#read file and make (id,text) list
regex = re.compile('[^a-zA-Z ]')

f = open(sys.argv[1], 'r')
ids, texts = [], []

while True:
    line = f.readline()
    if not line: break
    id = line.split(' ')[0]
    ids.append(id)
    texts.append(regex.sub('',line[len(id)+1:].lower()))
f.close()


#find all unique shingles
shingles = set([])

for i in range(len(ids)):
    length = len(texts[i])
    for j in range(length-2):
        shingles.add(texts[i][j:j+3])

shingles = list(shingles)
row = len(shingles)


#make characteristic matrix
c_matrix = np.zeros((row,len(ids)), dtype=int)   #c_matrix[row, id]

for i in range(2000):
    for r in range(row):
        if shingles[r] in texts[i]:
            c_matrix[r, i] = 1
        
#find prime number
c = row

while True:
    isPrime = True
    
    for i in range(2,c):
        if (c % i) == 0:
            isPrime = False
            break
    
    if isPrime:
        break
    c += 1
    
#make hash function and value
h_matrix = np.zeros((row,120), dtype=int)   #h_matrix[row, hash]

for h in range(120):
    random.seed(h)
    a = random.randrange(0,c)
    b = random.randrange(0,c)
    for r in range(row):
        h_matrix[r, h] = (a*r+b)%c
        
        
#initialize minhash signature to 9999(inf)
minhash = np.empty((120, 2000), dtype = int)   #minhash[hash, id]
minhash.fill(9999)


#update minhash signature
for r in range(row):
    for i in range(len(ids)):
        if c_matrix[r][i]==1:
            for h in range(120):
                if minhash[h, i] > h_matrix[r, h]:
                    minhash[h, i] = h_matrix[r, h]
            
        
#find candidate pairs
pairs = list(combinations([i for i in range(2000)], 2))
candidate = set([])

for b in range(6):
    for i, j in pairs:
        if np.array_equal(minhash[b*20:(b+1)*20, i],minhash[b*20:(b+1)*20, j]):
            candidate.add((i,j))

            
#print the output
for i, j in candidate:
    print("%s\t%s" %(ids[i], ids[j]))
    
