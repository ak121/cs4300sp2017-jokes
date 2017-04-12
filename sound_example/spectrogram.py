from specgram_funcs import *
from flask_restful import Resource
from flask import url_for

class Spectrogram(Resource):
    def get(self, title):
        fs, data = read_data('./static/%s.wav' % title)
        f,t,s = spectrogram(data, fs=fs, nperseg=1024, noverlap=512)
        specgram = {'specmat': s.tolist(),
                    'freqs': f.tolist(),
                    'times': t.tolist(),
                    'filename': url_for('static', filename='%s.wav' % title),
                    'maxtime': float(max(t)),
                    'maxfreq': float(max(f)),
                    'maxamplitude': float(max(s)) }
        return specgram

#'spectrogram': [{'frequency':f[i].item(), 'time':t[j].item(), 'amplitude':s[i,j].item()}
#                            for i in range(len(f)) for j in range(len(t))],
#
#
#               'specmat': s.tolist(),
#            'freqs': f.tolist(),
#            'times': t.tolist(),
