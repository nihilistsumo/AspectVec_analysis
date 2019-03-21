#!/usr/bin/python3
import sys, lucene, concurrent

def find_odd(l):
    p1 = l.split(" ")[1]
    p2 = l.split(" ")[2]
    p3 = l.split(" ")[3]
    odd_gt = l.split(" ")[4]

    if frozenset((p1,p2)) in scores.keys() and frozenset((p1,p3)) in scores.keys() and frozenset((p2,p3)) in scores.keys():
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
            return True, 0
        else:
            return False, 0
    else:
        print("At least one pair of ("+p1+","+p2+","+p3+") is missing from scores file")
        return False, 1


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
missing_in_scores = 0
with open(triples_file, 'r') as tf:
    for l in tf:
        iscorrect, miss = find_odd(l)
        if iscorrect:
            correct.append(l)
        else:
            incorrect.append(l)
        missing_in_scores+=miss
print("Accuracy: "+str(len(correct)/(len(correct)+len(incorrect))))
print(str(missing_in_scores)+" entries missing in scores file")