#!/usr/bin/python3

import sys, json, os
import numpy as np

def convert(json_filepath):
    paraids = []
    aspids = []
    aspvals = []
    with open(json_filepath,'r') as f:
        json_dat = json.load(f)
    for k in json_dat.keys():
        paraids.append(k)
    c = 0
    for p in paraids:
        aid = []
        av = []
        for asp in json_dat[p].keys():
            aid.append(asp.split(":")[1])
            av.append(json_dat[p][asp])
        aspids.append(aid)
        aspvals.append(av)
        c+=1
        if(c % 50 == 0):
            print(".", end=' ')
        if (c % 500 == 0):
            print("+")
    return paraids, aspids, aspvals

json_file = sys.argv[1]
out_dir = sys.argv[2]
outfile_prefix = sys.argv[3]
paraids, aspids, aspvals = convert(json_file)
paras_np = np.array(paraids)
aspids_np = np.array(aspids)
aspvals_np = np.array(aspvals)
np.save(out_dir+"/"+outfile_prefix+"-paraids", paras_np)
np.save(out_dir+"/"+outfile_prefix+"-aspids", aspids_np)
np.save(out_dir+"/"+outfile_prefix+"-aspvals", aspvals_np)
print("Done")
