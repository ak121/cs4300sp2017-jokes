from results_funcs import * # to get joke_id_to_joke
from flask_restful import Resource, reqparse
from flask import url_for, request # might need at some point
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
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


parser = reqparse.RequestParser()
parser.add_argument('query', location='json')

class Results(Resource):
    def post(self):
        args = json.loads(request.form.keys()[0])
        print args
        input_dict = args
        query = input_dict['query']
        ranked_list = []
        #include_nsfw = True #Hard coded right now but should get from query params
        include_nsfw = input_dict['nsfw'];
        # TODO IR stuff to get ranked_list
        qvec = tfidf.transform([query])
        qvec_thin = pca.transform(qvec)
        sims = dv_thin.dot(qvec_thin.T)
        idxs = np.argsort(-sims[:,0])[:1000]
        ranked_list = [jokes[i] for i in idxs if (include_nsfw or not nsfwclf.predict( [jokes[i]["title"] + jokes[i]["selftext"]] )[0])][:10]
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


