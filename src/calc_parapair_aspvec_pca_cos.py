#!/usr/bin/python3
import sys, lucene, concurrent, multiprocessing
import numpy as np
import scipy
from scipy import spatial

def get_page_para_dict():
    data = dict()
    with open(qrels) as q:
        for l in q:
            page = l.split(" ")[0].split("/")[0]
            para = l.split(" ")[2]
            if page not in data.keys():
                data[page] = set([paraids.tolist().index(para)])
            else:
                data[page].add(paraids.tolist().index(para))
    return data

def calc_score(t):
    p1 = paraids[t[0]]
    p2 = paraids[t[1]]
    p3 = paraids[t[2]]
    if pca_vec == "global":
        p1vec = para_pca[t[0]]
        p2vec = para_pca[t[1]]
        p3vec = para_pca[t[2]]
    else:
        p1vec = para_pca[()][page][page_paras[page].index(t[0])]
        p2vec = para_pca[()][page][page_paras[page].index(t[1])]
        p3vec = para_pca[()][page][page_paras[page].index(t[2])]
    p1vec_normed = (p1vec - np.min(p1vec))/(np.max(p1vec) - np.min(p1vec))
    p2vec_normed = (p2vec - np.min(p2vec))/(np.max(p2vec) - np.min(p2vec))
    p3vec_normed = (p3vec - np.min(p3vec))/(np.max(p3vec) - np.min(p3vec))
    return p1 + " " + p2 + " " + str(1-spatial.distance.cosine(p1vec_normed, p2vec_normed)) + "\n" + p1 + " " + p3 + " " \
           + str(1-spatial.distance.cosine(p1vec_normed, p3vec_normed)) + "\n" + p2 + " " + p3 + " " \
           + str(1-spatial.distance.cosine(p2vec_normed, p3vec_normed)) + "\n"

paraids_file = sys.argv[1]
para_pca_file = sys.argv[2]
triples_matrix_file = sys.argv[3]
output_file = sys.argv[4]
qrels = sys.argv[5]
pca_vec = sys.argv[6]
# denotes the nature of the pca data; can be pagewise or global

paraids = np.load(paraids_file)
para_pca = np.load(para_pca_file)
triples_matrix = np.load(triples_matrix_file)
page_paras = get_page_para_dict()
page = ""
print("done loading")
with open(output_file, 'w') as op:
    for p in triples_matrix[()].keys():
        page = p
        if page == "enwiki:Chatbot":
            print("here")
        for t in triples_matrix[()][p]:
            op.write(calc_score(t))
        print(p)