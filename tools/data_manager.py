import os
import pandas as pd
import librosa
from sklearn.model_selection import train_test_split
import numpy as np
import pyaudio
import wave
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from tools.wordSeparation import *
N_MFCCS = 24  # number of MFCCs to use in feature extraction

def get_data_from_dir(dir):
    """
    returns filenames corresponding to speakers. Assumes files are organized as follows /speaker/example.wav
    :param dir: str
        current working directory
    :param n_classes: int
        number of classes/
    :return: pandas dataframe
        dataframe with columns 'filepath' and 'speaker' where 'filepath' references a .wav file
    """
    speakers = os.listdir(dir)
    speakers = speakers[:10]

    df = pd.DataFrame(columns=['filepath', 'speaker'])
    for speaker in speakers:
        files = os.listdir(dir + '{}/'.format(speaker))
        for file in files:
            filepath = dir + '{}/{}'.format(speaker, file)
            df = df.append({'filepath': filepath, 'speaker': speaker}, ignore_index=True)
    return df


def extract_features(filename, n_mfccs=N_MFCCS):
    """
    Extract MFCCs and other features from .wav file
    :param filename: str
        wav file to extract features from
    :param n_mfccs: int
        number of mfccs to extract
    :return: list
        list of extracted features
    """
    X, sample_rate = librosa.load(filename, res_type='kaiser_fast')

    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=n_mfccs)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    #
    # delta = librosa.feature.delta(mfccs)
    # delta_mean = np.mean(delta.T, axis=0)
    #
    # deltadelta = librosa.feature.delta(mfccs, order=2)
    # deltadelta_mean = np.mean(deltadelta.T, axis=0)

    return mfccs_mean.tolist()#  + delta_mean.tolist() + deltadelta_mean.tolist()


def get_features(filepaths, ss):
    """
    extract and scale features for all files
    :param filepaths:
        list of filepaths of .wav files to get features from
    :param ss: standardScalar()
        used to fit and transform data (remove the mean from the data and scale it to unit variance)
    :return:
    """
    features = filepaths.apply(extract_features)
    features = features.tolist()
    features_scaled = ss.fit_transform(features)
    return features_scaled


def get_encoded_labels(speaker_names):
    """
    one hot encode labels
    :param speaker_names: list
        list of strings of labels/speakers
    :return: list
        list of one hot encoded labels
    """
    speaker_names.tolist()
    lb = LabelEncoder()
    return to_categorical(lb.fit_transform(speaker_names))


def predict_speaker(file_path, word_model):
    """
    predict the labels of the speaker from a .wav file
    :param file_path: str
        file path for the .wav file to predict the speaker of
    :param word_model:
        trained model to make the prediction from
    :return: prediction: str, predicted speaker/label
        m: float prediction confidence
    """
    labels = word_model.train_labels_encoded.tolist()  # list of the encoded labels from training

    features = word_model.ss.transform([extract_features(file_path)])

    to_predict = np.array(features)  # list of data for the model to predict, just one item for now

    predictions = word_model.model.predict(to_predict)  # returns a list of predictions
    pred = predictions[0].tolist()  # take the first element which is the prediciton for the first element in to_predict, remember this is still one hot encoded so it is a big array of 0s and 1s
    m = max(pred)
    p = [1 if i == m else 0 for i in pred]  # convert highest propability to 1 and all else to 0
    try:
        prediction_ind = labels.index(p)  # index of predicted label (encoded)
        prediction = word_model.train_labels[prediction_ind]
    except:
        prediction = "could not identify speaker"
    return prediction, m

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def get_mic_input():
    """
    get live audio input for 1 second and save it as a .wav file
    :return: str
        name of the .wav file where the audio is saved
    """
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = "test/test_output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("say '' in: 2")
    for i in range(1, 0, -1):
        time.sleep(1)
        print(i)
    time.sleep(1)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME


def get_meeting_input(secs = 2):

    WAVE_OUTPUT_FILENAME = "test/test_out_from_in.wav"
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # select the name of the audio input you want to use! see readme for details
        if (dev['name'] == 'Microphone (Realtek(R) Audio)' and dev['hostApi'] == 0):
            dev_index = dev['index']

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=48000,
                    input=True,
                    input_device_index=dev_index,
                    frames_per_buffer=CHUNK)

    # print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * secs)):
        data = stream.read(CHUNK)
        frames.append(data)

    # print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME


def most_frequent(p, c):
    """
    :param List: list
    :returns most frequently occuring element in a list
    """
    # if len(List) > 0:
    #     return max(set(List), key=List.count)
    if len(p) == 0:
        return '', 0

    confs = {}
    counts = {}
    for i in range(len(p)):
        confs[p[i]] = confs.get(p[i], 0) + c[i]
        counts[p[i]] = counts.get(p[i], 0) + 1

    speaker = max(confs, key=confs.get)
    confidence = confs[speaker]/counts[speaker]
    return speaker, confidence


def short_prediction(model, s=2):
    """
    record computer input for s seconds, then break it into chunks, then predict the speaker of each chunk, then return the best prediction
    :param model: keras model
    :param s: int
        seconds to record
    :return: string
        prediction of speaker in segment
    """
    one_second_input = get_meeting_input(s)
    chunks = separate_words(one_second_input)

    predictions = []
    confidence = []
    for chunk in chunks:
        try:
            pred, c = predict_speaker(chunk, model)

            # print(f"{pred}, {c}")
            predictions.append(pred)
            confidence.append(c)
        except:
            pass
    return most_frequent(predictions, confidence)


def live_input(model):
    """
    make short term predictions until interrupted.
    :param model: keras model
    """
    while True:
        print(short_prediction(model, 2))