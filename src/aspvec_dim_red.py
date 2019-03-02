#!/usr/bin/python3

import sys, json, os
import numpy as np
from collections import Counter

def print_para_coverage(paras, asps, sorted_aspids, useful_aspids, c):
    para_coverage = []
    for a in asps:
        para_coverage.append(len(set(a).intersection(set(useful_aspids))))
    para_coverage.sort()
    print(str(len(paras)) + ":" + str(len(sorted_aspids)) + ":" + str(c) + ":" + str(para_coverage[:3]))

# should do this eigen analysis per page instead of the whole dataset
def get_useful_aspval_mat(paras, asps, aspvals):
    # create frequency dictionary of asp ids
    # take top asps
    # create aspval matrix corresponding to top asps
    # do eigen analysis on top of that
    asps_freq = Counter(np.array(asps).flatten())
    sorted_aspids = sorted(asps_freq, key=asps_freq.get, reverse=True)
    c = 0
    # k = (cut*100)/(len(paras), k% of lower asps will be discarded
    cut = len(paras)//10 + 1
    for sa in sorted_aspids:
        if asps_freq[sa] < cut:
            break
        c+=1
    useful_aspids = sorted_aspids[:c]
    #print_para_coverage(paras, asps, sorted_aspids, useful_aspids, c)
    useful_aspvals = []
    for p in range(len(paras)):
        uvals = []
        for uasp in range(len(useful_aspids)):
            curr_asp = useful_aspids[uasp]
            if curr_asp in asps[p]:
                uvals.append(aspvals[p][asps[p].tolist().index(useful_aspids[uasp])])
            else:
                uvals.append(0.0)
        useful_aspvals.append(uvals)
    # now useful_aspvals has asp values for each paras in row and each useful_asp in column
    return useful_aspvals

def eigen_analysis(data_matrix):
    means = np.mean(data_matrix.T, axis=1)
    cent_data = data_matrix - means
    cov_cent_data = np.cov(cent_data.T)
    vals, vecs = np.linalg.eig(cov_cent_data)
    proj_data = vecs.T.dot(cov_cent_data.T)
    return proj_data, vals, vecs

def usage():
    print("parameters: art-qrels paras-file.npy aspids-file.npy aspvals-file.npy output-dir")


if len(sys.argv) < 6:
    usage()
    sys.exit()
art_qrels = sys.argv[1]
paras_file = sys.argv[2]
aspids_file = sys.argv[3]
aspvals_file = sys.argv[4]
outdir = sys.argv[5]
page_para_dict = dict()
with open(art_qrels,'r') as art:
    for line in art:
        page = line.split(" ")[0]
        para = line.split(" ")[2]
        if page in page_para_dict.keys():
            page_para_dict[page].append(para)
        else:
            page_para_dict[page] = [para]
paras_np = np.load(paras_file)
aspids_np = np.load(aspids_file)
aspvals_np = np.load(aspvals_file)
for page in page_para_dict.keys():
    page_paras = page_para_dict[page]
    page_aspids = []
    page_aspvals = []
    for para in page_paras:
        page_aspids.append(aspids_np[paras_np.tolist().index(para)])
        page_aspvals.append(aspvals_np[paras_np.tolist().index(para)])
    aspval_matrix = get_useful_aspval_mat(page_paras, page_aspids, page_aspvals)
    print("Going to do eigen analysis of "+str(len(page_paras))+" paras in Page: "+page)
    proj_data, eigvals, eigvecs = eigen_analysis(np.array(aspval_matrix))
    eigen_data = np.array([page_paras, proj_data, eigvals, eigvecs])
    print("Page: "+page+" done")
    np.save(outdir+"/"+page+"-eigen-data", eigen_data)