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

N_MFCCS = 12

def get_data_from_dir(dir, n_classes=10):
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
    X, sample_rate = librosa.load(filename, res_type='kaiser_fast')

    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=n_mfccs)
    mfccs_mean = np.mean(mfccs.T, axis=0)

    delta = librosa.feature.delta(mfccs)
    delta_mean = np.mean(delta.T, axis=0)

    deltadelta = librosa.feature.delta(mfccs, order=2)
    deltadelta_mean = np.mean(deltadelta.T, axis=0)

    return mfccs_mean.tolist() + delta_mean.tolist() + deltadelta_mean.tolist()


def get_features(filepaths, ss):

    features = filepaths.apply(extract_features)
    features = features.tolist()
    features_scaled = ss.fit_transform(features)
    return features_scaled


def get_encoded_labels(speaker_names):
    speaker_names.tolist()
    lb = LabelEncoder()
    return to_categorical(lb.fit_transform(speaker_names))


def predict_speaker(file_path, word_model):

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
    return prediction


def get_audio_input():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
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