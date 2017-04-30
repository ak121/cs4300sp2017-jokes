from results_funcs import * # to get joke_id_to_joke
from flask_restful import Resource, reqparse
from flask import url_for, request # might need at some point
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import spacy
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

with open('nsfwclassifier.pkl', 'rb') as fin:
    nsfwclf = pickle.load(fin)

nlp = spacy.load('en')

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

def transform_texts(texts):
    # Load the annotation models
    # Stream texts through the models. We accumulate a buffer and release
    # the GIL around the parser, for efficient multi-threading.
    for doc in nlp.pipe(texts, n_threads=2):
        # Iterate over base NPs, e.g. "all their good ideas"
        for np in list(doc.noun_chunks):
            # Only keep adjectives and nouns, e.g. "good ideas"
            while len(np) > 1 and np[0].dep_ not in ('amod', 'compound'):
                np = np[1:]
            if len(np) > 1:
                # Merge the tokens, e.g. good_ideas
                np.merge(np.root.tag_, np.text, np.root.ent_type_)
            # Iterate over named entities
            for ent in doc.ents:
                if len(ent) > 1:
                    # Merge them into single tokens
                    ent.merge(ent.root.tag_, ent.text, ent.label_)
        token_strings = []
        for token in doc:
            text = token.text.replace(' ', '_')
            tag = token.ent_type_ or token.pos_
            token_strings.append('%s|%s' % (text, tag))
        yield ' '.join(token_strings)

def pseudorel_qvec(qvecthin, ranked_idxs):
    a = 1.0
    b = 0.8
    relvecs = dv_thin[ranked_idxs,:]
    return a*qvecthin + b*np.sum(relvecs, axis=0)

def get_ranked_idxs(qvec_thin, include_nsfw):
    sims = dv_thin.dot(qvec_thin.T)
    idxs = np.argsort(-sims[:,0])[:1000]
    ranked_idxs = [i for i in idxs if (include_nsfw or not nsfwclf.predict( [jokes[i]["title"] + jokes[i]["selftext"]] )[0])][:10]
    return ranked_idxs

class Results(Resource):
    def post(self):
        args = json.loads(request.form.keys()[0])
        print args
        input_dict = args
        query = input_dict['query']
        ranked_list = []
        #include_nsfw = True #Hard coded right now but should get from query params
        include_nsfw = input_dict['nsfw'];
        qvec = tfidf.transform([query])
        qvec_thin = pca.transform(qvec)
        ranked_idxs = get_ranked_idxs(qvec_thin, include_nsfw)
        newqvec_thin = pseudorel_qvec(qvec_thin, ranked_idxs)
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
