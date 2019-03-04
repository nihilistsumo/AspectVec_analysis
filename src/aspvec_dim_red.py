#!/usr/bin/python3

import sys, json, os, concurrent
from concurrent import futures
import numpy as np
from collections import Counter

def load_global_data_matrix():
    data = []
    for p in range(len(paras_np)):
        para = paras_np[p]
        para_vec = np.load(indir+"/"+para+".npy")
        data.append(para_vec)
    return np.array(data)


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

def eigen_analysis(data_matrix):
    means = np.mean(data_matrix.T, axis=1)
    cent_data = data_matrix - means
    cov_cent_data = np.cov(cent_data.T)
    vals, vecs = np.linalg.eig(cov_cent_data)
    proj_data = vecs.T.dot(cov_cent_data.T)
    return proj_data, vals, vecs

def usage():
    print("parameters: art-qrels paras-file.npy global-para-vecs-dir output-dir")

if len(sys.argv) < 5:
    usage()
    sys.exit()
art_qrels = sys.argv[1]
paras_file = sys.argv[2]
indir = sys.argv[3]
outdir = sys.argv[4]

paras_np = np.load(paras_file)
print("Loading global para vecs")
aspval_matrix = load_global_data_matrix()
print("Done loading")


print("Going to do eigen analysis of "+str(len(paras_np))+" paras each of "+str(len(aspval_matrix[0]))+" dimensions")
proj_data, eigvals, eigvecs = eigen_analysis(aspval_matrix)
print("Done, going to save")
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