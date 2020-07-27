# Foundation of Big Data Analysis
Data mining algorithms implemented in python (+pyspark)

** add brief explanation for each part **
## 1. Finding potential friends (PySpark)
* Discover potential friends who have many mutual friends using a real dataset containing a LiveJournal friends graph.
* Algorithm
  1. 각 line을 (User, [list of friends])로 map
  2. User와 list of friend를 이용하여 직접 친구 관계인 두 명을 ((user, friend), 0)으로 flat map : real
  3. List of friends에 들어있는 사람들은 해당 User를 mutual friend로 두고 있으므로 List of friend 중에서 둘씩 조합하여 ((friend1, friend2), 1)로 flat map : potential
    - 2, 3번 과정에서 first user id가 second user id보다 작도록 정렬
  4. Potential friends이면서 real friends는 아닌 쌍을 찾기 위해 subtract by key 연산
  5. 남은 potential friends pair를 reduce by key를 통해 합치고 이때 value를 합산한다. i.e. ((user1, user2), 총 mutual friend의 수 = count)
  6. Count, user1, user2순으로 정렬하여 top-10 pair를 찾고 순서대로 print

* Run code
```bash
bin/spark-submit Finding_potential_friends.py path/to/soc-LiveJournal1Adj.txt
```

## 2. A-priori: Frequent item
## 3. LSH: Finding similar documents
## 4. K-means algorithm (PySpark)
## 5. Collaborative filtering
## 6. PageRank algorithm (PySpark)
## 7. Girvan-Newman algorithm (PySpark)
## 8. Gradient descent SVM algorithm
## 9. DGIM algorithm
