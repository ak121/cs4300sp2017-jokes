from results_funcs import * # to get joke_id_to_joke
from flask_restful import Resource
from flask import url_for # might need at some point
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import json
import glob

# input: list of dictionaries, where each dict is a joke.
# include_title and include_text are boolean flags -- important because need to determine whether we want to include 
# just title for the text of the joke, or just the actual post, or both. (obviously at least one of the two needs to be 
# True)
def build_tfidf(list_of_jokes, n_feats, include_title=True, include_post=True, min_df = 10, max_df = 1.0):
    tfidf_vec = TfidfVectorizer(input='content', decode_error=u'ignore', strip_accents=u'unicode',
                                analyzer=u'word',max_features=n_feats,stop_words='english',
                                norm=u'l2',min_df=min_df,max_df=max_df,lowercase=True,vocabulary=None)
    data = [(dt['title'] + ' ' + dt['selftext'] if include_post else dt['title']) if include_title else 
            (dt['selftext'] if include_post else '') for dt in list_of_jokes]
    doc_by_vocab_sparse = tfidf_vec.fit_transform(data)

    # Construct a inverted map from feature index to feature value (word) for later use
    index_to_vocab = tfidf_vec.get_feature_names()
    
    # return sparse tfidf matrix, and mapping showing the word's index to the word itself
    return (doc_by_vocab_sparse, index_to_vocab, tfidf_vec)

jokes = []
for fname in glob.glob('*.json'):
  with open(fname) as json_data:
    jokes += json.load(json_data)

doc_by_vocab, index_to_vocab, tfidf = build_tfidf(jokes, n_feats=5000)
pca = TruncatedSVD(n_components=50)
dv_thin = pca.fit_transform(doc_by_vocab)

class Results(Resource):
    def get(self, title):
        input_dict = json.loads(title)
        query = input_dict['query']
        ranked_list = []
        # TODO IR stuff to get ranked_list
        qvec = tfidf.transform([query])
        qvec_thin = pca.transform(qvec)
        sims = dv_thin.dot(qvec_thin.T)
        idxs = np.argsort(-sims[:,0])[:10]
        ranked_list = [jokes[i] for i in idxs]
        print sims[:10,:]
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


