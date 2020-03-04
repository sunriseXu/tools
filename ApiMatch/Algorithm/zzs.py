from zss import simple_distance, Node

A = (
    Node("a")
        .addkid(Node("a")
            .addkid(Node("a"))
            .addkid(Node("a")
                .addkid(Node("a"))))
        .addkid(Node("a"))
    )
B = (
    Node("a")
        .addkid(Node("a")
            .addkid(Node("a"))
            .addkid(Node("a")
                .addkid(Node("a"))))
        
    )
# print(simple_distance(A, B))
def topN(myList,N,newElem):
    for idx in range(0,N):
        if newElem<myList[idx]:
            myInsert(myList,idx,newElem,N)
            break
    return myList
def myInsert(myList,idx,value,N):
    assert(idx>=0 and idx<N)
    for i in range(N-1,-1,-1):
        if i == idx:
            break
        myList[i] = myList[i-1]
    myList[idx] = value
    return myList
import random

myList = [100,100,100,100]

for i in range(0,100):
    newElem = random.randint(0,10)
    print(newElem)
    topN(myList,3,newElem)
    print(myList)
    input()