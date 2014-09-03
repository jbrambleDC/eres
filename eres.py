import pandas as pd
import numpy as np
import math
import nltk
import copy
import csv
import sys
from collections import defaultdict

# add tf-idf weights
#add sparcity
#update linear operations
#update dict handling
#test case for repetition
def get_data(filename):
    f = open(filename)
    return f.readlines()

def get_csv_data(filename):
    csvfile = open(filename)
    return csv.DictReader(csvfile,delimiter = ',')

def gramify(string):
    result = []
    _string = stripify(string)
    for i in range(len(_string)-2):
        result.append(_string[i:i+3])
    return result

def stripify(string):
    return string.lower().replace('.','').replace('\n','')


def tokenize(string):
    return nltk.word_tokenize(string.lower())

def det_rawfreq(grams):
    d = defaultdict(int)
    for i in grams:
        d[i]+=1
    return d

def add_dict(dic,string):
    string = string.replace('\n','')
    keys = gramify(string)
    freq_vec = det_rawfreq(keys)
    for key in freq_vec.keys():
        if key in dic.keys():
            dic[key][string]+=freq_vec[key]
        else:
            d = defaultdict(int)
            d[string]+=freq_vec[key]
            dic[key] = d

def to_df(dic):
    return pd.DataFrame(dic).fillna(0).to_sparse(fill_value=0)

def tf_idf_weight(df):
    #print df
    d = defaultdict(str)

    for i,r in df.iterrows():
        for  key in r.keys():
            if r[key] != 0:
                r[key] = 0.5 + (0.5*float(r[key])/float(r.values.max()))
        d[i] = r
        print d[i]

    df = pd.DataFrame(d).T
    N = df.shape[0]
    for key in df.keys():
        num_docs = df.groupby(key).size()
        num_non_zero=num_docs.values[1:].sum()
        idf = np.log(N/num_non_zero)
        df[key]*=idf

    return df.to_sparse(fill_value=0)

def dot_prod(df,query):
    #make this faster by only selecting the query row
    #will change dimensions of rows
    #just switch around in det_sim
    return df,df.loc[[query]].dot(df.transpose()).to_sparse(fill_value=0)

def det_mag(vec):
    total = 0
    for i in vec.keys():
        total += vec[i][0]**(2.0)
    return math.sqrt(total)

def det_sim(query,dic):
    _dic = copy.deepcopy(dic)
    add_dict(_dic,query)
    d_f, sim = dot_prod((to_df(_dic)),query)
    q_sim = sim.to_dense()
    query_vec = d_f.loc[[query]]
    for i in q_sim.keys():
        q_sim[i] = q_sim[i]/(det_mag(query_vec)*det_mag(d_f.loc[[i]]))
    return q_sim

def main():
    corps = get_data(sys.argv[1])
    data_dict = {}
    for i in corps:
        add_dict(data_dict,i)
    if sys.argv[3] == 'test':
        queries = get_csv_data(sys.argv[2])
        res = []
        q_dict = data_dict
        for i in queries:
            # can just use i for everything
            res_dict = {}
            res_dict['query'] = i['query']
            res_dict['actual'] = i['actual']
            if i['query'] != i['actual']:
                sim = det_sim(i['query'],q_dict).transpose().sort(i['query'],ascending=False).iloc[1:]
                sim = sim[i['query']]
                if sim.iloc[0] == 0:
                    res_dict['match'] = 'None'
                else:
                    res_dict['match'] = sim.index.values[0]
                    res_dict['similarity'] = sim.iloc[0]
            else:
                res_dict['match'] = i['actual']
                res_dict['similarity'] = 1.0
            res.append(res_dict)
    else:
        #microsoft vs microsfot
        queries = get_data(sys.argv[2])
        res = []
        for i in queries:
            res_dict = {}
            q_dict = data_dict
            res_dict['query'] = i
            sim = det_sim(i,q_dict).transpose().sort(i,ascending=False).iloc[1:]
            sim = sim[i]
            if sim.iloc[0] == 0:
                res_dict['match'] = 'None'
            else:
                res_dict['match'] = sim.index.values[0]
            res_dict['similarity'] = sim.iloc[0]
            res.append(res_dict)

    with open('eres_data.out.csv','wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        if 'actual' in res[0].keys():
            writer.writerow(['query','name0','actual_name','similarity'])
            for i in res:
                writer.writerow([i['query'],i['match'],i['actual'],i['similarity']])
        else:
            writer.writerow(['query','name0','similarity'])
            for i in res:
                writer.writerow([i['query'],i['match'],i['similarity']])


main()
