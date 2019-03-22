#!/usr/bin/python3
import numpy as np
import tensorflow as tf

def split_to_tensors(page,w):
    triples = train_dat[()][page]
    sipage = []
    sjpage = []
    qipage = []
    qjpage = []
    c = 0
    for t in triples:
        c+=1
        print(c)
        sim = []
        odd = t[3]
        for p in range(3):
            if p != odd:
                sim.append(p)
        simp1 = (para_pca_tiny[sim[0]]+1)/2
        simp2 = (para_pca_tiny[sim[1]]+1)/2
        oddp = (para_pca_tiny[odd]+1)/2
        for x in range(len(simp1)-1):
            for y in range(x+1, len(simp1)):
                tens_wt = np.array([w[x],w[y],w[x],w[y]])
                if simp1[y] < simp2[y]:
                    if simp1[x] < simp2[x]:
                        sjpage.append([simp1[x], simp1[y], simp2[x], simp2[y]]*tens_wt)
                    else:
                        sipage.append([simp1[x], simp1[y], simp2[x], simp2[y]]*tens_wt)
                else:
                    if simp1[x] < simp2[x]:
                        sjpage.append([simp2[x], simp2[y], simp1[x], simp1[y]]*tens_wt)
                    else:
                        sipage.append([simp2[x], simp2[y], simp1[x], simp1[y]]*tens_wt)
                if oddp[y] < simp2[y]:
                    if oddp[x] < simp2[x]:
                        qjpage.append([oddp[x], oddp[y], simp2[x], simp2[y]]*tens_wt)
                    else:
                        qipage.append([oddp[x], oddp[y], simp2[x], simp2[y]]*tens_wt)
                else:
                    if oddp[x] < simp2[x]:
                        qjpage.append([simp2[x], simp2[y], oddp[x], oddp[y]]*tens_wt)
                    else:
                        qipage.append([simp2[x], simp2[y], oddp[x], oddp[y]]*tens_wt)
                if simp1[y] < oddp[y]:
                    if simp1[x] < oddp[x]:
                        qjpage.append([simp1[x], simp1[y], oddp[x], oddp[y]]*tens_wt)
                    else:
                        qipage.append([simp1[x], simp1[y], oddp[x], oddp[y]]*tens_wt)
                else:
                    if simp1[x] < oddp[x]:
                        qjpage.append([oddp[x], oddp[y], simp1[x], simp1[y]]*tens_wt)
                    else:
                        qipage.append([oddp[x], oddp[y], simp1[x], simp1[y]]*tens_wt)
    sipage_t = tf.convert_to_tensor(np.array(sipage))
    sjpage_t = tf.convert_to_tensor(np.array(sjpage))
    qipage_t = tf.convert_to_tensor(np.array(qipage))
    qjpage_t = tf.convert_to_tensor(np.array(qjpage))
    return sipage_t, sjpage_t, qipage_t, qjpage_t

def arrange_triples(dat):
    sim1 = []
    sim2 = []
    data_tn = []
    for t in dat:
        if t[0] == t[3]:
            sim1.append(t[1])
            sim2.append(t[2])
        elif t[1] == t[3]:
            sim1.append(t[0])
            sim2.append(t[2])
        else:
            sim1.append(t[0])
            sim2.append(t[1])
    sim1 = np.array(sim1)
    sim2 = np.array(sim2)
    odd = dat[:, 3].T
    sim1_vec = []
    for p in sim1:
        sim1_vec.append((para_pca_tiny[p] - np.min(para_pca_tiny[p]))/(np.max(para_pca_tiny[p] - np.min(para_pca_tiny[p]))))
    sim1_vec = np.array(sim1_vec)
    sim2_vec = []
    for p in sim2:
        sim2_vec.append((para_pca_tiny[p] - np.min(para_pca_tiny[p]))/(np.max(para_pca_tiny[p] - np.min(para_pca_tiny[p]))))
    sim2_vec = np.array(sim2_vec)
    odd_vec = []
    for p in odd:
        odd_vec.append((para_pca_tiny[p] - np.min(para_pca_tiny[p]))/(np.max(para_pca_tiny[p] - np.min(para_pca_tiny[p]))))
    odd_vec = np.array(odd_vec)
    return np.transpose(np.stack((sim1_vec, sim2_vec, odd_vec), axis=0), (1,0,2))

def theta(m):
    return 0

def theta_(m):
    return tf.reduce_mean(tf.divide(tf.multiply(tf.gather(tf.transpose(m),0),tf.gather(tf.transpose(m),1)),
                                   tf.multiply(tf.gather(tf.transpose(m),2),tf.gather(tf.transpose(m),3))))


def optimize():
    with tf.Session() as session:
        page = 'tqa:artificial%20light'
        weights = tf.Variable(np.full(len(para_pca_tiny[0]), 1.0))
        session.run(tf.global_variables_initializer())
        si, sj, qi, qj = split_to_tensors(page, weights)
        print("split")
        loss = tf.divide(tf.add(theta_(qi), theta_(qj)), tf.add(theta_(si), theta_(sj)))
        print("loss")
        optimizer = tf.train.AdamOptimizer(0.01)
        print("optimizer")
        minimizer = optimizer.minimize(loss, var_list=weights)
        print("minimizer")

        for step in range(10):
            _, cur_loss = session.run([minimizer, loss])
            print(cur_loss)
        print(session.run(weights))
        w = session.run(weights)


def optimize_cos():
    with tf.Session() as session:
        page = 'tqa:artificial%20light'
        para_vec_dat = tf.convert_to_tensor(arrange_triples(np.array(train_dat[()][page])))
        weights = tf.Variable(np.full(len(para_pca_tiny[0]), 1.0))
        # multiply with weights inside loss calc
        session.run(tf.global_variables_initializer())
        print("split")
        loss = tf.divide(tf.add(theta_(qi), theta_(qj)), tf.add(theta_(si), theta_(sj)))
        print("loss")
        optimizer = tf.train.AdamOptimizer(0.01)
        print("optimizer")
        minimizer = optimizer.minimize(loss, var_list=weights)
        print("minimizer")

        for step in range(10):
            _, cur_loss = session.run([minimizer, loss])
            print(cur_loss)
        print(session.run(weights))
        w = session.run(weights)

paraids = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/asp-vecs-np/all-std-10000-paraids.npy")
aspids = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/asp-vecs-np/all-std-10000-aspids.npy")
aspvals = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/asp-vecs-np/all-std-10000-aspvals.npy")
para_pca_tiny = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/aspvec-pca/pca-projected-data-10.npy")
para_pca = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/aspvec-pca/pca-projected-data-200.npy")
train_dat = np.load("/home/sumanta/Documents/Dugtrio-data/parasim-manual-assesment/triples/train/train.triples.matrix.npy")
optimize()