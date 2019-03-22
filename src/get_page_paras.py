#!/usr/bin/python3

import numpy as np
import sys

def get_page_para_dict():
    data = dict()
    with open(qrels) as q:
        for l in q:
            page = l.split(" ")[0].split("/")[0]
            para = l.split(" ")[2]
            if page not in data.keys():
                data[page] = [paras_np.tolist().index(para)]
            else:
                data[page].append(paras_np.tolist().index(para))
    for page in data.keys():
        data[page] = list(dict.fromkeys(data[page]))
    return np.array(data)

qrels = sys.argv[1]
paras_file = sys.argv[2]
out_file = sys.argv[3]

paras_np = np.load(paras_file)
np.save(out_file, get_page_para_dict())