from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import wave
import os
from playsound import playsound
import pyaudio
from time import sleep
import shutil
from tools.wordSeparation import clear_audio


directory_to_project = dir_path = os.path.dirname(os.path.realpath(__file__))  # "C:\\Users\\harle\\PycharmProjects\\QMINDv4"

# What do you want the program to do?
# record_new_data = False  # Records all data from your microphone
# break_up_audio = False  # Breaks up the recorded data to separate audio files
# play_recordings = True  # Plays you broken up audio files!

def create_recorded_data(directory, seconds):
    """
    Helper function to record audio (Actually records it and places into collected recordings)
    Args:
        directory: str
            The word that the person is saying multiple times
        seconds: int
            Amount of time given to record. (Usually 7-8 seconds)
    """
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    filename = f"collectedRecordings\\rawRecordings\\{directory}_RecordedData.wav"
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    # print("Say \"" + directory + "\" 5 times in 3")
    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


sound_file_name = "RecordedData.wav"
# These are the words used. If you want to add/delete them MAKE sure to add/delete the directory before
directories = ["the", "of", "and", "to", "be"]


def record_new_data():
    """
    Records all new data by calling the create recorded data function for each word we are training on
    """
    print("Get ready to record audio input")
    print("Wait ~0.5 seconds between each utterance of the word")
    print("You have 8 seconds for each, stay silent after you are done saying 5 utterances")
    sleep(5)
    for directory in directories:
        create_recorded_data(directory, 8)


def record_sentence(name, s=10):
    print("\nGet ready to record audio input \n")
    sleep(2)
    print(f"you will have {s} seconds to read the following sentence \n")
    sleep(2)
    print('"That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he\'s foiled you again, creating chaos"\n')
    sleep(1)
    print("recording in 3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)

    create_recorded_data("sentence", s)

    break_up_audio(["sentence"])

    export_recordings(name, ["sentence"])


def break_up_audio(dirs= directories):  # Break up the audio into separate word files
    """
    Breaks up the audio into separate word files to process and prints out a guess as to what the audio file says
    """
    for directory in dirs:
        sound_file = AudioSegment.from_wav(f"collectedRecordings\\rawRecordings\\{directory}_RecordedData.wav")
        # min_silence_len=time in milliseconds, silence_thresh=what the comp classifies as silence in dB
        audio_chunks = split_on_silence(sound_file, min_silence_len=100, silence_thresh=(int(sound_file.dBFS) - 10))

        clear_audio(f"collectedRecordings\\{directory}")
        numWords = 0
        for i, chunk in enumerate(audio_chunks):
            out_file = f"collectedRecordings\\{directory}\\{i+1}.wav"
            # print("Exporting", out_file) # Check to see exporting
            chunk.export(out_file, format="wav")
            numWords += 1
        print(f"Exported {numWords} .wav files")

        audio_to_text(f"collectedRecordings\\rawRecordings\\{directory}_RecordedData.wav")  # converts audio to text


def audio_to_text(audio_dir):
    """
    Transcribes an audio file (Prints out the audio to text)
    Args:
        dir: str
            Path to where the audio file is
    """
    # initialize the recognizer
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(audio_dir) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)


def play_recordings(dirs= directories):
    """
    Plays all of the recordings back to user to ensure that they were recorded correctly (A test feature)
    """
    for directory in dirs:
        numFiles = os.listdir(f"collectedRecordings\\{directory}")
        print(f"Words in \"{directory}\" directory")
        for segment in range(len(numFiles)):
            sound_file = AudioSegment.from_wav(
                f"collectedRecordings\\{directory}\\{1+segment}.wav")
            playsound(f"collectedRecordings\\{directory}\\{1+segment}.wav")
            playsound(f"soundEffects\\Beep.wav")


def export_recordings(name, dirs=directories):
    """
    copy files from collected recordings to /words/'word'/foo/
    """
    for directory in dirs:
        numFiles = os.listdir(f"collectedRecordings\\{directory}")
        for file in range(1,len(numFiles)+1):
            src = f"collectedRecordings\\{directory}\\{file}.wav"
            dst = f"words\\{directory}\\{name}\\{file}.wav"
            shutil.copy(src,dst)
            # print(f"copied {src} to {dst}")


def record_and_save(name):
    """ records and exports files for all words
    input:
        name: string of your name
    """
    record_new_data()
    break_up_audio()
    # play_recordings()
    export_recordings(name)


