
# coding: utf-8

# # Make a function to build an inverted index and a tfidf vectorizer given tokenized text.

# In[1]:

from collections import defaultdict
from scipy.sparse import csr_matrix
import json


# In[2]:

with open('Jokes.json') as json_data:
    jokes = json.load(json_data)    


# In[3]:

# TODOS
# n-grams for tfidf-vectorizer?


# In[4]:

def get_inverted_index(list_of_jokes, include_title, include_post):
    data = [(dt['title'] + ' ' + dt['selftext'] if include_post else dt['title']) if include_title else 
            (dt['selftext'] if include_post else '') for dt in list_of_jokes]
    tok_data = [dt.split(' ') for dt in data]
    return build_inverted_index(tok_data)

def build_inverted_index(list_of_toks_lists):
    """ Builds an inverted index from the messages.
    
    Arguments
    =========
     
    msgs: list of dicts.
        Each message in this list already has a 'toks'
        field that contains the tokenized message.
    
    Returns
    =======
    
    index: dict
        For each term, the index contains a list of
        tuples (doc_id, count_of_term_in_doc):
        index[term] = [(d1, tf1), (d2, tf2), ...]
        
    Example
    =======
    
    >> test_idx = build_inverted_index([
    ...    {'toks': ['to', 'be', 'or', 'not', 'to', 'be']},
    ...    {'toks': ['do', 'be', 'do', 'be', 'do']}])
    
    >> test_idx['be']
    [(0, 2), (1, 2)]
    
    >> test_idx['not']
    [(0, 1)]
    
    """
    # term --> tuple
    index = defaultdict(list)
    #for m in msgs:
    for doc_id in range(0, len(list_of_toks_lists)):
        term_to_count = defaultdict(int)
        for tok in list_of_toks_lists[doc_id]:
            term_to_count[tok] += 1
        for t, cnt in term_to_count.iteritems():
            index[t].append((doc_id, cnt))
    return index    


# In[5]:

from sklearn.feature_extraction.text import TfidfVectorizer

# input: list of dictionaries, where each dict is a joke.  The dict must have 'text' as a key. 
# include_title and include_text are boolean flags -- important because need to determine whether we want to include 
# just title for the text of the joke, or just the actual post, or both. (obviously at least one of the two needs to be 
# True)
def build_tfidf(list_of_jokes, include_title, include_post, n_feats, min_df = 10, max_df = 0.8):
    tfidf_vec = TfidfVectorizer(input='content', decode_error=u'ignore', strip_accents=u'unicode',
                                analyzer=u'word',max_features=n_feats,stop_words='english',
                                norm=u'l2',min_df=min_df,max_df=max_df,lowercase=True,vocabulary=None)
    data = [(dt['title'] + ' ' + dt['selftext'] if include_post else dt['title']) if include_title else 
            (dt['selftext'] if include_post else '') for dt in list_of_jokes]
    doc_by_vocab_sparse = tfidf_vec.fit_transform(data)
    # doc_by_vocab = doc_by_vocab_sparse.toarray()   # <-- Need?

    # Construct a inverted map from feature index to feature value (word) for later use
    index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}
    
    # return sparse tfidf matrix, and mapping showing the word's index to the word itself
    return (doc_by_vocab_sparse, index_to_vocab)


# In[6]:

# Not used yet.
def filter_title_post(list_of_jokes):
    return [(dt['title'] + ' ' + dt['selftext'] if include_post else dt['title']) if include_title else 
            (dt['selftext'] if include_post else '') for dt in list_of_jokes]


# In[ ]:




# In[8]:

#TESTING
j = jokes
print get_inverted_index(j, False, True)


# In[36]:

get_inverted_index(j, True, True)['black']


# In[ ]:




# In[35]:

# Precompute and save all of this information
n_feats = 5000
# j = [{'id':1, u'title': u'this is a title', u'selftext': u'punchline_e'},{'id':2,u'title': u'this is a title2', u'selftext': u'punchline_d'},
#      {'id':3, u'title': u'this is a title3', u'selftext': u'punchline_c'},
#      {'id':4, u'title': u'this is a title4', u'selftext': u'punchline_b'},{'id':5, u'title': u'this is a title5', u'selftext': u'punchline_a'}]

