#!/usr/bin/env python
import mincemeat
import numpy as np
import os
import pandas as pd


def main():

    path = "./matrix/m.csv"

    data = pd.read_csv(path)
    df_a = data[data["m_name"]=="a"]
    df_b = data[data["m_name"]=="b"]

    m,k,n = df_a['row'].max()+1, df_a['col'].max()+1, df_b['col'].max()+1
    assert (df_b['row'].max()+1)==k, "n_cols of A must be equal to n_rows in B"

    tuples = [tuple(list(x)+[m, n]) for x in data.values]
    # tuples[i] =(a/b, row, col, val, m, n)

    # The data source can be any dictionary-like object
    datasource = dict(enumerate(tuples))

    def mapfn(k, v):
        if v[0]=='a':
            for z in range(v[5]):
                yield (v[1],z), (v[0], v[2], v[3])
        else:
            for z in range(v[4]):
                yield (z, v[2]), (v[0], v[1], v[3])

    def reducefn(k, vs):
        d = {}
        max_k = 0
        for v in vs:
            if v[1] > max_k:
                max_k = v[1]
            d[tuple([v[0], v[1]])] = v[2]
        s = 0
        for z in range(max_k+1):
            s += d[('a',z)]*d[('b',z)] #% 97
        return s


    s = mincemeat.Server()
    s.mapfn = mapfn
    s.reducefn = reducefn
    s.datasource = datasource

    print "Waiting for clients"

    results = s.run_server(password="changeme")

    with open('res_hw3.csv', 'w') as f:
        f.write('m_name,row,col,val\n')
        for i in range(m):
            for j in range(n):
                f.write("{},{},{},{}\n".format('c', i, j, results[(i, j)]))


if __name__ == "__main__":
    main()