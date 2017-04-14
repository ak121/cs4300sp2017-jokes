from results_funcs import * # to get joke_id_to_joke
from flask_restful import Resource
from flask import url_for # might need at some point

class Results(Resource):
    def get(json_input):
        input_dict = json.load(json_input)
        query = input_dict['query']
        ranked_list = []
        # TODO IR stuff to get ranked_list
        
        json_output = [None for i in xrange(len(ranked_list)]
        i = 0
        # entries of ranked_list are just joke ids
        for jid in ranked_list:
            r_joke = jid_to_joke(jid)
            tmp_dict = {'title':r_joke['title'], 'selftext': r_joke['selftext']}
            json_output[i] = json.dumps(tmp_dict)
            i += 1
        return json_output
