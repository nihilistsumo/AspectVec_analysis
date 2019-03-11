#!/usr/bin/python3
import sys, lucene, concurrent

def find_odd(l):
    p1 = l.split(" ")[1]
    p2 = l.split(" ")[2]
    p3 = l.split(" ")[3]
    odd_gt = l.split(" ")[4]

    simScore12 = scores[frozenset((p1,p2))]
    simScore13 = scores[frozenset((p1,p3))]
    simScore23 = scores[frozenset((p2,p3))]

    if simScore12 > simScore13:
        if (simScore12 > simScore23):
            odd = p3
        else:
            odd = p1
    else:
        if simScore13 > simScore23:
            odd = p2
        else:
            odd = p1
    if odd == odd_gt:
        return True
    else:
        return False


score_file = sys.argv[1]
triples_file = sys.argv[2]

correct = []
incorrect = []
scores = dict()
with open(score_file, 'r') as sf:
    for l in sf:
        p1 = l.split(" ")[0]
        p2 = l.split(" ")[1]
        score = float(l.split(" ")[2])
        scores[frozenset((p1,p2))] = score
print("done loading")
with open(triples_file, 'r') as tf:
    for l in tf:
        if find_odd(l):
            correct.append(l)
        else:
            incorrect.append(l)
print("Accuracy: "+str(len(correct)/(len(correct)+len(incorrect))))