import re
import numpy as np
import pandas as pd

# variables for calculating bm25
N = 10000  # 727.0
k_1 = 1.0
k_3 = 3.0
b = 0.75
avdl = 5342
brands = ['laneige', 'kiehls', 'drjart', 'mac', 'avene', 'fresh', 'la roche posay', 'innisfree', 'elf', 'estee lauder',
          'fenty', 'glossier', 'bobbi brown', 'skii', 'lancome']

pdct = ['lancome monsieur big volumizing mascara',
        'la roche posay anthelios ultra light fluid spf50',
        'fenty beauty killawatt highlighter',
        'glossier balm dotcom',
        'fenty beauty flyliner longwear liquid eyeliner', 'estee lauder idealist pore minimizing skin refinisher',
        'kiehls super fluid daily uv defense spf 50+', 'fresh rose deep hydration face cream',
        'estee lauder day wear matte gel creme',
        'fenty beauty cheeks out freestyle cream blush', 'fresh seaberry moisturizing face oil',
        'estee lauder perfectionist [cp+r] wrinkle lifting firming serum',
        'kiehls ultra facial cleanser', 'kiehls calendula herbal-extract toner',
        'fresh black tea firming overnight mask',
        'estee lauder perfectly clean multi-action foam cleanser purifying mask',
        'estee lauder revitalizing supreme global anti-aging cell power creme',
        'fresh rose deep hydration facial toner', 'fresh lotus youth preserve dream face cream',
        'laneige water bank moisture cream', 'fenty beauty full frontal mascara',
        'innisfree my lip balm', 'glossier boy brow', 'glossier body hero dry-touch oil mist',
        'laneige perfect renew emulsion', 'kiehls super multi-corrective cream',
        'kiehls facial fuel energizing moisture treatment for men', 'innisfree real fit velvet lipstick',
        'la roche posay cicaplast baume b5 soothing repairing balm',
        'kiehls clearly corrective™ dark spot solution',
        'kiehls hydro-plumping re-texturizing serum concentrate',
        'la roche posay effaclar duo+', 'lancome advanced génifique youth activating serum',
        'fenty beauty body lava', 'lancome absolue regenerating soft cream', 'kiehls creme de corp',
        'estee lauder hydrationist maximum moisture creme', 'fenty beauty stunna lip paint',
        'estee lauder perfectly clean multi-action toning lotion refiner', 'laneige perfect renew cream',
        'fresh black tea age-delay eye concentrate',
        'la roche posay serozin', 'la roche posay respectissime waterproof eye makeup remover',
        'lancome bi-facil makeup remover', 'laneige water bank hydro cream ex', 'glossier cloud paint',
        'innisfree pore clearing clay mousse mask', 'skii r.n.a. power radical new age essence',
        'skii facial treatment gentle cleanser',
        'fenty beauty mattemoiselle plush matte lipstick', 'elf tinted lip oil',
        'kiehls powerful-strength line-reducing concentrate',
        'lancome cils booster xl mascara primer', 'fenty beauty pro filt’r soft matte longwear foundation',
        'glossier lidstar eyeshadow', 'la roche posay thermal spring water',
        'estee lauder daywear sheer tint release moisturizer',
        'laneige essential power skin refiner moisture', 'fenty beauty portable touchup brush 130',
        'innisfree dewy glow jelly cream',
        'innisfree matte full cover cushion', 'elf gentle peeling exfoliant',
        'fenty beauty gloss bomb universal lip luminizer',
        'skii facial treatment clear lotion', 'fresh soy face cleanser',
        'innisfree minimum for sensitive skin cleansing milk',
        'lancome teint idole ultra wear foundation', 'la roche posay effaclar purifying cleansing gel',
        'innisfree brightening & pore-caring sleeping mask',
        'laneige water sleeping mask', 'laneige moisture balancing emulsion', "lancome l'absolu rouge lipstick",
        'fresh black tea age-delay cream', 'kiehls ultra facial oil-free gel cream', 'innisfree vivid cotton ink',
        'fenty beauty match stix', 'elf jelly pop face and eye glo',
        'kiehls calendula deep cleansing foaming face wash',
        "fenty beauty sun stalk'r instant warmth bronzer", 'glossier futuredew',
        'estee lauder soft clean moisture rich foaming cleanser',
        'skii facial treatment cleansing oil', 'innisfree blemish care serum with bija seed oil',
        'kiehls midnight recovery concentrate',
        'skii facial treatment essence', 'lancome tonique confort hydrating facial toner',
        'skii genoptics spot essence serum',
        'kiehls ultimate strength hand salve', 'laneige time freeze firming sleeping mask',
        'elf 50 mg cbd moisturizer',
        'skii r.n.a. power radical new age eye cream', 'innisfree cica balm with bija seed oil',
        'innisfree my palette my eyeshadow',
        'kiehls creamy eye treatment with avocado', 'kiehls ultra facial cream', 'elf poreless putty primer',
        'kiehls calendula serum-infused water cream', 'la roche posay hyalu b5 hyaluronic acid serum',
        'glossier body hero',
        'fresh sugar lemon bath & shower gel', 'la roche posay effaclar micellar water',
        'elf clarifying booster drop',
        'kiehls ultra facial toner', 'lancome la vie est belle eau de parfum', 'kiehls ultra facial cream spf 30',
        'laneige multi deep-clean cleanser', 'la roche posay redermic [r] anti-wrinkle retinol treatment',
        'elf contour palette',
        'innisfree balancing toner with green tea', 'elf wow brow gel', 'estee lauder advanced night repair serum',
        'kiehls rare earth deep pore cleansing mask', 'kiehls vital skin-strengthening super serum',
        'skii r.n.a. radical new age power cream',
        'skii facial treatment mask', 'fenty beauty brow mvp ultra fine brow pencil & styler',
        'laneige lip sleeping mask',
        'invisimatte blotting paper', 'glossier milky jelly cleanser',
        'lancome rénergie lift multi-action cream spf 15']