j = jokes

#here, we will assign an index for each joke id. This index will help us access data in numpy matrices.
joke_id_to_index = {joke_id:index for index, joke_id in enumerate([d['id'] for d in j])}

#we will also need a dictionary mapping joke titles to joke ids
joke_title_to_id = {name:jid for name, jid in zip([d['title'] for d in j],
                                                     [d['id'] for d in j])}
joke_id_to_title = {v:k for k,v in joke_title_to_id.iteritems()}

#and because it might be useful...
joke_title_to_index = {title:joke_id_to_index[joke_title_to_id[title]] for title in [d['title'] for d in j]}
joke_index_to_title = {v:k for k,v in joke_title_to_index.iteritems()}


#printing
print joke_id_to_index
print joke_title_to_id
print joke_id_to_title
print joke_title_to_index
print joke_index_to_title

# I think order of rows in tfidf is same as order of docs in the list j.
# I think order of cols in tfidf is same as order of what get_feature_names, which I think is in alpha order.
tfidf, feat_names = build_tfidf(j, True, True, n_feats, min_df = 0, max_df = 1)
# List of tuples. 0th entry in tuple is the joke_id
inv_idx = get_inverted_index(j, True, True)

print(tfidf, feat_names)


# sims, like tfidf, is a sparse (CSR) matrix
tfidf_t = tfidf.transpose()
# print tfidf.shape
# print tfidf_t.shape

row1 = tfidf.getrow(0)
row2 =  tfidf.getrow(1)

# sims is sparse
sims = tfidf * tfidf_t


#print a[0].toarray()
# print a[1]
# print '\n'
# b =  build_tfidf(j, True, False, n_feats, min_df = 0, max_df = 1)
# print b[0].toarray()
# print b[1]
# print '\n'
# c = build_tfidf(j, False, True, n_feats, min_df = 0, max_df = 1)
# print c[0].toarray()
# print c[1]
# print '\n'
# Causes runtime error b/c there is clearly no text to consider at all.
#print build_tfidf(j, False, False, n_feats, min_df = 0, max_df = 1) 


# In[17]:


def get_sim(title1, title2, sims_mat):
    """
    Arguments:
        title1: The title of the first joke we are looking for.
        title2: The title of the second joke we are looking for.
        sims_mat: calculated as XX^T, where x is doc-by-vocab sparse matrix.
    Returns:
        similarity: Cosine similarity of the two movie transcripts.
    """
    #Code completion 1.2
    
    # Cannot do a simple np.dot on vectors in sparse matrix.
    #return np.dot(doc_by_vocab[movie_name_to_index[mov1],:],
                      #doc_by_vocab[movie_name_to_index[mov2],:])
    
    idx1 = joke_title_to_index[title1]
    idx2 = joke_title_to_index[title2]
    return sims_mat[idx1, idx2]



# In[18]:

get_sim('What are minorities?', 'I\'m Trying to Remember The Name of A Song', sims)


# In[19]:

# I wanted to buy an Audi.', 15689: u"I'm Trying to Remember The Name of A Song", 15690: u'What are minorities?', 15691: u'Did you hear that Donald Trump is technically a plant?', 15692: u'Yo mama is so ugly, when she was born the doctor wrapped the afterbirth in a blanket and threw her in the trash.', 15693: u'i had trouble swallowing a viagra last night', 15694: u'What 


# In[21]:

print sims[12,14]


# In[24]:

print sims.nonzero()


# In[26]:

print len(sims.nonzero()[0])


# In[31]:

nonzero_elems = zip(sims.nonzero()[0],sims.nonzero()[1])


# In[34]:

# print nonzero_elems

for elem in nonzero_elems:
    if elem[0] != elem[1]:
        print '**'


# In[37]:

get_sim(joke_index_to_title[208], joke_index_to_title[611], sims)


# In[ ]:

print tfidf.nonzero()


# In[39]:

print tfidf


# In[40]:

joke_index_to_title[40]


# In[41]:

joke_index_to_title[3418]


# In[44]:

print type(tfidf)


# In[ ]:



