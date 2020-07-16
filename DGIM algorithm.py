import sys

#read stream
f = open(sys.argv[1], 'r')
window = []
while True:
    line = f.readline()
    if not line:  break
    window.append(int(line))
f.close()

# make bucket
size = 1
bucket = {1 : []}
for i in range(len(window)):
    if window[i] == 1:
        bucket[1].append((i, i))

    # update buckets
    if len(bucket[1]) == 3: 
        test_size = 1
        while test_size <= size:                
            if len(bucket[test_size]) == 3:
                if test_size*2 not in bucket.keys():
                    bucket[test_size*2] = []
                    size *= 2
                bucket[test_size*2].append((bucket[test_size].pop(0)[0],bucket[test_size].pop(0)[1]))
                
            test_size *= 2   
            
# calculate number of bits
bucket_list = []
for i in bucket.keys():
    for j in reversed(range(len(bucket[i]))):
        bucket_list.append((i, j))

for k in sys.argv[2:]:
    if k == '0':
        print(0)
        
    else:
        bit = 0
        position = 10000000 - int(k)
        
        for b in bucket_list:
            start, end = bucket[b[0]][b[1]]
            if position <= end:
                index = bucket_list.index(b)        
    
        for n in bucket_list[:index]:
            bit += n[0]
        bit += bucket_list[index][0]/2    
        
        print(bit)
