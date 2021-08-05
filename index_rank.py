# importing libraries
import re
import numpy as np
import pandas as pd


## variables for calculating bm25
N = 10000 #727.0
k_1 = 1.0
k_3 = 3.0
b = 0.75
avdl = 5342  # avdl is already calculated
# r is the number of relevant documents containing the term; this is the avg
# n = number of documents got for each query
# R is the number of documents known to be relevant to a specific topic; got based on products == query
# dfreq for the term to be calculated

# bm-25 ranking is calculated based on query = each query is a product;
# extract that df['product'] == query and calculate for it the score and rank accordingly
brands = ['laneige', 'kiehls', 'drjart', 'mac', 'avene', 'fresh', 'la roche posay', 'innisfree', 'elf', 'estee lauder',
          'fenty', 'glossier', 'bobbi brown', 'skii', 'lancome']


###########################################
# Some functions
###########################################

# getting R; getting the brand name
# dataframe are the extracted sql values
def get_R(query_input, dataframe):
    brand_n =''
    n = query_input.split()
    n[0] = re.sub('\W+', '', n[0])
    for brand in brands:
        if brand.startswith(n[0]):
            brand_n = brand
    R = len(dataframe.loc[dataframe['brand'] == brand_n])
    return R, brand_n


def countX(lst, x):
    return lst.count(x)


###########################################
# calculate bm25 scores
###########################################
def bm25_scores(userquery):
    serps = []
    # the document frequency csv
    doc_f = pd.read_csv('data/doc_freq.csv', sep=',')
    # the products csv, contains everything needed
    df = pd.read_csv('data/products_final.csv', sep=",")

    query = userquery.lower()
    q = re.sub('\W+', ' ', query)
    q = re.sub(r'[^\x00-\x7f]', r'', q)
    q = q.split()

    # getting R value, brand name and tokenized query
    R, brand = get_R(query, df)
    # print(brand)
    # docs we are going to use for the query
    querydf = df.loc[df['product'] == query]
    title = list(querydf['title'])
    links = list(querydf['link'])
    # for each possible review doc in the extracted set of querydf
    docs = list(querydf['tokens'])

    # getting the qtf for each term
    for term in q:
        querytf = dict((nqt, q.count(term)) for nqt in q)
    # print(querytf)
    terms = list(querytf.keys())
    keywords = ['eye', 'face', 'reviews', 'worth', 'love', 'good', 'hate', 'bad', 'great', 'brand', 'buy']
    for k in keywords:
        terms.append(k)

    # getting the score in the individual document
    for x, doc in enumerate(docs):
        bm = []
        #     print(terms)
        # getting the score for each term in the query
        for term in terms:

            # getting qtf
            if term in querytf:
                qtf = querytf[term]
            else:
                qtf = 1

            # getting the tf of query term in the document
            tf = countX(doc,term)

            # getting r for the term - relevant documents containing the term
            r = 0
            for doc in docs:
                if term in doc:
                    r += 1

            # getting n -  number of df of the term
            n = doc_f.loc[doc_f['words'] == term, 'freq'].iloc[0]

            # getting K
            K = k_1 * ((1 - b) + b * (len(doc) / avdl))

            # getting the Robertson-Sparck Jones weight ; w_1
            upper = (r + 0.5) / (R - r + 0.5)
            lower = (n - r + 0.5) / (N - n - R + r + 0.5)
            w_1 = np.log(upper / lower)

            # calculating the bm25 score
            f_left = ((k_1 + 1) * tf) / (K + tf)
            f_right = ((k_3 + 1) * qtf) / (K + qtf)
            f_result = w_1 * f_left * f_right
            # calculating the bmscore for this doc
            bm.append(f_result)

        bm25 = np.sum(bm)  # final score
        serp = {'title': title[x],
                'link':links[x],
               'score':bm25}
        # scores.append(bm25)
        serps.append(serp)
        # reorganize based on score
        print('for doc {}: {}'.format(x, bm25))
    serps = sorted(serps, key=lambda i: i['score'], reverse=True)
    return serps


if __name__ == '__main__':
    query = 'kiehls creamy eye treatment with avocado'  # this will be input by the user

    # # the document frequency csv
    # doc_f = pd.read_csv('data/doc_freq.csv', sep=',')
    # # the products csv, contains everything needed
    # df = pd.read_csv('data/products_final.csv', sep=",")

    serps = bm25_scores(query)
    print('scores: {}'.format(serps))



