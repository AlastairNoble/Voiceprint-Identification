from tools.data_manager import *
from tools.dataCreation import *
from tools.wordSeparation import *


def create_model(n_features, n_classes):
    model = Sequential()

    model.add(Dense(n_features, input_shape=(n_features,), activation='relu'))
    model.add(Dropout(0.1))

    model.add(Dense(2048, activation='relu'))
    model.add(Dropout(0.4))

    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.4))

    model.add(Dense(2048, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(n_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def train_model(word):
    data = get_data_from_dir('{word}/')
    train, val = train_test_split(data, test_size=0.29, stratify=data['speaker'])
    ss = StandardScaler()
    train_features = get_features(train['filepath'], ss)
    val_features = get_features(val['filepath'], ss)

    train_labels = get_encoded_labels(train['speaker'])
    val_labels = get_encoded_labels(val['speaker'])

    model = create_model(3 * N_MFCCS, len(train_labels[0]))

    history = model.fit(train_features, train_labels, epochs=20, validation_data=(val_features, val_labels))

    return model, train_labels
    # print(predict_speaker("test/alex.wav", model, train['speaker'].tolist(), train_labels, ss))
    # print(predict_speaker(audio_input, model, train['speaker'].tolist(), train_labels, ss))
    # audio_input = get_audio_input()


class word_model:
    def __init__(self, word):
        data = get_data_from_dir('words/{}/'.format(word))
        train, val = train_test_split(data, test_size=0.29, stratify=data['speaker'])
        self.ss = StandardScaler()

        train_features = get_features(train['filepath'], self.ss)
        val_features = get_features(val['filepath'], self.ss)

        self.train_labels = train['speaker'].tolist()

        self.train_labels_encoded = get_encoded_labels(train['speaker'])
        val_labels = get_encoded_labels(val['speaker'])

        self.model = create_model(3 * N_MFCCS, len(self.train_labels_encoded[0]))

        history = self.model.fit(train_features, self.train_labels_encoded, epochs=20, validation_data=(val_features, val_labels))


dir_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    # words = ["the", "be", "to", "of", "and"]

    # alexa_model = word_model("alexa")

    # print(predict_speaker("test/alex.wav", alexa_model))

    # separate_words(f"{dir_path}\\test\\Sentence.wav")

    record_and_save("alastair")