#!/usr/bin/python3
import sys
import numpy as np
import tensorflow as tf

def convert_to_matrix():
    # triples_file = "/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/triples/train/train.triples"
    # paraids = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/asp-vecs-np/all-std-10000-paraids.npy")
    paraids = np.load(paraids_file)
    matrix_data = dict()
    with open(triples_file, 'r') as tf:
        triples_lines = tf.readlines()
        print("Start")
        for l in triples_lines:
            difficult = int(l.split(" ")[5])
            if difficult != 1:
                elems = l.split(" ")
                page = elems[0]
                p1 = elems[1]
                p2 = elems[2]
                p3 = elems[3]
                odd = elems[4]
                if p1 == odd:
                    data = [paraids.tolist().index(p2), paraids.tolist().index(p3), paraids.tolist().index(p1)]
                elif p2 == odd:
                    data = [paraids.tolist().index(p1), paraids.tolist().index(p3), paraids.tolist().index(p2)]
                else:
                    data = [paraids.tolist().index(p1), paraids.tolist().index(p2), paraids.tolist().index(p3)]
                if page not in matrix_data.keys():
                    matrix_data[page] = [data]
                else:
                    matrix_data[page].append(data)
    print("Done")
    matrix_data = np.array(matrix_data)
    # np.save("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/triples/train/train.triples.matrix", matrix_data)
    np.save(output_file, matrix_data)

triples_file = sys.argv[1]
paraids_file = sys.argv[2]
output_file = sys.argv[3]

convert_to_matrix()