#!/usr/bin/env python
import mincemeat
import numpy as np
import os
import nltk
from nltk.tokenize import RegexpTokenizer
import re
import string
import pandas as pd
nltk.download('punkt')



def main():

    tokenizer = RegexpTokenizer(r'\w+')
    path = "./southpark/All-seasons.csv"

    data = pd.read_csv(path)
    data['Line'] = data['Line'].str.replace('\n', '')

    subdata = data[['Character', 'Line']]
    tuples = [tuple(x) for x in subdata.values]
    data = [[x[0], tokenizer.tokenize(x[1].lower())] for x in tuples]

    del subdata

    # The data source can be any dictionary-like object
    datasource = dict(enumerate(data))

    def mapfn(k, v):
        #for name, words in v:
        #    print name, words
        yield v[0], set(v[1])


    def reducefn(k, vs):
        return len(set().union(*vs))


    s = mincemeat.Server()
    s.mapfn = mapfn
    s.reducefn = reducefn
    s.datasource = datasource

    print "Waiting for clients"

    results = s.run_server(password="changeme")
    
    #print results

    with open('res_hw1.csv', 'w') as f:
        f.write('Character,UniqWords\n')
        for name, words in results.iteritems():
            f.write("{},{}\n".format(name, words))


if __name__ == "__main__":
    main()