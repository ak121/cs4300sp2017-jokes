import pickle as pkl
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
# import spacy
import json
import glob

# nlp = spacy.load('en')
jokefile = 'final_jokes_4_23_17.pkl'
tfidf_transformer_file = 'final_vectorizer_4_23_17.pkl'
pca_file = 'final_pca_4_23_17.pkl'
dvthin_file = 'final_dv_thin_4_23_17.npy'
### ADDITIONAL FILES by Dani
# inv_index_file_name = 'inv_index_file.pkl'
# words_compressed_file_name = 'words_compressed.npy'
# index_to_vocab_file_name = 'index_to_vocab.pkl'
# vocab_to_index_file_name = 'vocab_to_index.pkl'
#####

with open(jokefile, 'rb') as fin:
    jokelist = pkl.load(fin)


"""
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
"""

# def transform_texts(texts):
#     return [' '.join([sent.lemma_ for sent in doc.sents]) for doc in nlp.pipe(texts, n_threads=2)]

transformed_sents = [' '.join([joke['title'], joke['selftext']]) for joke in jokelist]
print "Transformed Sentences"
tfidf_vec = TfidfVectorizer(input='content', decode_error=u'ignore', strip_accents=u'unicode',
                            analyzer=u'word',max_features=10000,stop_words='english',
                            norm=u'l2',min_df=10,max_df=1.0, vocabulary=None, ngram_range=(1,3))
pca = TruncatedSVD(n_components=30)
doc_by_vocab_sparse = tfidf_vec.fit_transform(transformed_sents)
# Construct a inverted map from feature index to feature value (word) for later use
index_to_vocab = tfidf_vec.get_feature_names()

#### TOPIC MODELING STUFF by Dani
# def build_inverted_index(list_of_toks_lists):
#     index = defaultdict(list)
#     for doc_id in range(0, len(list_of_toks_lists)):
#         term_to_count = defaultdict(int)
#         for tok in list_of_toks_lists[doc_id]:
#             term_to_count[tok] += 1
#         for t, cnt in term_to_count.iteritems():
#             index[t].append((doc_id, cnt))
#     return index    
# regex = re.compile('[%s]' % re.escape(string.punctuation))
# transformed_sents = [' '.join([joke['title'], joke['selftext']]) for joke in jokelist]
# toks = [regex.sub('',ts.lower()).split(' ') for ts in transformed_sents]
# inv_index = build_inverted_index(toks)
# lst = filter(lambda x: len(x[1])>5, inv_index.items())
# inv_index_filtered = {v[0]:v[1] for v in lst}
# _, s, words_compressed = svds(doc_by_vocab_sparse, k=100)
# vocab_to_index = { t:i for i,t in enumerate(tfidf_vec.get_feature_names())}
# words_compressed = words_compressed.transpose()
# words_compressed = normalize(words_compressed, axis = 1)
# np.save(words_compressed_file_name,words_compressed)
# with open(inv_index_file_name, 'wb') as fout:
#     pkl.dump(inv_index_filtered, fout)
# with open(index_to_vocab_file_name, 'wb') as fout:
#     pkl.dump(index_to_vocab,fout)
# with open(vocab_to_index_file_name, 'wb') as fout:
#     pkl.dump(vocab_to_index,fout)
#####

dv_thin = pca.fit_transform(doc_by_vocab_sparse)

with open(tfidf_transformer_file, 'wb') as fout:
    pkl.dump(tfidf_vec, fout)

with open(pca_file, 'wb') as fout:
    pkl.dump(pca, fout)

np.save(dvthin_file, dv_thin)
