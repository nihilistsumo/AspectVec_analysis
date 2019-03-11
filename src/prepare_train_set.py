#!/usr/bin/python3

# Given test.triples file and all.triples file, this will create a train.triples in output directory
# where all the lines from all.triples will be included except those which has atleast one para that
# is present somewhere in test.triples. This will ensure no ground truth leakage.

import sys

def get_paras_set(triples):
    paras = set()
    with open(triples,'r') as n:
        for l in n:
            paras.add(l.split(" ")[1])
            paras.add(l.split(" ")[2])
            paras.add(l.split(" ")[3])
    return paras

test_triples = sys.argv[1]
all_triples = sys.argv[2]
output_dir = sys.argv[3]

test_paras = get_paras_set(test_triples)
all_paras = get_paras_set(all_triples)
train_set = []
with open(all_triples,'r') as a:
    for l in a:
        p1 = l.split(" ")[1]
        p2 = l.split(" ")[2]
        p3 = l.split(" ")[3]
        if p1 not in test_paras and p2 not in test_paras and p3 not in test_paras:
            train_set.append(l)
with open(output_dir+"/train.triples",'w') as out:
    for l in train_set:
        out.write(l)