def related(userquery, brand):
    prodrec = []
    recc = []
    query = userquery.lower()
    q = re.sub('\W+', ' ', query)
    q = re.sub(r'[^\x00-\x7f]', r'', q)
    q = q.split()
    note = ['oil', 'cream', 'emulsion', 'mask', 'cleanser', 'spf', 'serum', 'creme', 'gel', 'toner', 'eye', 'lip',
            'mascara']
    for item in q:
        if item in note:
            prodrec.append(item)
    for x, pos in enumerate(prodrec):
        if pos == 'creme':
            prodrec.append('cream')
            del prodrec[x]

    if len(prodrec) == 1:
        for prod in pdct:
            if prod == userquery:
                continue
            if re.search(prodrec[0], prod):
                rec = {'recp': prod}
                recc.append(rec)

    elif len(prodrec) == 0:
        for prod in pdct:
            if prod == userquery:
                continue
            if re.search(brand, prod):
                rec = {'recp': prod}
                recc.append(rec)
    else:
        for prod in pdct:
            if prod == userquery:
                continue
            if all(map(prod.__contains__, prodrec)):
                print(prod)
                rec = {'recp': prod}
                recc.append(rec)
    if len(recc) > 6:
        del recc[5:]
    return recc


def get_R(query_input, dataframe):
    brand_n = ''
    n = query_input.split()
    n[0] = re.sub('\W+', '', n[0])
    for brand in brands:
        if brand.startswith(n[0]):
            brand_n = brand
    R = len(dataframe.loc[dataframe['brand'] == brand_n])
    return R, brand_n


def countX(lst, x):
    return lst.count(x)


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
    # print(querydf.head())
    title = list(querydf['title'])
    links = list(querydf['link'])
    # for each possible review doc in the extracted set of querydf
    docs = list(querydf['tokens'])

    # getting the qtf for each term
    for term in q:
        querytf = dict((nqt, q.count(term)) for nqt in q)
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
            tf = countX(doc, term)

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
                'link': links[x],
                'score': bm25}
        serps.append(serp)
        # reorganize based on score
    serps = sorted(serps, key=lambda i: i['score'], reverse=True)
    return serps, brand
