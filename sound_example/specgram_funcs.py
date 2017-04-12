from __future__ import division
from __future__ import print_function
from scipy.io.wavfile import read
from scipy.signal import *
from numpy import max,mean
from sys import argv
import json


def read_data(filename):
    rawfs, rawdata = read(filename)
    #If audio is mono
    if len(rawdata.shape) == 1:
        fs, data = prune_samples(rawfs, rawdata)
    else:
        #If audio has two channels
        longdata = mean(rawdata, 1)
        fs, data = prune_samples(rawfs, longdata)
    return fs, data

#Since most of the frequencies are well below half the sampling rate, prune the high frequencies
def prune_samples(fs, data):
    #Sample every fifth element of the data array
    newdata = data[::5]
    newfs = fs/5
    return (newfs, newdata)


#Make a javascript file with an object containing the times, frequencies, and amplitudes for future processing
def generate_jsdata(filename):
    fs, data = read_data(filename)
    f,t,s = spectrogram(data, fs=fs, nperseg=1024, noverlap=512)
    specgram = [{'frequency':f[i].item(), 'time':t[j].item(), 'amplitude':s[i,j].item()}
                                for i in range(len(f)) for j in range(len(t))]
    jsstring = ('var spectrogram = ' + json.dumps(specgram) + '\n'
                + 'var filename = ' + "'" + filename + "'" + '\n'
                + 'var maxtime = ' + str(max(t)) + '\n'
                + 'var maxfreq = ' + str(max(f)) + '\n'
                + 'var maxamplitude = ' + str(max(s)) + '\n' )
    with open('./spectrogram.js','w+') as jsfile:
        jsfile.write(jsstring)

def main():
    filename = argv[1]
    generate_jsdata(filename)

if __name__ == '__main__':
    main()
