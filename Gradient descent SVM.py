import numpy as np
import sys

f = open(sys.argv[1], 'r')
features = []
while True:
    line = f.readline()
    if not line:  break
    features.append([int(i) for i in line[:-1].split(',')])
f.close()

f = open(sys.argv[2], 'r')
labels = []
while True:
    line = f.readline()
    if not line:  break
    labels.append(int(line))
f.close()

features = np.c_[np.array(features), np.ones(len(features))]  # add extra component +1
labels = np.array(labels)

avg = 0
acc = {}
epoch = 2500

numPoint, numFeatures = features.shape
eta = 0.0001
C = 0.1

for k in range(10):
   # k-fold
X = features[k * 600:(k + 1) * 600, :]
X_tr = np.delete(features, np.s_[k * 600:(k + 1) * 600], axis=0)

Y = labels[k * 600:(k + 1) * 600]
Y_tr = np.delete(labels, np.s_[k * 600:(k + 1) * 600])

w = np.ones(numFeatures)
acc[k] = {'train': [], 'test': []}

for n in range(epoch):
    # train
    mask = Y_tr * np.matmul(X_tr, w) < 1
    dL = np.matmul((mask * Y_tr), X_tr) * -1
    dF = w + C * dL
    w -= eta * dF

test = np.sum(np.equal(np.sign(np.matmul(X, w)), Y)) / 600
avg += test

print(avg / 10)
print(C)
print(eta)

