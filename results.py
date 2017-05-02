from results_funcs import * # to get joke_id_to_joke
from flask_restful import Resource, reqparse
from flask import url_for, request # might need at some point
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
# import spacy
from nltk.corpus import wordnet as wn
import json
import glob
import base64
import pickle

# Decoding numpy array from JSON (from Flask template)
def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct

# input: list of dictionaries, where each dict is a joke.
# include_title and include_text are boolean flags -- important because need to determine whether we want to include
# just title for the text of the joke, or just the actual post, or both. (obviously at least one of the two needs to be
# True)
def build_tfidf(list_of_jokes, n_feats, include_title=True, include_post=True, min_df = 10, max_df = 1.0):
    tfidf_vec = TfidfVectorizer(input='content', decode_error=u'ignore', strip_accents=u'unicode',
                                analyzer=u'word',max_features=n_feats,stop_words='english',
                                norm=u'l2',min_df=min_df,max_df=max_df,lowercase=True,vocabulary=None, ngram_range=(1,3))
    data = [(dt['title'] + ' ' + dt['selftext'] if include_post else dt['title']) if include_title else
            (dt['selftext'] if include_post else '') for dt in list_of_jokes]
    doc_by_vocab_sparse = tfidf_vec.fit_transform(data)

    # Construct a inverted map from feature index to feature value (word) for later use
    index_to_vocab = tfidf_vec.get_feature_names()

    # return sparse tfidf matrix, and mapping showing the word's index to the word itself
    return (doc_by_vocab_sparse, index_to_vocab, tfidf_vec)

# These files are under the encoded_data folder in our Google Drive folder
dv_thin = np.load('final_dv_thin_4_23_17.npy')

with open('final_vectorizer_4_23_17.pkl', 'rb') as fin:
    tfidf = pickle.load(fin)

with open('final_pca_4_23_17.pkl', 'rb') as fin:
    pca = pickle.load(fin)

with open('final_jokes_4_23_17.pkl', 'rb') as fin:
    jokes = pickle.load(fin)

with open('nsfwclassifier.pkl', 'r') as fin:
    nsfwclf = pickle.load(fin)

## FILES LOADED by Dani
# with open('inv_index_file.pkl','r') as fin:
#     inv_index = pickle.load(fin)

# with open('index_to_vocab.pkl','r') as fin:
#     index_to_vocab = pickle.load(fin)

# with open('vocab_to_index.pkl','r') as fin:
#     vocab_to_index = pickle.load(fin)
####

nouns = {x.name().split('.',1)[0] for x in wn.all_synsets('n')}
# nlp = spacy.load('en')

parser = reqparse.RequestParser()
parser.add_argument('query', location='json')

LABELS = {
    'ENT': 'ENT',
    'PERSON': 'ENT',
    'NORP': 'ENT',
    'FAC': 'ENT',
    'ORG': 'ENT',
    'GPE': 'ENT',
    'LOC': 'ENT',
    'LAW': 'ENT',
    'PRODUCT': 'ENT',
    'EVENT': 'ENT',
    'WORK_OF_ART': 'ENT',
    'LANGUAGE': 'ENT',
    'DATE': 'DATE',
    'TIME': 'TIME',
    'PERCENT': 'PERCENT',
    'MONEY': 'MONEY',
    'QUANTITY': 'QUANTITY',
    'ORDINAL': 'ORDINAL',
    'CARDINAL': 'CARDINAL'
}

def get_suggestions():
    tfidfsum = pca.inverse_transform(dv_thin.sum(axis=0).reshape(1,-1))
    featnames = tfidf.get_feature_names()
    return [featnames[i] for i in np.argsort(-tfidfsum[0,:])[1:40] if featnames[i] in nouns]

# def transform_texts(texts):
#     return [' '.join([sent.lemma_ for sent in doc.sents]) for doc in nlp.pipe(texts, n_threads=2)]

def pseudorel_qvec(qvecthin, ranked_idxs, excludevec = None):
    a = 1.0
    b = 0.8
    c = 0.3
    relvecs = dv_thin[ranked_idxs,:]
    if excludevec is None:
        excludevec = np.zeros(qvecthin.shape)
    return a*qvecthin + b*np.sum(relvecs, axis=0) - c*excludevec

def get_ranked_idxs(qvec_thin, include_nsfw):
    sims = dv_thin.dot(qvec_thin.T)
    idxs = np.argsort(-sims[:,0])[:1000]
    ranked_idxs = [i for i in idxs if (include_nsfw or not nsfwclf.predict( [jokes[i]["title"] + jokes[i]["selftext"]] )[0])][:20]
    return ranked_idxs

###### TOPIC MODEL AND GETTING JOKES FROM FEATURES by Dani
# def closest_words(word_in, k = 10):
#     if word_in not in vocab_to_index: []
#     sims = words_compressed.dot(words_compressed[vocab_to_index[word_in],:])
#     asort = np.argsort(-sims)[:k+1]
#     return [(index_to_vocab[i],sims[i]/sims[asort[0]]) for i in asort[1:]]
# flatten = lambda l: [item for sublist in l for item in sublist]
# def grab_jokes_from_word(word_list):
#     words = [[k[0] for k in closest_words(word,2)] for word in word_list]
#     if not words:
#         return []
#     flattened_words = flatten(words)
#     return [k[0] for k in flatten([inv_index[w] for w in words if w in inv_index])]
######

class Results(Resource):
    def post(self):
        args = json.loads(request.form.keys()[0])
        print args
        input_dict = args
        query = input_dict['query']

        #### IF WERE TO INCLUDE by Dani
        # query_nouns = [k for k in query.split(' ') if k in nouns][:2]
        # print query_nouns
        # closest_query_words = flatten([closest_words(k,2) for k in query_nours])
        # print "===="
        # print closest_query_words
        # #### 
        # if 'liked' in input_dict:
        #     words = input_dict['liked'].split(",")
        #     closest_liked_words = flatten([closest_words(k,2) for k in words])
        #     releveant_jokes = grab_jokes_from_word(closest_liked_words) 
        ### 
        exclude = input_dict['exclude']
        ranked_list = []
        include_nsfw = input_dict['nsfw'];
        qvec = tfidf.transform([query])
        qvec_thin = pca.transform(qvec)
        evec = tfidf.transform([exclude]) if exclude else np.zeros(qvec.shape)
        evec_thin = pca.transform(evec)
        ranked_idxs = get_ranked_idxs(qvec_thin, include_nsfw)
        newqvec_thin = pseudorel_qvec(qvec_thin, ranked_idxs, excludevec=evec_thin)
        new_ranked_idxs = get_ranked_idxs(newqvec_thin, include_nsfw)
        ranked_list = [jokes[i] for i in new_ranked_idxs]
        json_output = ranked_list
        """
        i = 0
        # entries of ranked_list are just joke ids
        for jid in ranked_list:
            r_joke = jid_to_joke(jid)
            tmp_dict = {'title':r_joke['title'], 'selftext': r_joke['selftext']}
            json_output[i] = json.dumps(tmp_dict)
            i += 1
        """
        return json_output
