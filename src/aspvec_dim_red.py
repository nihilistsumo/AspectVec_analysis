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

def project_para_global_asp(p, paras, asps, aspvals, useful_asps, result_dict):
    uvals = []
    for uasp in range(len(useful_asps)):
        curr_asp = useful_asps[uasp]
        if curr_asp in asps[p]:
            uvals.append(aspvals[p][asps[p].tolist().index(useful_asps[uasp])])
        else:
            uvals.append(0.0)
    result_dict[paras[p]] = uvals
    print(".")

def get_useful_aspval_mat(paras, asps, aspvals, k):
    # create frequency dictionary of asp ids
    # take top asps
    # create aspval matrix corresponding to top asps
    # do eigen analysis on top of that
    asps_freq = Counter(asps.flatten())
    sorted_aspids = sorted(asps_freq, key=asps_freq.get, reverse=True)
    c = 0
    # k = (cut*100)/(len(paras), only those asps will remain whose para-frequency is at least k% of len(paras)
    cut = len(paras)*k//100 + 1
    for sa in sorted_aspids:
        if asps_freq[sa] < cut:
            break
        c+=1
    useful_aspids = sorted_aspids[:c]
    print_para_coverage(paras, asps, sorted_aspids, useful_aspids, c)
    print("Creating expanded data matrix")
    useful_aspvals_dict = dict()

    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(project_para_global_asp, p, paras, asps, aspvals, useful_aspids, useful_aspvals_dict) for p in range(len(paras))]
    concurrent.futures.wait(futures)

    # now useful_aspvals has asp values for each paras in row and each useful_asp in column
    useful_aspvals = []
    for p in range(len(paras)):
        useful_aspvals.append(useful_aspvals_dict[paras[p]])
    return np.array(useful_aspids), np.array(useful_aspvals)

def eigen_analysis(data_matrix):
    means = np.mean(data_matrix.T, axis=1)
    cent_data = data_matrix - means
    cov_cent_data = np.cov(cent_data.T)
    vals, vecs = np.linalg.eig(cov_cent_data)
    proj_data = vecs.T.dot(cov_cent_data.T)
    return proj_data, vals, vecs

def usage():
    print("parameters: art-qrels paras-file.npy aspids-file.npy aspvals-file.npy output-dir k(in %)")


if len(sys.argv) < 7:
    usage()
    sys.exit()
art_qrels = sys.argv[1]
paras_file = sys.argv[2]
aspids_file = sys.argv[3]
aspvals_file = sys.argv[4]
outdir = sys.argv[5]
k = int(sys.argv[6])
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
useful_asps, aspval_matrix = get_useful_aspval_mat(paras_np, aspids_np, aspvals_np, k)
print("Going to do eigen analysis of "+str(len(paras_np))+" paras each of "+str(len(aspval_matrix[0]))+" dimensions")
proj_data, eigvals, eigvecs = eigen_analysis(aspval_matrix)
print("Done, going to save")
np.save(outdir+"/useful_aspids", useful_asps)
np.save(outdir+"/projected-data", proj_data)
np.save(outdir+"/eigvals", eigvals)
np.save(outdir+"/eigvecs", eigvecs)
print("Saved")


# for page in page_para_dict.keys():
#     page_paras = page_para_dict[page]
#     page_aspids = []
#     page_aspvals = []
#     for para in page_paras:
#         page_aspids.append(aspids_np[paras_np.tolist().index(para)])
#         page_aspvals.append(aspvals_np[paras_np.tolist().index(para)])
#     aspval_matrix = get_useful_aspval_mat(page_paras, page_aspids, page_aspvals)
#     print("Going to do eigen analysis of "+str(len(page_paras))+" paras in Page: "+page)
#     proj_data, eigvals, eigvecs = eigen_analysis(np.array(aspval_matrix))
#     eigen_data = np.array([page_paras, proj_data, eigvals, eigvecs])
#     print("Page: "+page+" done")
#     np.save(outdir+"/"+page+"-eigen-data", eigen_data)