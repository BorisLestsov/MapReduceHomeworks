#!/usr/bin/env python
import mincemeat
import numpy as np
import os
import nltk
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt')



def main():

    tokenizer = RegexpTokenizer(r'\w+')
    path = "./sherlock/"

    data = []
    files = os.listdir(path)
    for name in files:
        filepath = os.path.join(path, name)
        print "Preprocessing", filepath
        with open(filepath, 'r') as f:
            data.append(tokenizer.tokenize(f.read().lower()))

    # The data source can be any dictionary-like object
    datasource = dict(enumerate(data))

    def mapfn(k, v):
        for w in v:
            yield w, [k, 1]


    def reducefn(k, vs):
        arr = [0] * 67  # 67 files in the folder
        for task, i in vs:
            arr[task] += i
        return arr

    s = mincemeat.Server()
    s.mapfn = mapfn
    s.reducefn = reducefn
    s.datasource = datasource

    print "Waiting for clients"

    results = s.run_server(password="changeme")
    res = np.array(np.vstack(results.values()), dtype=np.int32)
    words = np.array(map(lambda x: [x], results.keys()))
    res = np.hstack((words, res))
    header = ["word"] + files
    header = np.array(header)
    res = np.vstack((header, res))
    with open('res_hw2.csv', 'wb') as f:
        np.savetxt(f, res, delimiter=',', fmt='%2s')

if __name__ == "__main__":
    main()