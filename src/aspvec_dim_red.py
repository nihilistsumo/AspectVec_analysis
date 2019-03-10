#!/usr/bin/python3

import sys, json, os, concurrent
from concurrent import futures
import numpy as np
from collections import Counter
from scipy import sparse
from scipy.sparse.linalg import svds
import sklearn
from sklearn.decomposition import PCA

def load_global_data_matrix_slow():
    data = np.load(indir+"/"+paras_np[0]+".npy")
    c = 1
    for p in range(1, len(paras_np)):
        para = paras_np[p]
        if os.path.isfile(indir+"/"+para+".npy"):
            para_vec = np.load(indir+"/"+para+".npy")
            data = np.vstack((data, para_vec))
            c+=1
            #print(str(c) + "Data size: "+str(sys.getsizeof(data)/(1024.0*1024.0))+" MB")
        else:
            print(para+" not present in global vector dir")
    return data

def load_global_data_matrix_fast():
    data = []
    for p in range(len(paras_np)):
        para = paras_np[p]
        if os.path.isfile(indir + "/" + para + ".npy"):
            data.append(np.load(indir+"/"+para+".npy"))
        else:
            print(para+" not present in global vector dir")
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

def pca_sklearn(data_matrix, svdk):
    pca = PCA(n_components=svdk)
    pca.fit(data_matrix)
    print("Sorted explained variance")
    print(pca.explained_variance_ratio_)
    print("Total variance explained by pca components: "+str(np.sum(pca.explained_variance_ratio_)))
    return pca.transform(data_matrix)

def svd_analysis(data_matrix, svdk):
    print("SVD analysis")
    print("--------------\n")
    print("Calculating col means...")
    means = np.mean(data_matrix.T, axis=1)
    print("Done")
    print("Centering data matrix...")
    cent_data = data_matrix - means
    print("Done")
    cent_data_sp = sparse.csr_matrix(cent_data)
    print("Calculating svd...")
    u, s, vt = svds(cent_data_sp.T, k=svdk)
    print("Done")
    return u, s, vt

def eigen_analysis(data_matrix):
    print("Eigen analysis")
    print("--------------\n")
    print("Calculating col means...")
    means = np.mean(data_matrix.T, axis=1)
    print("Done")
    print("Centering data matrix...")
    cent_data = data_matrix - means
    print("Done")

    print("Calculating covariance matrix...")
    cov_cent_data = np.cov(cent_data.T)
    print("Done")
    np.save(outdir+"/cov-matrix", cov_cent_data)
    print("Saved covariance matrix")
    print("Performing eigenvalue decomposition...")
    vals, vecs = np.linalg.eig(cov_cent_data)
    print("Done")
    print("Projecting data in transformed space...")
    proj_data = vecs.T.dot(cov_cent_data.T)
    print("Done")
    return proj_data, vals, vecs

def usage():
    print("parameters: svd/eig/pca art-qrels paras-file.npy global-para-vecs-dir output-dir svdk")

if len(sys.argv) < 6:
    usage()
    sys.exit()
m = sys.argv[1]
art_qrels = sys.argv[2]
paras_file = sys.argv[3]
indir = sys.argv[4]
outdir = sys.argv[5]
k = sys.argv[6]

paras_np = np.load(paras_file)
print("Loading global para vecs")
aspval_matrix = load_global_data_matrix_fast()
print("Done loading")


print("Going to do svd/eigen/pca analysis of "+str(len(paras_np))+" paras each of "+str(len(aspval_matrix[0]))+" dimensions\n")
if m == 'svd':
    u, s, vt = svd_analysis(aspval_matrix, k)
    np.save(outdir + "/u-matrix-svd", u)
    np.save(outdir + "/singular_val_svd", s)
    np.save(outdir + "/vt-matrix-svd", vt)
elif m == 'eig':
    proj_data, eigvals, eigvecs = eigen_analysis(aspval_matrix)
    np.save(outdir+"/eig-projected-data", proj_data)
    np.save(outdir+"/eigvals", eigvals)
    np.save(outdir+"/eigvecs", eigvecs)
elif m == 'pca':
    proj_data = pca_sklearn(aspval_matrix, k)
    np.save(outdir + "/pca-projected-data", proj_data)

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