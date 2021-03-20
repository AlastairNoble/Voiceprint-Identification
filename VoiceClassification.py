from tools.data_manager import *
from tools.dataCreation import *
from tools.wordSeparation import *
import keras

def create_model(n_features, n_classes):
    """
    :param n_features: int
        number of features in the data
    :param n_classes:
        number of classes/speakers/labels
    :return:
        keras model
    """
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


class word_model:
    """
    A class to represent a model for multiple words
    Attributes:
        train_labels: list
            list of labels (speakers) in the training set
        train_labels_encoded: list
            list of one hot encoded labels
        model: keras model
            model fit to the training data

    """
    def __init__(self, words, load=False, path=""):
        """
        constructs one keras model for many words using data found in directory words/'word'/ for each 'word'
        :param words: list of str
            list of words to use for training, ASSUMES data for each word exists in words/'word'
        """

        data = pd.DataFrame()
        for word in words:
            word_data = get_data_from_dir('words/{}/'.format(word))
            data = data.append(word_data)

        train, val = train_test_split(data, test_size=0.25, stratify=data['speaker'])
        self.ss = StandardScaler()

        train_features = get_features(train['filepath'], self.ss)
        val_features = get_features(val['filepath'], self.ss)

        self.train_labels = train['speaker'].tolist()

        self.train_labels_encoded = get_encoded_labels(train['speaker'])
        val_labels = get_encoded_labels(val['speaker'])

        if load:
            self.model = keras.models.load_model(path)
            self.accuracy = self.model.evaluate(val_features, val_labels)
        else:
            self.model = create_model( N_MFCCS, len(self.train_labels_encoded[0]))
            history = self.model.fit(train_features, self.train_labels_encoded, epochs=50, validation_data=(val_features, val_labels))
            self.accuracy = history.history['val_accuracy']


dir_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":

    # play_recordings(['sentence'])
    # words = ["alexa","the", "be", "to", "of", "and"]
    #
    model = word_model(['sentence'])
    #
    # print(predict_speaker("test/eli.wav", model))
    # print(predict_speaker("test/harley.wav", model))
    # print(predict_speaker("test/alex.wav", model))

    # live_input(model)

    # separate_words(f"{dir_path}\\test\\Sentence.wav")

    # record_and_save("harley")
