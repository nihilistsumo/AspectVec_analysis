#!/usr/bin/python3

import sys, json, os, concurrent
from concurrent import futures
import numpy as np
from collections import Counter

def print_para_coverage(paras, asps, sorted_aspids, useful_aspids, c):
    para_coverage = []
    for a in asps:
        para_coverage.append(len(set(a).intersection(set(useful_aspids))))
    para_coverage.sort()
    print(str(len(paras)) + ":" + str(len(sorted_aspids)) + ":" + str(c) + ":" + str(para_coverage[:3]))

def convert_para(p, useful_aspids):
    para = paras_np[p]
    uvals = []
    for uasp in range(len(useful_aspids)):
        curr_asp = useful_aspids[uasp]
        if curr_asp in aspids_np[p]:
            uvals.append(aspvals_np[p][aspids_np[p].tolist().index(curr_asp)])
        else:
            uvals.append(0.0)
    np.save(outdir + "/global-para-vecs/" + para, np.array(uvals))

def convert_all_paras():
    # create frequency dictionary of asp ids
    # take top asps
    # create aspval matrix corresponding to top asps
    # do eigen analysis on top of that
    asps_freq = Counter(aspids_np.flatten())
    sorted_aspids = sorted(asps_freq, key=asps_freq.get, reverse=True)
    c = 0
    # k = only those asps will remain whose para-frequency is at least k% of len(paras)
    cut = len(paras_np)*k//100 + 1
    for sa in sorted_aspids:
        if asps_freq[sa] < cut:
            break
        c+=1
    useful_aspids = sorted_aspids[:c]
    print_para_coverage(paras_np, aspids_np, sorted_aspids, useful_aspids, c)
    print("Creating expanded data matrix")

    # for p in range(len(paras_np)):
    #     convert_para(p, useful_aspids)

    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(convert_para, p, useful_aspids) for p in range(len(paras_np))]
    concurrent.futures.wait(futures)

    # now useful_aspvals has asp values for each paras in row and each useful_asp in column
    return np.array(useful_aspids)

def usage():
    print("parameters: paras-file.npy aspids-file.npy aspvals-file.npy output-dir k(in %)")

if len(sys.argv) < 6:
    usage()
    sys.exit()

paras_file = sys.argv[1]
aspids_file = sys.argv[2]
aspvals_file = sys.argv[3]
outdir = sys.argv[4]
k = int(sys.argv[5])

paras_np = np.load(paras_file)
aspids_np = np.load(aspids_file)
aspvals_np = np.load(aspvals_file)
if os.path.isdir(outdir+"/global-para-vecs"):
    os.rmdir(outdir+"/global-para-vecs")
os.mkdir(outdir+"/global-para-vecs")
useful_asps = convert_all_paras()
np.save(outdir+"/global-aspids", useful_asps)
print("Done")