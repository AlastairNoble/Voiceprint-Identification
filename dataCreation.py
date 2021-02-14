from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import wave
import os
import shutil
from playsound import playsound
import pyaudio
from time import sleep


directory_to_project = dir_path = os.path.dirname(os.path.realpath(__file__))  # "C:\\Users\\harle\\PycharmProjects\\QMINDv4"

# What do you want the program to do?
record_new_data = False  # Records all data from your microphone
break_up_audio = False  # Breaks up the recorded data to separate audio files
play_recordings = True  # Plays you broken up audio files!


def clear_audio(path):  # Helper Function to Empty Directory of Useless Files
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def create_recorded_data(directory, filename, seconds):  # Helper function to record audio
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    filename = f"collectedRecordings\\rawRecordings\\{directory}_{filename}"
    print(filename)
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print("Say \"" + directory + "\" 5 times in 3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)
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

if record_new_data:
    print("Get ready to record audio input")
    print("Wait ~0.5 seconds between each utterance of the word")
    print("You have 8 seconds for each, stay silent after you are done saying 5 utterances")
    sleep(5)
    for directory in directories:
        create_recorded_data(directory, sound_file_name, 8)

if break_up_audio:  # Break up the audio into separate word files
    for directory in directories:
        sound_file = AudioSegment.from_wav(f"{directory_to_project}\\collectedRecordings\\rawRecordings\\{directory}_RecordedData.wav")
        # min_silence_len=time in milliseconds, silence_thresh=what the comp classifies as silence in dB
        audio_chunks = split_on_silence(sound_file, min_silence_len=400, silence_thresh=(int(sound_file.dBFS) - 10))

        clear_audio(f"collectedRecordings\\{directory}")
        numWords = 0
        for i, chunk in enumerate(audio_chunks):
            out_file = f"collectedRecordings\\{directory}\\{i+1}.wav"
            # print("Exporting", out_file) # Check to see exporting
            chunk.export(out_file, format="wav")
            numWords += 1
        print(f"Exported {numWords} .wav files")

        # CONVERT AUDIO TO TEXT ------------- cool lil feature
        # initialize the recognizer
        r = sr.Recognizer()

        # open the file
        with sr.AudioFile(f"collectedRecordings\\rawRecordings\\{directory}_RecordedData.wav") as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)

if play_recordings:  # A test feature to test segments
    for directory in directories:
        numFiles = os.listdir(f"collectedRecordings\\{directory}")
        print(f"Words in \"{directory}\" directory")
        for segment in range(len(numFiles)):
            sound_file = AudioSegment.from_wav(
                f"collectedRecordings\\{directory}\\{1+segment}.wav")
            playsound(f"collectedRecordings\\{directory}\\{1+segment}.wav")
            playsound(f"soundEffects\\Beep.wav")
